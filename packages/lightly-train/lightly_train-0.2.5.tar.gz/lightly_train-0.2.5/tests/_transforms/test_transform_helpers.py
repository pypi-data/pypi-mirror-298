#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import pytest

from lightly_train._transforms import transform_helpers
from lightly_train._transforms.transform import MethodTransformArgs, NormalizeArgs
from lightly_train.errors import ConfigUnknownKeyError, ConfigValidationError


@pytest.mark.parametrize(
    "transform_dict, expected_result",
    [
        # Test case for default empty dictionary
        ({}, MethodTransformArgs()),
        # Test case for None input
        (None, MethodTransformArgs()),
        # Test case for user config
        (
            {"normalize": {"mean": (0.5, 0.5, 0.5), "std": (0.5, 0.5, 0.5)}},
            MethodTransformArgs(
                normalize=NormalizeArgs(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
            ),
        ),
    ],
)
def test_validate_transform_args__success(transform_dict, expected_result) -> None:
    transform_args = transform_helpers.validate_transform_args(
        transform_dict, default_args=MethodTransformArgs()
    )
    # The instance check look unnecessary, but is actually needed. The reason is that
    # MethodTransformArgs() == omegaconf.create(MethodTransformArgs), but the latter is
    # an instance of a DictConfig, not of MethodTransformArgs.
    assert isinstance(transform_args, MethodTransformArgs)

    # TODO(Malte, 09/24): Improve assertion once we switched to pydantic.
    # OmegaConf wrongly converts tuples to lists, see https://github.com/omry/omegaconf/issues/392
    # Thus 'assert transform_args == expected_result' fails currently.
    assert (
        transform_args.random_flip.horizontal_prob
        == expected_result.random_flip.horizontal_prob
    )


@pytest.mark.parametrize(
    "transform_dict, expected_exception, expected_message",
    [
        # Test case for wrong argument name (top-level)
        (
            {"nonexisting_arg": {"any_arg": 5}},
            ConfigUnknownKeyError,
            "Unknown key in config: 'nonexisting_arg'",
        ),
        # Test case for wrong argument name (nested)
        (
            {"normalize": {"mean": (0.5, 0.5, 0.5), "std": (0.5, 0.5, 0.5), "out": 5}},
            ConfigUnknownKeyError,
            "Unknown key in config: 'normalize.out'",
        ),
        # Test case for wrong argument type
        (
            {"normalize": True},
            ConfigValidationError,  # noqa: F821
            "Merge error: bool is not a subclass of NormalizeArgs. value: True",
        ),
    ],
)
def test_validate_transform_args__failure(
    transform_dict, expected_exception, expected_message
) -> None:
    with pytest.raises(expected_exception, match=expected_message):
        transform_helpers.validate_transform_args(
            transform_dict, default_args=MethodTransformArgs()
        )
