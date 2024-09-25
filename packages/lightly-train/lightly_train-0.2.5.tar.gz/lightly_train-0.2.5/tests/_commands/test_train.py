#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import dataclasses
import inspect
import logging
from pathlib import Path

import pytest
import torch
from omegaconf import MISSING, OmegaConf
from pytest import LogCaptureFixture

from lightly_train._checkpoint import Checkpoint
from lightly_train._commands import train
from lightly_train._commands.train import TrainConfig
from lightly_train._methods import method_helpers

from .. import helpers

try:
    import tensorboard
except ImportError:
    tensorboard = None


def test_train__cpu(tmp_path: Path) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="simclr",
        batch_size=4,
        num_workers=2,
        epochs=1,
        accelerator="cpu",
    )

    # Check that the correct files were created.
    filepaths = {fp.relative_to(out) for fp in out.rglob("*")}
    expected_filepaths = {
        Path("checkpoints"),
        Path("checkpoints") / "epoch=0-step=2.ckpt",
        Path("checkpoints") / "last.ckpt",
        Path("metrics.jsonl"),
        Path("train.log"),
    }
    if tensorboard is not None:
        # Tensorboard filename is not deterministic, so we need to find it.
        tensorboard_filepath = next(
            fp for fp in filepaths if fp.name.startswith("events.out.tfevents")
        )
        expected_filepaths.add(tensorboard_filepath)

    assert filepaths == expected_filepaths


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
@pytest.mark.parametrize("num_workers", [0, 2])
def test_train(tmp_path: Path, caplog: LogCaptureFixture, num_workers: int) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="simclr",
        batch_size=4,
        num_workers=num_workers,
        epochs=1,
        devices=1,
    )

    # Check that we can resume training
    last_ckpt_path = out / "checkpoints" / "last.ckpt"
    with caplog.at_level(logging.INFO):
        train.train(
            out=out,
            data=data,
            model="torchvision/resnet18",
            method="simclr",
            batch_size=4,
            num_workers=2,
            epochs=2,
            devices=1,
            resume=True,
        )
    assert (
        f"Restoring states from the checkpoint path at {last_ckpt_path}" in caplog.text
    )
    # Epochs in checkpoint are 0-indexed. Epoch 1 is therefore the second epoch.
    assert torch.load(last_ckpt_path)["epoch"] == 1


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__overwrite_true(tmp_path: Path) -> None:
    """Test that overwrite=True allows training with an existing output directory that
    contains files."""
    out = tmp_path / "out"
    data = tmp_path / "data"
    out.mkdir(parents=True, exist_ok=True)
    (out / "file.txt").touch()
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="simclr",
        batch_size=4,
        num_workers=2,
        epochs=1,
        devices=1,
        overwrite=True,
    )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__overwrite_false(tmp_path: Path) -> None:
    (tmp_path / "file.txt").touch()

    with pytest.raises(ValueError):
        train.train(
            out=tmp_path,
            data=tmp_path,
            model="torchvision/resnet18",
            method="simclr",
            batch_size=4,
            num_workers=2,
            epochs=1,
        )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__embed_dim(tmp_path: Path) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="simclr",
        batch_size=4,
        num_workers=2,
        epochs=1,
        devices=1,
        embed_dim=64,
    )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__custom_model(tmp_path: Path) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model=helpers.DummyCustomModel(),
        method="simclr",
        batch_size=4,
        num_workers=2,
        devices=1,
        epochs=1,
    )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__parameters() -> None:
    """Tests that train function and TrainConfig have the same parameters and default
    values.

    This test is here to make sure we don't forget to update train/TrainConfig when
    we change parameters in one place.
    """
    config = dataclasses.asdict(TrainConfig())
    train_fn = inspect.signature(train.train)

    # Check that train function and TrainConfig have the same parameters.
    assert config.keys() == train_fn.parameters.keys()

    for param_name, param in train_fn.parameters.items():
        if param.default is inspect.Parameter.empty:
            # Check that parameter without default is MISSING in the config.
            assert config[param_name] == MISSING
        else:
            # Check that parameter with default has the same value as in config.
            assert param.default == config[param_name]


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__zero_epochs(tmp_path: Path) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)
    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="simclr",
        batch_size=4,
        num_workers=2,
        devices=1,
        epochs=0,
    )
    assert (out / "checkpoints" / "last.ckpt").exists()


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train_from_config(tmp_path: Path) -> None:
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)
    config = OmegaConf.create(
        dict(
            out=str(out),
            data=str(data),
            model="torchvision/resnet18",
            method="simclr",
            batch_size=4,
            num_workers=2,
            epochs=1,
            devices=1,
            optim_args={"lr": 0.1, "betas": [0.9, 0.99]},
            loader_args={"shuffle": True},
            trainer_args={"min_epochs": 1},
            model_args={"num_classes": 42},
            callbacks={"model_checkpoint": {"every_n_epochs": 5}},
            loggers={"jsonl": {"flush_logs_every_n_steps": 5}},
        )
    )
    train.train_from_config(config=config)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
@pytest.mark.parametrize("method", method_helpers.list_methods())
@pytest.mark.parametrize(
    "devices", [1]
)  # TODO(Philipp, 09/24): Add test with 2 devices back.
def test_train__method(tmp_path: Path, method: str, devices: int) -> None:
    if torch.cuda.device_count() < devices:
        pytest.skip("Test requires more GPUs than available.")

    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        devices=devices,
        method=method,
        batch_size=4,
        num_workers=2,
        epochs=1,
    )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_train__checkpoint_gradients(tmp_path: Path) -> None:
    """Test that checkpoints saved during training do not have disabled gradients.

    This is especially a problem for methods with momentum encoders (e.g. DINO) where
    the momentum encoder does not receive gradients during training. As the momentum
    encoder is used for finetuning, we want to make sure that it doesn't have gradients
    disabled in the checkpoint as this can result in subtle bugs where users don't
    realize that the model is frozen while finetuning.
    """
    out = tmp_path / "out"
    data = tmp_path / "data"
    helpers.create_images(image_dir=data, n=10)

    train.train(
        out=out,
        data=data,
        model="torchvision/resnet18",
        method="dino",
        batch_size=4,
        num_workers=2,
        epochs=1,
        devices=1,
    )
    ckpt_path = out / "checkpoints" / "last.ckpt"
    ckpt = Checkpoint.from_path(checkpoint=ckpt_path)
    for param in ckpt.lightly_train.models.model.parameters():
        assert param.requires_grad
