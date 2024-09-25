#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import dataclasses
import logging
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pytorch_lightning.loggers import Logger

from lightly_train._configs import validate
from lightly_train._loggers.jsonl import JSONLLogger
from lightly_train._loggers.logger_args import LoggerArgs
from lightly_train._loggers.tensorboard import TensorBoardLogger
from lightly_train._loggers.wandb import WandbLogger

try:
    import tensorboard
except ImportError:
    tensorboard = None

logger = logging.getLogger(__name__)


def validate_logger_args(loggers: dict[str, Any] | None) -> LoggerArgs:
    """Validates the logger arguments.

    The default loggers are:
    - JSONLLogger
    - TensorBoardLogger if tensorboard is installed
    """
    logger_dictconfig = OmegaConf.create({} if loggers is None else loggers)
    logger_dictconfig = validate.validate_dictconfig(logger_dictconfig, LoggerArgs)
    logger_args = OmegaConf.to_object(logger_dictconfig)
    assert isinstance(logger_args, LoggerArgs)  # make mypy happy
    return logger_args


def get_loggers(logger_args: LoggerArgs, out: Path) -> list[Logger]:
    """Get logger instances based on the provided configuration.

    All loggers are configured with the same output directory 'out'.

    Args:
        logger_args:
            Configuration for the loggers.
        out:
            Path to the output directory.

    Returns:
        List of loggers.
    """
    loggers: list[Logger] = []

    if logger_args.jsonl is not None:
        logger.debug(f"Using jsonl logger with args {logger_args.jsonl}")
        loggers.append(
            JSONLLogger(save_dir=out, **dataclasses.asdict(logger_args.jsonl))
        )
    if logger_args.tensorboard is not None:
        if tensorboard is None:
            logger.warning(
                "tensorboard is not installed. Skipping tensorboard logger.\n"
                "Please install tensorboard with 'pip install tensorboard'."
            )
        else:
            logger.debug(
                f"Using tensorboard logger with args {logger_args.tensorboard}"
            )
            loggers.append(
                TensorBoardLogger(
                    save_dir=out, **dataclasses.asdict(logger_args.tensorboard)
                )
            )
    if logger_args.wandb is not None:
        logger.debug(f"Using wandb logger with args {logger_args.wandb}")
        loggers.append(
            WandbLogger(save_dir=out, **dataclasses.asdict(logger_args.wandb))
        )

    logger.debug(f"Using loggers {[log.__class__.__name__ for log in loggers]}.")
    return loggers
