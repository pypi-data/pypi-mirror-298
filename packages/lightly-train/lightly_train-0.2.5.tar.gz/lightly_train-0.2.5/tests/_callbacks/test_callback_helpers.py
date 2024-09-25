#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from pathlib import Path

import pytest
from pytorch_lightning.callbacks import (
    DeviceStatsMonitor,
    EarlyStopping,
)

from lightly_train._callbacks import callback_helpers
from lightly_train._callbacks.callback_args import (
    CallbackArgs,
    LearningRateMonitorArgs,
)
from lightly_train._callbacks.checkpoint import ModelCheckpoint, ModelCheckpointArgs
from lightly_train.errors import ConfigUnknownKeyError, ConfigValidationError

from .. import helpers


@pytest.mark.parametrize(
    "callback_dict, expected_result",
    [
        # Test case for default empty dictionary
        ({}, CallbackArgs()),
        # Test case for None input
        (None, CallbackArgs()),
        # Test case for user config
        (
            {"model_checkpoint": {"every_n_epochs": 5}},
            CallbackArgs(model_checkpoint=ModelCheckpointArgs(every_n_epochs=5)),
        ),
    ],
)
def test_validate_callback_args__success(callback_dict, expected_result) -> None:
    callback_args = callback_helpers.validate_callback_args(callback_dict)
    assert callback_args == expected_result
    # The instance checks look unnecessary, but are actually needed. The reason is that
    # CallbackArgs() == omegaconf.create(CallbackArgs), but the latter is an instance of
    # a DictConfig, not of CallbackArgs.
    assert isinstance(callback_args, CallbackArgs)
    assert isinstance(callback_args.learning_rate_monitor, LearningRateMonitorArgs)


@pytest.mark.parametrize(
    "callback_dict, expected_exception, expected_message",
    [
        # Test case for wrong callback name
        (
            {"nonexisting_callback": {"any_arg": 5}},
            ConfigUnknownKeyError,
            "Unknown key in config: 'nonexisting_callback'",
        ),
        # Test case for forbidden argument name
        (
            {"model_checkpoint": {"out": "some_path"}},
            ConfigUnknownKeyError,
            "Unknown key in config: 'model_checkpoint.out'",
        ),
        # Test case for wrong argument type
        (
            {"model_checkpoint": True},
            ConfigValidationError,
            "Merge error: bool is not a subclass of ModelCheckpointArgs. value: True",
        ),
    ],
)
def test_validate_callback_args__failure(
    callback_dict, expected_exception, expected_message
) -> None:
    with pytest.raises(expected_exception, match=expected_message):
        callback_helpers.validate_callback_args(callback_dict)


def test_validate_callback_args_get_callbacks__default(tmp_path: Path) -> None:
    # Assert that validate_callback_args and get_callbacks work together.
    model = helpers.get_model()
    embedding_model = helpers.get_embedding_model(model=model)
    callback_args = callback_helpers.validate_callback_args(None)
    callbacks = callback_helpers.get_callbacks(
        callback_args=callback_args,
        out=tmp_path,
        model=model,
        embedding_model=embedding_model,
    )
    assert len(callbacks) == 4
    early_stopping = next(c for c in callbacks if isinstance(c, EarlyStopping))
    model_checkpoint = next(c for c in callbacks if isinstance(c, ModelCheckpoint))
    assert early_stopping.monitor == "train_loss"
    assert early_stopping.patience == int(1e12)
    assert model_checkpoint.save_last
    assert str(model_checkpoint.dirpath) == str(tmp_path / "checkpoints")


def test_get_callbacks__default(tmp_path: Path) -> None:
    model = helpers.get_model()
    embedding_model = helpers.get_embedding_model(model=model)
    callback_args = CallbackArgs()
    callbacks = callback_helpers.get_callbacks(
        callback_args=callback_args,
        out=tmp_path,
        model=model,
        embedding_model=embedding_model,
    )
    assert len(callbacks) == 4
    early_stopping = next(c for c in callbacks if isinstance(c, EarlyStopping))
    model_checkpoint = next(c for c in callbacks if isinstance(c, ModelCheckpoint))
    assert early_stopping.monitor == "train_loss"
    assert early_stopping.patience == int(1e12)
    assert model_checkpoint.save_last
    assert str(model_checkpoint.dirpath) == str(tmp_path / "checkpoints")


def test_get_callbacks__disable(tmp_path: Path) -> None:
    model = helpers.get_model()
    embedding_model = helpers.get_embedding_model(model=model)
    callback_args = CallbackArgs(
        learning_rate_monitor=None,
        early_stopping=None,
    )
    callbacks = callback_helpers.get_callbacks(
        callback_args=callback_args,
        out=tmp_path,
        model=model,
        embedding_model=embedding_model,
    )
    assert len(callbacks) == 2
    assert any(isinstance(c, DeviceStatsMonitor) for c in callbacks)
    assert any(isinstance(c, ModelCheckpoint) for c in callbacks)


def test_get_callbacks__user_config(tmp_path: Path) -> None:
    model = helpers.get_model()
    embedding_model = helpers.get_embedding_model(model=model)
    callback_args = CallbackArgs(
        model_checkpoint=ModelCheckpointArgs(every_n_epochs=5),
    )
    callbacks = callback_helpers.get_callbacks(
        callback_args=callback_args,
        out=tmp_path,
        model=model,
        embedding_model=embedding_model,
    )
    model_checkpoint = next(c for c in callbacks if isinstance(c, ModelCheckpoint))
    assert str(model_checkpoint.dirpath) == str(tmp_path / "checkpoints")
    assert model_checkpoint.every_n_epochs == 5
