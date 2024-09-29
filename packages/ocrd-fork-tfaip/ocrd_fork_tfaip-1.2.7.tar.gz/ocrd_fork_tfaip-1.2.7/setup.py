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
import os

from setuptools import setup

setup(
    name="ocrd-fork-tfaip",
    license="GPL-v3.0",
    author="PLANET AI GmbH",
    author_email="admin@planet-ai.de",
    maintainer="bertsky",
    url="https://github.com/bertsky/tfaip",
    #url="https://github.com/Planet-AI-GmbH/tfaip",
    #download_url="https://github.com/Planet-AI-GmbH/tfaip/releases",
    entry_points={
        "console_scripts": [
            "tfaip-adapt-exported-model=tfaip.scripts.adapt_exported_model:run",
            "tfaip-benchmark-scenario-input-pipeline=tfaip.scripts.benchmark_scenario_input_pipeline:run",
            "tfaip-train=tfaip.scripts.train:run",
            "tfaip-lav=tfaip.scripts.lav:run",
            "tfaip-multi-lav=tfaip.scripts.lav_multi:run",
            "tfaip-evaluate=tfaip.scripts.evaluate:run",
            "tfaip-predict=tfaip.scripts.predict:run",
            "tfaip-experimenter=tfaip.scripts.experimenter:main",
            "tfaip-resume-training=tfaip.scripts.resume_training:main",
            "tfaip-train-from-params=tfaip.scripts.train_from_params:main",
        ],
    },
    python_requires=">=3.7",
    keywords=["machine learning", "tensorflow", "framework"],
)
