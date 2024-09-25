#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import os
from dataclasses import dataclass
from typing import Optional

from pytorch_lightning.loggers import TensorBoardLogger as LightningTensorBoardLogger
from pytorch_lightning.utilities import rank_zero_only
from typing_extensions import override

from lightly_train._configs.config import Config


@dataclass
class TensorBoardLoggerArgs(Config):
    name: str = ""
    version: str = ""
    log_graph: bool = False
    default_hp_metric: bool = True
    prefix: str = ""
    sub_dir: Optional[str] = None


class TensorBoardLogger(LightningTensorBoardLogger):
    @override
    @rank_zero_only
    def save(self) -> None:
        super().save()
        # Delete hparams file as the parent class creates it and there is no easy way
        # to disable it. We don't want hparams file because we'll save all parameters to
        # a custom file.
        dir_path = self.log_dir
        hparams_file = os.path.join(dir_path, self.NAME_HPARAMS_FILE)
        if self._fs.isfile(hparams_file):
            self._fs.rm(hparams_file)
