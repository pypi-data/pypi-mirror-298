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
from dataclasses import dataclass
from typing import Type

import numpy as np
from paiargparse import pai_dataclass
from tfaip import Sample
from tfaip.data.pipeline.processor.dataprocessor import DataProcessorParams, MappingDataProcessor

from examples.atr.params import Keys


@pai_dataclass
@dataclass
class PrepareProcessorParams(DataProcessorParams):
    @staticmethod
    def cls() -> Type["MappingDataProcessor"]:
        return PrepareProcessor


class PrepareProcessor(MappingDataProcessor):
    def apply(self, sample: Sample) -> Sample:
        img = sample.inputs.transpose()
        encoded = [self.data_params.codec.index(c) for c in sample.targets]
        return sample.new_inputs({Keys.Image: img, Keys.ImageLength: np.array([img.shape[0]])}).new_targets(
            {Keys.Targets: np.array(encoded), Keys.TargetsLength: np.array([len(encoded)])}
        )
