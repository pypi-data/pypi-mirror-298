# Copyright 2021 The tfaip authors. All Rights Reserved.
#
# This file is part of tfaip.
#
# tfaip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# tfaip is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# tfaip. If not, see http://www.gnu.org/licenses/.
# ==============================================================================
"""Implementation of LAV"""
import logging
import os
from abc import ABC
from queue import Queue
from threading import Thread
from packaging.version import Version
from typing import TYPE_CHECKING, Type, Dict, List, Callable, Optional, Iterable, Any

import tensorflow
import tensorflow.keras as keras
from tensorflow.python.keras.callbacks import Callback, ProgbarLogger
from tensorflow.python.keras.engine import data_adapter
from tfaip import LAVParams, DataGeneratorParams, ScenarioBaseParams
from tfaip import Sample
from tfaip.device.device_config import DeviceConfig, distribute_strategy
from tfaip.evaluator.evaluator import EvaluatorBase
from tfaip.lav.callbacks.lav_callback import LAVCallback
from tfaip.lav.callbacks.print_callback import PrintCallback
from tfaip.model.graphbase import create_lav_graph
from tfaip.scenario.scenariobase import ScenarioBase
from tfaip.trainer.callbacks.benchmark_callback import BenchmarkCallback, BenchmarkResults
from tfaip.trainer.callbacks.extract_logs import ExtractLogsCallback
from tfaip.util.file.oshelper import ChDir
from tfaip.util.sample.shape_utils import to_unbatched_samples
from tfaip.util.tftyping import sync_to_numpy_or_python_type

if TYPE_CHECKING:
    from tfaip.data.data import DataBase
    from tfaip.model.modelbase import ModelBase


if Version(tensorflow.version.VERSION) >= Version("2.6"):
    from keras.callbacks import CallbackList
else:
    from tensorflow.keras.callbacks import CallbackList

logger = logging.getLogger(__name__)


class MetricsAccumulator:
    """
    Computation of the running weighted sum (=weighted mean) of a dictionary of float (here the metrics of the scenario)
    Call final() to access the mean.

    Attributes:
        running_sum: The running weighted sum of all values
        running_weight: The sum of all weights
    """

    def __init__(self):
        self.running_sum: Dict[str, float] = {}
        self.running_weight: Dict[str, float] = {}

    def accumulate_dict_sum(self, new_values: Dict[str, float], sample_weights: Dict[str, float]):
        def weighted(value, weight):
            if weight is None:
                return value

            return value * weight

        if len(self.running_sum) == 0:
            self.running_sum = {k: 0 for k, v in new_values.items()}
            self.running_weight = {k: 0 for k, v in new_values.items()}

        self.running_sum = {
            k: (self.running_sum[k] + weighted(v, sample_weights.get(k, None))) for k, v in new_values.items()
        }
        self.running_weight = {
            k: (v + (1 if k not in sample_weights else sample_weights[k])) for k, v in self.running_weight.items()
        }

    def final(self):
        return {k: v / self.running_weight[k] for k, v in self.running_sum.items()}


class InplaceCallbackList(CallbackList):
    """Callback list that does not create new log objects

    This is required in Tensorflow 2.5.x to support adding and removing of log entries
    """

    def _process_logs(self, logs, is_batch_hook=False):
        new_logs = super()._process_logs(logs, is_batch_hook).copy()
        if logs is not None:
            logs.clear()
            logs.update(new_logs)
            new_logs = logs
        return new_logs


class EvaluationCallback(Callback):
    """Callback to run the post-proc pipeline and call the evaluator
    run post proc pipeline in a separate thread so that it is instantiated only once
    the EvaluationCallback handles writing to post proc queue, reading the post proc data back again
    evaluating the result and writing it to the logs
    """

    def __init__(self, evaluator: EvaluatorBase, data_pipeline, callbacks: List[LAVCallback]):
        super().__init__()
        self._supports_tf_logs = True
        self.evaluator = evaluator
        self.write_queue = Queue()

        def post_proc_worker():
            def read_fn():
                while True:
                    sample = self.write_queue.get()
                    if sample is None:
                        break
                    yield sample

            with data_pipeline.process_output(read_fn()) as samples:
                for sample in samples:
                    evaluator.update_state(sample)
                    for cb in callbacks:
                        cb.on_sample_end(sample)

        self.post_proc_runner = Thread(target=post_proc_worker, daemon=True)
        self.post_proc_runner.start()

    def on_test_batch_end(self, batch, logs=None):
        (inputs, targets, meta), _, outputs = sync_to_numpy_or_python_type(logs["__outputs__"])

        samples = to_unbatched_samples(inputs, targets, outputs, meta)
        for sample in samples:
            self.write_queue.put(sample)

        # logs.update(self.evaluator.result())  # not up to date, since running asynchron!
        del logs["__outputs__"]

    def on_test_end(self, logs=None):
        assert logs is not None
        self.write_queue.put(None)  # end message
        self.post_proc_runner.join()  # wait to collect all samples
        logs.update(self.evaluator.result())  # add the final result


class LAV(ABC):
    """
    This is the base Class for Loading And Validation (LAV) a scenario. By default, LAV is independent of the scenario
    and should therefore not be overridden (but it is possible though in Meta of a Scenario).

    LAV will open an exported (or the best) model, create the metrics of the actual scenario. Then predict is called
    on the model on the DataBase validation(!) set and fed to the metric to obtain results (MetricsAccumulator).
    During the prediction a models print_evaluate method is called to print informative text.

    Override _custom_callbacks to "inject" logic for processing samples during LAV (e.g. saving or printing).
    """

    @classmethod
    def params_cls(cls) -> Type[LAVParams]:
        return LAVParams

    def __init__(
        self,
        params: LAVParams,
        scenario_params: ScenarioBaseParams,
        **kwargs,
    ):
        assert len(kwargs) == 0, f"Not all kwargs processed by subclasses: {kwargs}"
        assert params.model_path
        self._scenario_cls = scenario_params.cls()
        self._scenario_params = scenario_params
        self._params = params
        self.device_config = DeviceConfig(self._params.device)
        self._data: Optional["DataBase"] = None
        self._model: Optional["ModelBase"] = None
        self.benchmark_results = BenchmarkResults()

    @property
    def params(self) -> LAVParams:
        return self._params

    @distribute_strategy
    def run(
        self,
        generator_params: Iterable[DataGeneratorParams],
        keras_model: keras.Model = None,
        run_eagerly=False,
        callbacks: List[LAVCallback] = None,
        return_tensorboard_outputs=False,
        instantiate_graph=False,
    ) -> Iterable[Dict[str, float]]:
        """

        Args:
            generator_params:
            keras_model:
            run_eagerly: Run LAV in eager mode, also sets instantiate_graph=True
            callbacks:
            return_tensorboard_outputs:
            instantiate_graph: Force to instantiate the real graph. This might lead to changed of the original graph
                if there were changes in the code. Always True if run_eagerly

        Returns:
            Results for each DataGeneratorParams in generator_params

        """
        if run_eagerly:
            instantiate_graph = True
        callbacks = callbacks or []

        if self._params.print_samples:
            callbacks.append(PrintCallback())

        callbacks += self._custom_callbacks()
        with ChDir(os.path.join(self._params.model_path)):
            # resources are located in parent dir
            self._data = self._scenario_cls.data_cls()(
                self._scenario_params.data,
                **self._scenario_cls.static_data_kwargs(self._scenario_params),
            )
        evaluator: EvaluatorBase = self._scenario_cls.create_evaluator(
            self._scenario_params.evaluator,
            **self._scenario_cls.additional_evaluator_kwargs(self._data, self._scenario_params),
        )

        root_graph = self._scenario_cls.model_cls().root_graph_cls()(
            self._scenario_params.model,
            setup_graph=False,
            **self._scenario_cls.additional_root_graph_kwargs(self._data, self._scenario_params),
        )
        self._model = model = root_graph.create_model(
            **self._scenario_cls.additional_model_kwargs(self._data, self._scenario_params)
        )

        if run_eagerly:
            logger.warning(
                "Running in eager mode. Use this only for debugging, since the graph of the saved model "
                'might get changed due to "reconstruction" of the graph'
            )

        if not keras_model:
            keras_model = keras.models.load_model(
                os.path.join(self._params.model_path, "serve"),
                compile=False,
                custom_objects=model.all_custom_objects() if instantiate_graph else model.base_custom_objects(),
            )

        # create a new keras model that uses the inputs and outputs of the loaded model but adds the targets of the
        # dataset. Then create the metrics as output of the new model
        class LAVModel(keras.models.Model):
            def __init__(self, model, prediction_graph):
                super().__init__()
                self.model = model
                self.graph = prediction_graph

            def call(self, inputs, training=None, mask=None):
                inputs, targets, meta = inputs
                outputs = self.graph.lav(inputs, targets)
                return outputs

            def test_step(self, data):
                data = data_adapter.expand_1d(data)
                x, y, sample_weight = data_adapter.unpack_x_y_sample_weight(data)
                inputs, _, meta = x

                y_pred, pre_proc_targets = self(x, training=False)

                # Updates stateful loss metrics.
                self.compiled_loss(y, y_pred, sample_weight, regularization_losses=self.losses)

                self.compiled_metrics.update_state(y, y_pred, sample_weight)
                logs = {m.name: m.result() for m in self.metrics}
                logs["__outputs__"] = ((inputs, pre_proc_targets, meta), y, y_pred)
                return logs

            def get_config(self):
                raise NotImplementedError

        keras_model.compile(run_eagerly=run_eagerly)
        keras_model.run_eagerly = True
        lav_model = LAVModel(model, create_lav_graph(model, keras_model))
        lav_model.compile(run_eagerly=run_eagerly)

        def regroup(i, t, m):
            return (i, t, m), {}

        # accumulate the mean
        for params in generator_params:
            val_data = self._data.create_pipeline(self._params.pipeline, params)
            with evaluator:
                dataset = val_data.input_dataset()
                for cb in callbacks:
                    cb.setup(params, self, self._data, model)
                    cb.on_lav_start()

                extract_logs_callback = ExtractLogsCallback(test_prefix="")
                benchmark_callback = BenchmarkCallback(extract_logs_callback)
                eval_callbacks = [
                    EvaluationCallback(evaluator, val_data, callbacks),
                    extract_logs_callback,
                    benchmark_callback,
                ]
                if not self._params.silent:
                    eval_callbacks.append(ProgbarLogger(count_mode="steps"))

                r = lav_model.evaluate(
                    dataset.map(regroup),
                    callbacks=InplaceCallbackList(eval_callbacks, model=lav_model),
                    return_dict=True,
                    verbose=0 if self._params.silent else 1,
                )
                self.benchmark_results = benchmark_callback.last_test_results
                if return_tensorboard_outputs:
                    r.update(extract_logs_callback.extracted_logs)

                for cb in callbacks:
                    cb.on_lav_end(r)

                if not self._params.silent:
                    logger.info("LAV results: \n" + "\n    ".join([f"{k} = {v}" for k, v in r.items()]))
                yield r

    def _custom_callbacks(self) -> List[LAVCallback]:
        """Additional custom callbacks

        This function is meant to be implemented by a subclassed LAV to provide custom LAVCallbacks for a scenario.
        """

        return []

    def extract_dump_data(self, sample: Sample):
        return sample.targets, sample.outputs
