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
"""Definition of the various Optimizers and their OptimizerParams"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple, Any, Dict, Type, TYPE_CHECKING, Union, Optional, List
from packaging import version

from paiargparse import pai_dataclass, pai_meta

if TYPE_CHECKING:
    # do not import here
    import tensorflow as tf

    from tensorflow.keras.optimizers import Optimizer
    TOptimizer = Type[Optimizer]
    if version.parse(tf.__version__) >= version.parse("2.11.0"):
        from tensorflow.keras.optimizers.legacy import Optimizer as LegacyOptimizer
        TOptimizer = Type[Union[Optimizer, LegacyOptimizer]]
    elif version.parse(tf.__version__) >= version.parse("2.9.0"):
        from tensorflow.keras.optimizers.experimental import Optimizer as ExperimentalOptimizer
        TOptimizer = Type[Union[Optimizer, ExperimentalOptimizer]]


@pai_dataclass
@dataclass
class OptimizerParams(ABC):
    """General parameters of a Optimizer"""

    @abstractmethod
    def create(self) -> Tuple["TOptimizer", Dict[str, Any]]:
        raise NotImplementedError

    clip_norm: Optional[float] = field(
        default=None, metadata=pai_meta(help="float or None. If set, clips gradients to a maximum norm.")
    )
    clip_value: Optional[float] = field(
        default=None, metadata=pai_meta(help="float or None. If set, clips gradients to a maximum value.")
    )
    global_clip_norm: Optional[float] = field(
        default=None,
        metadata=pai_meta(
            help="float or None. If set, the gradient of all weights is clipped so that "
            "their global norm is no higher than this value."
        ),
    )

    def _clip_grad_args(self):
        return {
            "clipnorm": self.clip_norm,
            "clipvalue": self.clip_value,
            "global_clipnorm": self.global_clip_norm,
        }


@pai_dataclass(alt="SGD")
@dataclass
class SGDOptimizer(OptimizerParams):
    """The Stochastic Gradient Optimizer"""

    momentum: float = 0.0
    nesterov: bool = False
    weight_decay: float = 0.0

    def create(self):
        import tensorflow as tf  # pylint: disable = import-outside-toplevel

        if version.parse(tf.__version__) >= version.parse("2.11.0"):
            from tensorflow.keras.optimizers.legacy import SGD
            from tensorflow.keras.optimizers.experimental import SGD as SGDW
        else:
            from tensorflow.keras.optimizers import SGD
            from tensorflow_addons.optimizers import SGDW

        if self.weight_decay > 0:
            return SGDW, {
                "weight_decay": self.weight_decay,
                "momentum": self.momentum,
                "nesterov": self.nesterov,
                **self._clip_grad_args(),
            }
        else:
            return SGD, {
                "momentum": self.momentum,
                "nesterov": self.nesterov,
                **self._clip_grad_args(),
            }


@pai_dataclass(alt="Adam")
@dataclass
class AdamOptimizer(OptimizerParams):
    """The Adam optimizer"""

    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-7
    weight_decay: float = 0.0

    def create(self):
        import tensorflow as tf

        if version.parse(tf.__version__) >= version.parse("2.11.0"):
            from tensorflow.keras.optimizers import AdamW
        elif version.parse(tf.__version__) >= version.parse("2.9.0"):
            from tensorflow.keras.optimizers.experimental import AdamW
        else:
            from tensorflow_addons.optimizers import AdamW

        if version.parse(tf.__version__) >= version.parse("2.11.0"):
            from tensorflow.keras.optimizers.legacy import Adam
        else:
            from tensorflow.keras.optimizers import Adam

        if self.weight_decay > 0:
            return AdamW, {
                "weight_decay": self.weight_decay,
                "beta_1": self.beta_1,
                "beta_2": self.beta_2,
                "epsilon": self.epsilon,
                **self._clip_grad_args(),
            }
        else:
            return Adam, {
                "beta_1": self.beta_1,
                "beta_2": self.beta_2,
                "epsilon": self.epsilon,
                **self._clip_grad_args(),
            }


@pai_dataclass(alt="Adamax")
@dataclass
class AdamaxOptimizer(AdamOptimizer):
    """The Adamax Optimizer"""

    def create(self):
        import tensorflow as tf  # pylint: disable = import-outside-toplevel

        if version.parse(tf.__version__) >= version.parse("2.11.0"):
            from tensorflow.keras.optimizers.legacy import Adamax
        else:
            from tensorflow.keras.optimizers import Adamax

        return Adamax, {
            "beta_1": self.beta_1,
            "beta_2": self.beta_2,
            "epsilon": self.epsilon,
            **self._clip_grad_args(),
        }


@pai_dataclass(alt="RMSprop")
@dataclass
class RMSpropOptimizer(OptimizerParams):
    """The RMSprop Optimizer"""

    momentum: float = 0.0
    epsilon: float = 1e-7
    rho: float = 0.0
    centered: bool = False

    def create(self):
        import tensorflow as tf  # pylint: disable = import-outside-toplevel

        if version.parse(tf.__version__) >= version.parse("2.11.0"):
            from tensorflow.keras.optimizers.legacy import RMSprop
        else:
            from tensorflow.keras.optimizers import RMSprop

        return RMSprop, {
            "momentum": self.momentum,
            "rho": self.rho,
            "centered": self.centered,
            "epsilon": self.epsilon,
            **self._clip_grad_args(),
        }


@pai_dataclass(alt="AdaBelief")
@dataclass
class AdaBeliefOptimizer(OptimizerParams):
    """The AdaBeliefOptimizer"""

    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-14
    weight_decay: float = 0.0
    rectify: bool = True
    amsgrad: bool = False
    sma_threshold: float = 5.0
    total_steps: int = 0
    warmup_proportion: float = 0.1
    min_lr: float = 0.0

    def create(self):
        from adabelief_tf import AdaBeliefOptimizer as ABOpt  # pylint: disable = import-outside-toplevel

        return ABOpt, {
            "beta_1": self.beta_1,
            "beta_2": self.beta_2,
            "epsilon": self.epsilon,
            "weight_decay": self.weight_decay,
            "rectify": self.rectify,
            "amsgrad": self.amsgrad,
            "sma_threshold": self.sma_threshold,
            "total_steps": self.total_steps,
            "warmup_proportion": self.warmup_proportion,
            "min_lr": self.min_lr,
            **self._clip_grad_args(),
        }


@pai_dataclass(alt="LAMB")
@dataclass
class LAMBOptimizer(OptimizerParams):
    """The LAMBOptimizer"""

    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-6
    weight_decay: float = 0.0
    exclude_from_weight_decay: Optional[List[str]] = None
    exclude_from_layer_adaptation: Optional[List[str]] = None

    def create(self):
        from tensorflow_addons.optimizers import LAMB  # pylint: disable = import-outside-toplevel

        return LAMB, {
            "beta_1": self.beta_1,
            "beta_2": self.beta_2,
            "epsilon": self.epsilon,
            "weight_decay": self.weight_decay,
            "exclude_from_weight_decay": self.exclude_from_weight_decay,
            "exclude_from_layer_adaptation": self.exclude_from_layer_adaptation,
            **self._clip_grad_args(),
        }
