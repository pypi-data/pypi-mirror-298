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
from image_compressor import load_image, plot_compressed_images

# Load an image and convert to grayscale
gray_image = load_image('path_to_your_image.jpg')

# Define the number of singular values to retain
k_values = [1, 5, 10, 20, 50]

# Visualize the compressed images
plot_compressed_images(gray_image, k_values)
```