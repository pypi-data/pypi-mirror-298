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
import unittest

import pytest
from tensorflow.python.keras.backend import clear_session

from examples.template.general.scenario import TemplateScenario
from tfaip.util.testing.training import single_train_iter, resume_training, lav_test_case, warmstart_training_test_case


# [remove @pytest.mark.skip]
@pytest.mark.skip(reason="This test is only a show-case how to implement a tests for a custom scenario.")
class TestTemplateScenario(unittest.TestCase):
    def tearDown(self) -> None:
        clear_session()

    def test_data(self):
        trainer_params = TemplateScenario.default_trainer_params()
        # (optionally) disable parallel processing to simplify debugging
        trainer_params.scenario.data.pre_proc.run_parallel = False
        data = trainer_params.scenario.data.create()

        # First check if generate_input_samples is working which will return single pre-processed samples
        with trainer_params.gen.train_data(data).generate_input_samples(auto_repeat=False) as samples:
            train_data = next(samples)
        with trainer_params.gen.val_data(data).generate_input_samples(auto_repeat=False) as samples:
            val_data = next(samples)

        # [check if train_data and val_data comprise correct data]

        # Then check if the tf.data.Dataset can be correctly set up
        # If the first test works and this fails, most probably there are mismatches of the input and target layer
        # specs. See TemplateData
        with trainer_params.gen.train_data(data).generate_input_batches(auto_repeat=False) as batches:
            train_data = next(batches)
        with trainer_params.gen.val_data(data).generate_input_batches(auto_repeat=False) as batches:
            val_data = next(batches)

        # [check if train_data and val_data comprise correct data]

    def test_single_train_iter(self):
        single_train_iter(self, TemplateScenario)

    def test_resume_training(self):
        resume_training(self, TemplateScenario)

    def test_lav(self):
        lav_test_case(self, TemplateScenario)

    def test_warmstart(self):
        warmstart_training_test_case(self, TemplateScenario)
