#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from dataclasses import dataclass, field
from typing import Optional

from lightly_train._configs.config import Config
from lightly_train._loggers.jsonl import JSONLLoggerArgs
from lightly_train._loggers.tensorboard import TensorBoardLoggerArgs
from lightly_train._loggers.wandb import WandbLoggerArgs


@dataclass
class LoggerArgs(Config):
    jsonl: Optional[JSONLLoggerArgs] = field(default_factory=JSONLLoggerArgs)
    tensorboard: Optional[TensorBoardLoggerArgs] = field(
        default_factory=TensorBoardLoggerArgs
    )
    wandb: Optional[WandbLoggerArgs] = None
