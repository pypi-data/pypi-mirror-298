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
import json
import logging
from argparse import Action

from tfaip.lav.callbacks.dump_results import DumpResultsCallback
from tfaip.util.tfaipargparse import TFAIPArgumentParser

logger = logging.getLogger(__name__)


def run():
    logging.basicConfig(level=logging.INFO)
    main(*parse_args())


def main(args, scenario_cls, scenario_params, predictor_params):
    data = args.data
    callbacks = []
    if args.dump:
        callbacks.append(DumpResultsCallback(args.dump))

    lav_params = args.lav
    logger.info("data=" + data.to_json(indent=2))
    logger.info("lav_params=" + lav_params.to_json(indent=2))

    # create the lav and run it
    lav = scenario_cls.create_multi_lav(lav_params, scenario_params, predictor_params)
    for i, r in enumerate(lav.run(data, run_eagerly=args.run_eagerly, callbacks=callbacks)):
        print(json.dumps(r, indent=2))
        lav.benchmark_results.pretty_print()


class ScenarioSelectionAction(Action):
    def __call__(self, parser: TFAIPArgumentParser, namespace, values, option_string=None):
        from tfaip.imports import ScenarioBase

        export_dirs = values
        scenario, scenario_params = ScenarioBase.from_path(export_dirs[0])  # scenario based on first model
        lav_params = scenario.lav_cls().params_cls()()
        lav_params.model_path = export_dirs
        predictor_params = scenario.multi_predictor_cls().params_cls()()

        parser.add_root_argument("lav", scenario.lav_cls().params_cls(), default=lav_params)
        parser.add_root_argument(
            "predictor", scenario.multi_predictor_cls().params_cls(), default=predictor_params, ignore=["pipeline"]
        ),
        parser.add_root_argument("data", scenario.predict_generator_params_cls())

        setattr(namespace, self.dest, values)
        setattr(namespace, "scenario", scenario)
        setattr(namespace, "scenario_params", scenario_params)


def parse_args(args=None):

    parser = TFAIPArgumentParser()
    parser.add_argument("--export_dirs", required=True, nargs="+", action=ScenarioSelectionAction)
    parser.add_argument(
        "--run_eagerly",
        action="store_true",
        help="Run the graph in eager mode. This is helpful for debugging. Note that all custom layers must be added to ModelBase!",
    )
    parser.add_argument("--dump", type=str, help="Dump the predictions and results to the given filepath")

    args = parser.parse_args(args=args)
    return args, args.scenario, args.scenario_params, args.predictor


if __name__ == "__main__":
    run()
