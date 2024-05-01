# YOLOv5 Utils

## activations.py
This file contains implementations of various activation functions used in the YOLOv5 model. These activation functions include:
- SiLU (Sigmoid Linear Unit)
- GeLU (Gaussian Error Linear Unit)
- Hardswish
- Mish
- MemoryEfficientMish
- FReLU (Feature-wise Linear Unit)
- AconC and MetaAconC (Activate or Not)

These activation functions are utilized within the YOLOv5 model to introduce non-linearity and enhance the model's learning and expression capabilities.

## torch_utils.py
This file provides utility functions for PyTorch, used in the YOLOv5 project. Functions include:
- `torch_distributed_zero_first`: Decorator to synchronize distributed processes
- `date_modified`: Returns human-readable file modification date
- `git_describe`: Returns human-readable git description
- `select_device`: Selects the device (CPU or GPU) for computation
- `profile`: Profiles the speed, memory usage, and FLOPs of the model
- `is_parallel` and `de_parallel`: Check and de-parallelize a model if it's of type DP or DDP
- `initialize_weights`: Initializes weights of the model
- `find_modules`: Finds layer indices matching a given module class
- `sparsity` and `prune`: Computes and applies model sparsity
- `fuse_conv_and_bn`: Fuses convolution and batch normalization layers
- `model_info`: Prints information about the model including layer count, parameters, and FLOPs
- `scale_img`: Scales images by a given ratio while ensuring alignment to a grid
- `copy_attr`: Copies attributes from one object to another
- `EarlyStopping` and `ModelEMA`: Classes for early stopping and model exponential moving average

## datasets.py
This file contains dataloaders and dataset utilities for the YOLOv5 project. It includes functions for:
- Data augmentation
- Dataset creation and loading
- Handling image and video formats
- Exif data correction
- Hashing and data integrity checks
- Exif orientation correction for images
- Random cropping, flipping, and rotation of images
- Dataset class definitions for image and video datasets

## loss.py
The `loss.py` module contains custom loss functions utilized in the YOLOv5 project by Ultralytics. These loss functions are designed to optimize the model's performance during training by computing appropriate loss values for object detection tasks.

### Loss Functions Included:

1. **`BCEBlurWithLogitsLoss`**: A variation of the Binary Cross Entropy (BCE) with Logits loss, which reduces missing label effects.
   
2. **`FocalLoss`**: Implements the Focal Loss, which addresses class imbalance by focusing on hard examples and down-weights easy ones.

3. **`QFocalLoss`**: Quality Focal Loss, a variant of the Focal Loss with an emphasis on improving quality predictions.


## augmentations.py
This file contains image augmentation functions used to augment input images for training. It includes functions for HSV color-space augmentation, histogram equalization, replication, letterboxing, random perspective transformation, copy-paste augmentation, and image cutout. These augmentations help enhance the diversity and robustness of the training data.

## autoanchor.py
Auto-anchor utils for YOLOv5. This file provides functions for checking anchor fit to the dataset, re-computing anchors if necessary, and performing k-means clustering to evolve anchors from the training dataset. The `check_anchors()` function checks if the current anchors are a good fit to the dataset and re-computes them if needed. The `kmean_anchors()` function uses k-means clustering to evolve anchors from the dataset.

## general.py
Contains various utilities used in the YOLOv5 project by Ultralytics. Features include file operations, logging configuration, context managers, environment checks, data processing, and more.

## Setup

Use the following commands to set up the environment:

```bash
cd nms_rotated

# Install Dependencies in Editable Mode
pip install -v -e .

# Build the Package
python setup.py build
