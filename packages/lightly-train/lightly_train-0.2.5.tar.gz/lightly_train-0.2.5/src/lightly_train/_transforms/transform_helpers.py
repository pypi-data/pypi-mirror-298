#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Any

from omegaconf import OmegaConf

from lightly_train._configs import validate
from lightly_train._transforms.transform import MethodTransformArgs


def validate_transform_args(
    transform_dict: dict[str, Any] | None, default_args: MethodTransformArgs
) -> MethodTransformArgs:
    transform_dictconfig = OmegaConf.create(
        {} if transform_dict is None else transform_dict
    )
    transform_dictconfig = validate.validate_dictconfig(
        transform_dictconfig, default_args
    )
    transform_args = OmegaConf.to_object(transform_dictconfig)
    assert isinstance(transform_args, MethodTransformArgs)  # make mypy happy
    return transform_args
