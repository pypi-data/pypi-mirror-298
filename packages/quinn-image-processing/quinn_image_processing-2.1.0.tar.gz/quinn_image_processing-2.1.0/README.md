# My Image Processing Package

**My Image Processing Package** is a simple Python tool designed to perform basic image processing tasks, such as cropping and padding images. It allows you to resize and crop images to specific dimensions and fill transparent pixels with a white background, making your image dimensions uniform.

## Features

- **Resize and Crop Images**: Automatically resize images while maintaining aspect ratio and crop them to different positions (top-left, bottom-right, or center).
- **Padding Images**: Add white padding around images to ensure they are square, preserving the aspect ratio of the original image.
- **Handles Transparent Pixels**: Automatically replace any transparent pixels in PNG images with white.

## Installation

You can install this package using `pip`:

```bash
pip install quinn_image_processing

Update the PATH variable as needed, based on the warning given by pip:
WARNING: The scripts overlay-images.exe and square-images.exe are installed in 'SCRIPTLOCATION' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

$env:PATH += ';SCRIPTLOCATION'

