#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Dict,
    Generic,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
)

from lightly.transforms.utils import IMAGENET_NORMALIZE
from PIL.Image import Image as PILImage
from torch import Tensor

from lightly_train._configs.config import Config


@dataclass
class RandomResizeArgs(Config):
    min_scale: float = 0.08
    max_scale: float = 1.0


@dataclass
class RandomFlipArgs(Config):
    horizontal_prob: float = 0.5
    vertical_prob: float = 0.0


@dataclass
class NormalizeArgs(Config):
    mean: Tuple[float, float, float] = (
        IMAGENET_NORMALIZE["mean"][0],
        IMAGENET_NORMALIZE["mean"][1],
        IMAGENET_NORMALIZE["mean"][2],
    )
    std: Tuple[float, float, float] = (
        IMAGENET_NORMALIZE["std"][0],
        IMAGENET_NORMALIZE["std"][1],
        IMAGENET_NORMALIZE["std"][2],
    )

    def to_dict(self) -> Dict:
        return {
            "mean": self.mean,
            "std": self.std,
        }


@dataclass
class MethodTransformArgs(Config):
    image_size: Tuple[int, int] = (224, 224)
    random_resize: RandomResizeArgs = field(default_factory=RandomResizeArgs)
    random_flip: RandomFlipArgs = field(default_factory=RandomFlipArgs)
    random_gray_scale: float = 0.2
    normalize: Optional[NormalizeArgs] = field(default_factory=NormalizeArgs)


_T = TypeVar("_T", covariant=True)


class Transform(Generic[_T], Protocol):
    # `image` is a positional only argument because naming of the argument differs
    # between lightly, v1, and v2 transforms.
    def __call__(self, image: PILImage, /) -> _T: ...


class MethodTransform:
    transform_args: MethodTransformArgs
    transform: Transform[list[Tensor]]

    def __init__(self, transform_args: MethodTransformArgs):
        raise NotImplementedError

    def __call__(self, image: PILImage, /) -> list[Tensor]:
        return self.transform(image)

    @staticmethod
    def default_args() -> MethodTransformArgs:
        raise NotImplementedError
