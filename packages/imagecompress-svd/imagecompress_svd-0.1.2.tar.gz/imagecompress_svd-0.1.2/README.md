# Image Compression

## Overview
`imagecompress_svd` is a Python package that compresses images using Singular Value Decomposition (SVD). It provides functions to convert RGB images to grayscale, compress images by retaining a specified number of singular values, and visualize the compressed images.

## Features
- Convert RGB images to grayscale.
- Compress images using SVD with adjustable singular values.
- Visualize the compressed images for different levels of compression.

## Installation

To install the package, first clone the repository or download the code, then navigate to the package directory and run:

```bash
pip install .
```

## Usage
```python
from imagecompress_svd import rgb2gray, plot_compressed_images
from PIL import Image
import numpy as np

# Load image and convert to grayscale
image = Image.open('your_image.jpg')
gray_image = rgb2gray(np.array(image))

# Define different k values for compression
k_values = [1, 2, 5, 10, 20, 50]

# Plot compressed images
plot_compressed_images(gray_image, k_values)
```