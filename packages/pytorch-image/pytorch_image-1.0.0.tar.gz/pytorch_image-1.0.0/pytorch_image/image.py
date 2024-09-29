from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterator, List, Optional, Tuple, Union

import numpy as np
import PIL.Image
import torch as pt
import torch.nn.functional as F
from pydantic import BaseModel, ConfigDict

try:
    import albumentations as A
except ImportError:
    pass


class Image(BaseModel):
    data: pt.Tensor  # shape (N, C, H, W), between 0 and 1
    path: Optional[Path] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def open(cls, path: Union[str, Path]) -> Image:
        return cls.from_pil_image(PIL.Image.open(path)).replace(path=Path(path))

    @classmethod
    def from_pil_image(cls, pil_image: PIL.Image.Image) -> Image:
        return cls.from_numpy(np.array(pil_image))

    @classmethod
    def from_numpy(cls, numpy_image: np.ndarray) -> Image:
        if numpy_image.ndim != 3:
            raise ValueError("Expected dims HWC")

        if numpy_image.dtype != np.uint8:
            raise ValueError("Expected uint8")

        # Convert to float32 and normalize to [0, 1] range
        return cls(
            data=pt.from_numpy(numpy_image).float().div(255).permute(2, 0, 1)[None]
        )

    @classmethod
    def cat(cls, images: List[Image], dim=0) -> Image:
        return cls(data=pt.cat([image.data for image in images], dim=dim))

    @property
    def shape(self):
        return self.data.shape

    def __len__(self):
        return len(self.data)

    def __iter__(self) -> Iterator[Image]:
        for data_ in self.data:
            yield Image(data=data_[None])

    def __getitem__(self, index: int) -> Image:
        return self.replace(data=self.data[index][None])

    def resize(
        self,
        shape: Tuple[int, int],
        mode="bicubic",
        align_corners=None,
        antialias=None,
    ) -> Image:
        return Image(
            data=F.interpolate(
                self.data,
                size=shape,
                mode=mode,
                align_corners=align_corners,
                antialias=antialias,
            )
        )

    def augment(self, augmenter: A.Compose):
        augmented = augmenter(image=self.numpy())
        return self.from_numpy(augmented["image"])

    def map(self, func: Callable[[pt.Tensor], pt.Tensor]) -> Image:
        return self.replace(data=func(self.data))

    def replace(self, **kwargs) -> Image:
        dict_ = self.model_dump()
        for key, value in kwargs.items():
            dict_[key] = value
        return Image(**dict_)

    def torch(self) -> pt.Tensor:
        return self.data

    def numpy(self) -> np.ndarray:
        return (self.data[0].permute(1, 2, 0).clamp(0, 1) * 255).byte().numpy()

    def representation(self) -> pt.Tensor:
        return self.data.float().clamp(0, 1)

    def save(self, path: Union[str, Path]):
        self.pil_image().save(path)

    def pil_image(self) -> PIL.Image.Image:
        return PIL.Image.fromarray(self.numpy())

    def _repr_png_(self):
        return self.pil_image()._repr_png_()
