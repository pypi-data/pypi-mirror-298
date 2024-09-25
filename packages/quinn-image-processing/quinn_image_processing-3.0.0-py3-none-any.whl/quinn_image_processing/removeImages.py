import os
from PIL import Image

def is_corner_white_or_transparent(pixel, image_mode):
    """
    Check if a given pixel is white or transparent.
    
    Args:
        pixel (tuple): The pixel to check.
        image_mode (str): The mode of the image (e.g., 'RGB', 'RGBA').

    Returns:
        bool: True if the pixel is white or transparent, False otherwise.
    """
    if image_mode == 'RGBA':
        # Check for transparency (alpha = 0)
        return pixel[3] == 0 or (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255)
    elif image_mode == 'RGB':
        # Check for white in RGB mode
        return pixel == (255, 255, 255)
    return False

def should_delete_image(image):
    """
    Check if all four corners of the image are not white or transparent.
    
    Args:
        image (PIL.Image.Image): The image to check.

    Returns:
        bool: True if the image should be deleted, False otherwise.
    """
    width, height = image.size

    # Get the corner pixels
    top_left = image.getpixel((0, 0))
    top_right = image.getpixel((width - 1, 0))
    bottom_left = image.getpixel((0, height - 1))
    bottom_right = image.getpixel((width - 1, height - 1))
    
    # Check if all corners are white or transparent
    return (
        is_corner_white_or_transparent(top_left, image.mode) and
        is_corner_white_or_transparent(top_right, image.mode) and
        is_corner_white_or_transparent(bottom_left, image.mode) and
        is_corner_white_or_transparent(bottom_right, image.mode)
    )

def delete_non_focused_images(source_directory):
    """
    Iterate through all images in a directory and delete images where
    all four corners are not white or transparent.

    Args:
        source_directory (str): The directory to search for images.
    """
    supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    
    # Walk through all subdirectories and process images
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip files that don't have supported image extensions
            if filename.lower().endswith(supported_extensions):
                try:
                    with Image.open(file_path) as img:
                        # Check if the image should be deleted based on the four corners
                        if should_delete_image(img):
                            print(f"Deleting {filename} (corners are not all white or transparent)")
                            os.remove(file_path)
                        else:
                            print(f"Keeping {filename} (corners are all white or transparent)")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def main():
    # Get the source directory from the user
    source_directory = input("Enter the directory containing images: ").strip()
    
    # Run the function to delete images based on the four corners check
    delete_non_focused_images(source_directory)

if __name__ == "__main__":
    main()
