# pytorch-image

Minimalistic library designed to be an interface for the model input with a lightweight `Image` class.

```python
from my_model import MyModel, Image

image = Image.from_numpy(numpy_image)
predictions = model(image)
```

It also offers a simple interface for essential image operations such as loading, resizing, augmenting, and saving.

## Installation

```bash
pip install pytorch-image
```

```bash
poetry add pytorch-image
```

## Usage

```python
from pytorch_image import Image
import albumentations


image = Image.open("path/to/image.png")

image.augment(albumentations.HorizontalFlip())

image.torch()
```

```python
Image.from_numpy
Image.from_torch
Image.from_pil_image
Image.open
```
