import os
from PIL import Image

# Resize and crop the image in multiple ways (top-left, bottom-right, center)
def resize_and_crop_image(image_path, max_size, output_directory, enable_top_left_crop, enable_bottom_right_crop, enable_center_crop, skip_non_white_or_transparent, save_as_jpg):
    """
    Resize and crop the image into selected versions (top-left, bottom-right, center).
    Replace any transparent pixels with white.
    
    Args:
        image_path (str): The file path of the image to process.
        max_size (int): The size of the resulting cropped image.
        output_directory (str): The directory to save the processed images.
        enable_top_left_crop (bool): Enable cropping from the top-left.
        enable_bottom_right_crop (bool): Enable cropping from the bottom-right.
        enable_center_crop (bool): Enable cropping from the center.
        skip_non_white_or_transparent (bool): If True, skip images where the top-left pixel is not white or transparent.
        save_as_jpg (bool): If True, save the cropped images as .jpg files.
    """
    try:
        with Image.open(image_path) as img:
            if skip_non_white_or_transparent and not should_process_image(img):
                print(f"Skipping {os.path.basename(image_path)} (top-left pixel is not white or transparent)")
                return
            
            original_width, original_height = img.size
            ratio = max(max_size / original_width, max_size / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Top-left crop
            if enable_top_left_crop:
                print(f"Processing top-left crop for {os.path.basename(image_path)}...")
                top_left_crop = resized_img.crop((0, 0, max_size, max_size))
                top_left_crop = replace_transparent_pixels(top_left_crop)
                save_cropped_image(top_left_crop, image_path, output_directory, "top_left", max_size, save_as_jpg)

            # Bottom-right crop
            if enable_bottom_right_crop:
                print(f"Processing bottom-right crop for {os.path.basename(image_path)}...")
                bottom_right_crop = resized_img.crop((new_width - max_size, new_height - max_size, new_width, new_height))
                bottom_right_crop = replace_transparent_pixels(bottom_right_crop)
                save_cropped_image(bottom_right_crop, image_path, output_directory, "bottom_right", max_size, save_as_jpg)

            # Center crop
            if enable_center_crop:
                print(f"Processing center crop for {os.path.basename(image_path)}...")
                left = (new_width - max_size) // 2
                top = (new_height - max_size) // 2
                center_crop = resized_img.crop((left, top, left + max_size, top + max_size))
                center_crop = replace_transparent_pixels(center_crop)
                save_cropped_image(center_crop, image_path, output_directory, "center", max_size, save_as_jpg)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def resize_and_pad_image(image_path, max_size, output_directory, skip_non_white_or_transparent, save_as_jpg):
    """
    Resize an image so that the larger dimension matches max_size (e.g., 2000 pixels),
    while maintaining the original aspect ratio. Then, pad the image with white to
    make it max_size x max_size pixels. For PNGs with transparent pixels, fill those areas with white.
    
    Args:
        image_path (str): The file path of the image to process.
        max_size (int): The size of the resulting padded image.
        output_directory (str): The directory to save the processed images.
        skip_non_white_or_transparent (bool): If True, skip images where the top-left pixel is not white or transparent.
        save_as_jpg (bool): If True, save the padded images as .jpg files.
    """
    try:
        with Image.open(image_path) as img:
            if skip_non_white_or_transparent and not should_process_image(img):
                print(f"Skipping {os.path.basename(image_path)} (top-left pixel is not white or transparent)")
                return

            # Convert transparent areas in PNG to white
            if img.mode == "RGBA":
                img = convert_transparent_to_white(img)

            # Get original dimensions
            original_width, original_height = img.size

            # Calculate the ratio for resizing
            if original_width > original_height:
                ratio = max_size / original_width
            else:
                ratio = max_size / original_height

            # Calculate new dimensions
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a new image with a white background
            new_image = Image.new("RGB", (max_size, max_size), (255, 255, 255))

            # Calculate position to center the resized image
            paste_position = ((max_size - new_width) // 2, (max_size - new_height) // 2)

            # Paste the resized image onto the white square background
            new_image.paste(resized_img, paste_position)

            # Create output path and preserve subdirectory structure
            save_padded_image(new_image, image_path, output_directory, max_size, save_as_jpg)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def save_cropped_image(cropped_img, image_path, output_directory, crop_type, max_size, save_as_jpg):
    """
    Save the cropped image to the specified output directory.
    
    Args:
        cropped_img (PIL.Image.Image): The cropped image to save.
        image_path (str): The original image file path.
        output_directory (str): The directory to save the image.
        crop_type (str): Type of crop (top_left, bottom_right, center).
        max_size (int): The max size for the cropped image.
        save_as_jpg (bool): If True, save the image as .jpg.
    """
    try:
        filename, ext = os.path.splitext(os.path.basename(image_path))
        if save_as_jpg:
            output_filename = f"{filename}_{crop_type}_{max_size}x{max_size}.jpg"
            output_path = os.path.join(output_directory, output_filename)
            cropped_img = cropped_img.convert("RGB")  # Ensure image is in RGB mode before saving as JPEG
            cropped_img.save(output_path, "JPEG")
        else:
            output_filename = f"{filename}_{crop_type}_{max_size}x{max_size}{ext}"
            output_path = os.path.join(output_directory, output_filename)
            cropped_img.save(output_path)

        print(f"Saved {output_filename} to {output_path}")

    except Exception as e:
        print(f"Error saving cropped image: {e}")

def save_padded_image(new_image, image_path, output_directory, max_size, save_as_jpg):
    """
    Save the padded image to the specified output directory.
    
    Args:
        new_image (PIL.Image.Image): The padded image to save.
        image_path (str): The original image file path.
        output_directory (str): The directory to save the image.
        max_size (int): The max size for the padded image.
        save_as_jpg (bool): If True, save the image as .jpg.
    """
    try:
        filename, ext = os.path.splitext(os.path.basename(image_path))
        if save_as_jpg:
            output_filename = f"{filename}_padded_{max_size}x{max_size}.jpg"
            output_path = os.path.join(output_directory, output_filename)
            new_image.save(output_path, "JPEG")
        else:
            output_filename = f"{filename}_padded_{max_size}x{max_size}{ext}"
            output_path = os.path.join(output_directory, output_filename)
            new_image.save(output_path)

        print(f"Saved padded image to {output_path}")

    except Exception as e:
        print(f"Error saving padded image: {e}")

def should_process_image(image):
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

def replace_transparent_pixels(image):
    """
    Replace transparent pixels in an image with white. 
    Convert from RGBA to RGB if the image has transparency.
    """
    if image.mode in ("RGBA", "LA"):  # Check for transparency
        return convert_transparent_to_white(image)
    return image

def convert_transparent_to_white(image):
    """
    Convert an RGBA image (with transparency) to RGB, filling transparent pixels with white.
    """
    # Create a white background image
    background = Image.new("RGB", image.size, (255, 255, 255))
    
    # Paste the image on top of the white background, using the alpha channel as a mask
    background.paste(image, mask=image.split()[3])  # Use the alpha channel as the mask
    
    return background

def resize_images_in_directory_for_padding(directory, max_size, output_directory, skip_non_white_or_transparent, save_as_jpg):
    """
    Resizes all image files in the given directory and its subdirectories
    so that the largest dimension matches max_size and pads them to make them max_size x max_size pixels.
    PNG images with transparent pixels will have those pixels filled with white.
    
    Args:
        directory (str): Directory containing images to process.
        max_size (int): The maximum size for the largest dimension of the resized images.
        output_directory (str): Directory to save the processed images.
        skip_non_white_or_transparent (bool): If True, skip images where the top-left pixel is not white or transparent.
        save_as_jpg (bool): If True, save the padded images as .jpg files.
    """
    supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

    # Walk through all subdirectories and process images
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip files with "_Generated_" in the path
            if "_Generated_" in file_path:
                print(f"Skipping {file_path} (contains '_Generated_')")
                continue

            if filename.lower().endswith(supported_extensions):
                try:
                    # Call resize_and_pad_image with the skip_non_white_or_transparent parameter
                    resize_and_pad_image(file_path, max_size, output_directory, skip_non_white_or_transparent, save_as_jpg)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def get_user_input():
    """
    Get user input for max image size for both crops and padding.
    """
    max_size = int(input("Enter the maximum size for the larger dimension (default is 2000): ") or 2000)
    return max_size

def main():
    # Directory containing the images
    image_directory = input("Enter the directory containing the images: ").strip()

    # Get user input for max image size
    max_image_size = get_user_input()

    # Ask the user for the folder name for processed images
    processed_folder_name = input("Enter a name for the processed images folder (default is 'ProcessedImages'): ").strip() or "ProcessedImages"
    processed_folder_name += '_Generated_'
    
    # Create output directory for all processed images
    output_directory = os.path.join(image_directory, processed_folder_name)
    os.makedirs(output_directory, exist_ok=True)

    # Ask the user which crop options to enable
    enable_top_left_crop = input("Do you want to enable Top-Left Crop? (y/n): ").strip().lower() == 'y'
    enable_bottom_right_crop = input("Do you want to enable Bottom-Right Crop? (y/n): ").strip().lower() == 'y'
    enable_center_crop = input("Do you want to enable Center Crop? (y/n): ").strip().lower() == 'y'
    
    # Ask if Resize and Pad is enabled
    enable_resize_and_pad = input("Do you want to enable Resize and Pad? (y/n): ").strip().lower() == 'y'

    # Ask the user if they want to skip images where the top-left pixel is not white or transparent
    skip_non_white_or_transparent = input("Do you want to skip images where the top-left pixel is not white or transparent? (y/n): ").strip().lower() == 'y'

    # Ask the user if they want to save all processed images as .jpg
    save_as_jpg = input("Do you want to save all processed images as .jpg files? (y/n): ").strip().lower() == 'y'

    # Run Resize and Crop (top-left, bottom-right, center) if any crop option is enabled
    if enable_top_left_crop or enable_bottom_right_crop or enable_center_crop:
        print("Running Resize and Crop...")
        resize_images_in_directory_for_crops(
            image_directory, 
            max_image_size, 
            output_directory, 
            enable_top_left_crop, 
            enable_bottom_right_crop, 
            enable_center_crop,
            skip_non_white_or_transparent,  # Pass the new parameter here
            save_as_jpg  # Pass the new save_as_jpg parameter
        )
    else:
        print("Skipping Resize and Crop...")

    # Run Resize and Pad (with white background) if enabled
    if enable_resize_and_pad:
        print("Running Resize and Pad...")
        resize_images_in_directory_for_padding(image_directory, max_image_size, output_directory, skip_non_white_or_transparent, save_as_jpg)  # Pass the new parameter here
    else:
        print("Skipping Resize and Pad...")

if __name__ == "__main__":
    main()
