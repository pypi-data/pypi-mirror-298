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
    """
    A class representing an image using PyTorch tensors.

    Attributes:
        data (torch.Tensor): Image data as a PyTorch tensor with shape (N, C, H, W), values between 0 and 1.
        path (Optional[Path]): Path to the image file, if applicable.
    """

    data: pt.Tensor
    path: Optional[Path] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def open(cls, path: Union[str, Path]) -> Image:
        """
        Open an image file and create an Image instance.

        Args:
            path (Union[str, Path]): Path to the image file.

        Returns:
            Image: An Image instance created from the file, with pixel values normalized to [0, 1] range.
        """
        return cls.from_pil_image(PIL.Image.open(path)).replace(path=Path(path))

    @classmethod
    def from_pil_image(cls, pil_image: PIL.Image.Image) -> Image:
        """
        Create an Image instance from a PIL Image.

        Args:
            pil_image (PIL.Image.Image): PIL Image object.

        Returns:
            Image: An Image instance created from the PIL Image, with pixel values normalized to [0, 1] range.
        """
        return cls.from_numpy(np.array(pil_image))

    @classmethod
    def from_numpy(cls, numpy_image: np.ndarray) -> Image:
        """
        Create an Image instance from a NumPy array.

        Args:
            numpy_image (np.ndarray): NumPy array representing the image (HWC format, uint8, values 0-255).

        Returns:
            Image: An Image instance created from the NumPy array, with pixel values normalized to [0, 1] range.

        Raises:
            ValueError: If the input array doesn't have 3 dimensions or isn't uint8.
        """
        if numpy_image.ndim != 3:
            raise ValueError("Expected dims HWC")

        if numpy_image.dtype != np.uint8:
            raise ValueError("Expected uint8")

        return cls(
            data=pt.from_numpy(numpy_image).float().div(255).permute(2, 0, 1)[None]
        )

    @classmethod
    def from_torch(cls, torch_tensor: pt.Tensor) -> Image:
        """
        Create an Image instance from a PyTorch tensor.

        Args:
            torch_tensor (torch.Tensor): PyTorch tensor representing the image (NCHW format, float, values 0-1).

        Returns:
            Image: An Image instance created from the PyTorch tensor.

        Raises:
            ValueError: If the input tensor doesn't have 4 dimensions or values outside [0, 1] range.
        """
        if torch_tensor.dim() != 4:
            raise ValueError("Expected 4 dimensions (NCHW)")

        return cls(data=torch_tensor)

    @classmethod
    def cat(cls, images: List[Image], dim: int = 0) -> Image:
        """
        Concatenate multiple Image instances.

        Args:
            images (List[Image]): List of Image instances to concatenate.
            dim (int, optional): Dimension along which to concatenate. Defaults to 0.

        Returns:
            Image: A new Image instance with concatenated data.
        """
        return cls(data=pt.cat([image.data for image in images], dim=dim))

    @property
    def shape(self) -> Tuple[int, int, int, int]:
        """
        Get the shape of the image data.

        Returns:
            Tuple[int, int, int, int]: Shape of the image data (N, C, H, W).
        """
        return self.data.shape

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[Image]:
        for data_ in self.data:
            yield Image(data=data_[None])

    def __getitem__(self, index: int) -> Image:
        return self.replace(data=self.data[index][None])

    def resize(
        self,
        shape: Tuple[int, int],
        mode: str = "bicubic",
        align_corners: Optional[bool] = None,
        antialias: Optional[bool] = None,
    ) -> Image:
        """
        Resize the image to the specified shape.

        Args:
            shape (Tuple[int, int]): Target shape (height, width).
            mode (str, optional): Interpolation mode. Defaults to "bicubic".
            align_corners (Optional[bool], optional): Align corners option. Defaults to None.
            antialias (Optional[bool], optional): Antialias option. Defaults to None.

        Returns:
            Image: A new Image instance with resized data.
        """
        return Image(
            data=F.interpolate(
                self.data,
                size=shape,
                mode=mode,
                align_corners=align_corners,
                antialias=antialias,
            )
        )

    def augment(self, augmenter: A.Compose) -> Image:
        """
        Apply augmentations to the image.

        Args:
            augmenter (A.Compose): Albumentations composition of augmentations.

        Returns:
            Image: A new Image instance with augmented data.
        """
        augmented = augmenter(image=self.numpy())
        return self.from_numpy(augmented["image"])

    def map(self, func: Callable[[torch.Tensor], torch.Tensor]) -> Image:
        """
        Apply a function to the image data.

        Args:
            func (Callable[[torch.Tensor], torch.Tensor]): Function to apply to the image data.

        Returns:
            Image: A new Image instance with transformed data.
        """
        return self.replace(data=func(self.data))

    def replace(self, **kwargs) -> Image:
        """
        Create a new Image instance with replaced attributes.

        Args:
            **kwargs: Attributes to replace.

        Returns:
            Image: A new Image instance with replaced attributes.
        """
        dict_ = self.model_dump()
        for key, value in kwargs.items():
            dict_[key] = value
        return Image(**dict_)

    def torch(self) -> torch.Tensor:
        """
        Get the image data as a PyTorch tensor.

        Returns:
            torch.Tensor: Image data as a PyTorch tensor.
        """
        return self.data

    def numpy(self) -> np.ndarray:
        """
        Get the image data as a NumPy array.

        Returns:
            np.ndarray: Image data as a NumPy array (HWC format, uint8).
        """
        return (self.data[0].permute(1, 2, 0).clamp(0, 1) * 255).byte().numpy()

    def representation(self) -> torch.Tensor:
        """
        Get a normalized representation of the image data.

        Returns:
            torch.Tensor: Normalized image data as a PyTorch tensor.
        """
        return self.data.float().clamp(0, 1)

    def save(self, path: Union[str, Path]) -> None:
        """
        Save the image to a file.

        Args:
            path (Union[str, Path]): Path to save the image.
        """
        self.pil_image().save(path)

    def pil_image(self) -> PIL.Image.Image:
        """
        Convert the image to a PIL Image.

        Returns:
            PIL.Image.Image: Image as a PIL Image object.
        """
        return PIL.Image.fromarray(self.numpy())

    def _repr_png_(self) -> bytes:
        """
        Get a PNG representation of the image for Jupyter notebook display.

        Returns:
            bytes: PNG representation of the image.
        """
        return self.pil_image()._repr_png_()
