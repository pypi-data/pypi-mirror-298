#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from dataclasses import dataclass
from typing import Optional

from pytorch_lightning.loggers import WandbLogger as LightningWandbLogger

from lightly_train._configs.config import Config


@dataclass
class WandbLoggerArgs(Config):
    name: Optional[str] = None
    version: Optional[str] = None
    offline: bool = False
    anonymous: Optional[bool] = None
    project: Optional[str] = None
    # TODO(Philipp, 09/24): Enable log_model: Literal["all"] | bool = False.
    # Currently, the type is set to bool because the type Literal is a collection
    # and OmegaConf does not support unions of collections and single values.
    log_model: bool = False
    prefix: str = ""
    checkpoint_name: Optional[str] = None


# No customizations necessary.
WandbLogger = LightningWandbLogger
