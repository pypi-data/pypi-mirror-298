import os
import shutil
from PIL import Image

def create_focused_images_directory(output_directory):
    """
    Create the 'Focused Images' directory if it doesn't exist.
    """
    focused_images_directory = os.path.join(output_directory, "Focused Images")
    os.makedirs(focused_images_directory, exist_ok=True)
    return focused_images_directory

def should_copy_image(image):
    """
    Check if the top-left pixel of the image is white or transparent.
    """
    top_left_pixel = image.getpixel((0, 0))
    
    # Check if image has an alpha channel (RGBA)
    if image.mode == 'RGBA':
        # Check for transparency (alpha = 0)
        return top_left_pixel[3] == 0
    # Check for white in RGB mode
    elif image.mode == 'RGB':
        return top_left_pixel == (255, 255, 255)
    
    return False

def copy_focused_images(source_directory, output_directory):
    """
    Copy images from the source directory to 'Focused Images' if the top-left pixel
    is white or transparent, maintaining the subdirectory structure, and ignoring
    files that contain "_Generated_" in their path.
    
    Args:
        source_directory (str): The directory to search for images.
        output_directory (str): The directory where 'Focused Images' folder will be created.
    """
    supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    
    # Create 'Focused Images' directory
    focused_images_directory = create_focused_images_directory(output_directory)
    
    # Walk through all subdirectories and process images
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip files that contain "_Generated_" in their path
            if "_Generated_" in file_path:
                print(f"Skipping {filename} (contains '_Generated_' in path)")
                continue

            # Skip files that don't have supported image extensions
            if filename.lower().endswith(supported_extensions):
                try:
                    with Image.open(file_path) as img:
                        # Check if the image should be copied based on the top-left pixel
                        if should_copy_image(img):
                            # Compute the relative path of the file to preserve subdirectory structure
                            relative_path = os.path.relpath(root, source_directory)
                            destination_directory = os.path.join(focused_images_directory, relative_path)

                            # Create the subdirectory in the destination if it doesn't exist
                            os.makedirs(destination_directory, exist_ok=True)

                            # Copy the image to the destination directory
                            destination_path = os.path.join(destination_directory, filename)
                            print(f"Copying {filename} to {destination_path}...")
                            shutil.copy(file_path, destination_path)
                        else:
                            print(f"Skipping {filename} (top-left pixel is not white or transparent)")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def main():
    # Get the source directory from the user
    source_directory = input("Enter the source directory containing images: ").strip()
    
    # Get the output directory from the user (where 'Focused Images' will be created)
    output_directory = input("Enter the directory where 'Focused Images' will be created: ").strip()
    
    # Run the function to copy images based on the top-left pixel check
    copy_focused_images(source_directory, output_directory)

if __name__ == "__main__":
    main()
