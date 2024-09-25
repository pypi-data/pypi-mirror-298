#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pytorch_lightning import Callback
from pytorch_lightning.callbacks import (
    DeviceStatsMonitor,
    EarlyStopping,
    LearningRateMonitor,
)
from torch.nn import Module

from lightly_train._callbacks.callback_args import (
    CallbackArgs,
)
from lightly_train._callbacks.checkpoint import ModelCheckpoint
from lightly_train._checkpoint import CheckpointLightlyTrainModels
from lightly_train._configs import validate
from lightly_train._models.embedding_model import EmbeddingModel


def validate_callback_args(callback_dict: dict[str, Any] | None) -> CallbackArgs:
    callback_dictconfig = OmegaConf.create(
        {} if callback_dict is None else callback_dict
    )
    callback_dictconfig = validate.validate_dictconfig(
        callback_dictconfig, CallbackArgs
    )
    callback_args = OmegaConf.to_object(callback_dictconfig)
    assert isinstance(callback_args, CallbackArgs)  # make mypy happy
    return callback_args


def get_callbacks(
    callback_args: CallbackArgs,
    out: Path,
    model: Module,
    embedding_model: EmbeddingModel,
):
    callbacks: list[Callback] = []
    if callback_args.learning_rate_monitor is not None:
        callbacks.append(
            LearningRateMonitor(
                **dataclasses.asdict(callback_args.learning_rate_monitor)
            )
        )
    if callback_args.device_stats_monitor is not None:
        callbacks.append(
            DeviceStatsMonitor(**dataclasses.asdict(callback_args.device_stats_monitor))
        )
    if callback_args.early_stopping is not None:
        callbacks.append(
            EarlyStopping(**dataclasses.asdict(callback_args.early_stopping))
        )
    if callback_args.model_checkpoint is not None:
        callbacks.append(
            ModelCheckpoint(
                models=CheckpointLightlyTrainModels(
                    model=model, embedding_model=embedding_model
                ),
                dirpath=out / "checkpoints",
                **dataclasses.asdict(callback_args.model_checkpoint),
            )
        )
    return callbacks
