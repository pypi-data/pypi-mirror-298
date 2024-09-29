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
"""Utility to write custom data to the Tensorboard.

Usage:
    Call ``self.add_tensorboard`` of ``TFAIPLayer`` which expects ``TensorboardWriter`` and a Tensor as input.
    The ``TensorboardWriter`` expects a function as parameter which must write the data to the Tensorboard.
"""
from typing import Optional, List, Callable

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras


class TensorboardWriterInterface(keras.metrics.Metric):
    def __init__(self, func: Callable[[str, np.ndarray, int], None], **kwargs):
        super().__init__(**kwargs)
        self.handle_fn = func

    def handle(self, name: str, value: np.ndarray, step: int):
        return self.handle_fn(name, value, step)


class TensorboardMetricWriter(TensorboardWriterInterface):
    def get_config(self):
        cfg = super().get_config()
        cfg["func"] = "NOT_SUPPORTED"
        cfg["metric"] = "NOT_SUPPORTED"
        return cfg

    @classmethod
    def from_config(cls, config):
        return super().from_config(config)

    def __init__(self, func: Callable[[str, np.ndarray, int], None], metric: keras.metrics.Metric):
        super().__init__(func, name=metric.name)
        self.metric = metric

    def update_state(self, *args, **kwargs):
        return self.metric(*args, **kwargs)

    def result(self):
        return self.metric.result()

    def reset_state(self):
        return self.metric.reset_state()

    def reset_states(self):
        # backwards compatibility with TF < 2.5
        return self.reset_state()


class TensorboardWriter(TensorboardWriterInterface):
    """Dummy Metric that holds the outputs of the last batch.

    Used to write this data to the logs, which can then be written to the tensorboard
    """

    def get_config(self):
        cfg = super().get_config()
        cfg["input_shape"] = self.initial_input_shape
        cfg["n_storage"] = self.n_storage
        cfg["func"] = "NOT_SUPPORTED"
        return cfg

    @classmethod
    def from_config(cls, config):
        return super().from_config(config)

    def __init__(
        self,
        func: Callable[[str, np.ndarray, int], None],
        input_shape: Optional[List[Optional[int]]] = None,
        n_storage: int = 2,
        **kwargs,
    ):
        super().__init__(func, **kwargs)
        self.initial_input_shape = input_shape
        self.n_storage = n_storage
        self.store_w = tf.Variable(
            initial_value=[],
            shape=tf.TensorShape(None),  # dynamic shape
            trainable=False,
            validate_shape=False,
            name="store",
            dtype=self.dtype,
        )

    def update_state(self, y_true, y_pred, **kwargs):
        del y_true  # not used, the actual data is in y_pred, y_true is dummy data
        return self.store_w.assign(y_pred)

    def result(self):
        # return the stored variable
        return tf.stack(self.store_w)

    def reset_state(self):
        self.store_w.assign([])
