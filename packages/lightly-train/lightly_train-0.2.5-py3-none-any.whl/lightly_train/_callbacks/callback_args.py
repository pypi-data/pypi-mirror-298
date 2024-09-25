#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from dataclasses import dataclass, field
from typing import Optional

from lightly_train._callbacks.checkpoint import ModelCheckpointArgs
from lightly_train._configs.config import Config


@dataclass
class LearningRateMonitorArgs(Config):
    pass


@dataclass
class DeviceStatsMonitorArgs(Config):
    pass


@dataclass
class EarlyStoppingArgs(Config):
    monitor: str = "train_loss"
    patience: int = int(1e12)
    check_finite: bool = True


@dataclass
class CallbackArgs(Config):
    learning_rate_monitor: Optional[LearningRateMonitorArgs] = field(
        default_factory=LearningRateMonitorArgs
    )
    device_stats_monitor: Optional[DeviceStatsMonitorArgs] = field(
        default_factory=DeviceStatsMonitorArgs
    )
    early_stopping: Optional[EarlyStoppingArgs] = field(
        default_factory=EarlyStoppingArgs
    )
    model_checkpoint: Optional[ModelCheckpointArgs] = field(
        default_factory=ModelCheckpointArgs
    )
