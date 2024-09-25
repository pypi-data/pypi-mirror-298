import os
from datetime import datetime
from PIL import Image

def create_output_subdir(output_dir):
    """Creates a timestamped folder inside the specified output directory."""
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_subdir = os.path.join(output_dir, f"processed_{current_datetime}")
    os.makedirs(output_subdir, exist_ok=True)
    return output_subdir

def overlay_image(base_image_path, overlay_image_path, overlay_area_percentage, margin_percentage, output_subdir):
    """Processes an image by overlaying a resized image and saving it in the provided output directory."""
    
    # Open the base image and overlay image
    base_image = Image.open(base_image_path)
    overlay = Image.open(overlay_image_path)
    
    # Calculate the area of the base image
    base_width, base_height = base_image.size
    base_area = base_width * base_height
    
    # Calculate the target area for the overlay as a percentage of the base image's area
    target_overlay_area = base_area * (overlay_area_percentage / 100)
    
    # Get the original aspect ratio of the overlay
    overlay_width, overlay_height = overlay.size
    aspect_ratio = overlay_width / overlay_height
    
    # Calculate the new overlay dimensions based on the target area and maintain aspect ratio
    new_overlay_width = int((target_overlay_area * aspect_ratio) ** 0.5)
    new_overlay_height = int(new_overlay_width / aspect_ratio)
    
    # Calculate the margins (percentage of the base image size)
    margin_right = int(base_width * (margin_percentage / 100))
    margin_top = int(base_height * (margin_percentage / 100))  # Changed margin_bottom to margin_top
    
    # Check if the overlay dimensions plus the margins exceed the base image dimensions
    if new_overlay_width + margin_right > base_width or new_overlay_height + margin_top > base_height:
        # Scale down the overlay proportionally so that it fits with the margins
        scale_factor = min(
            (base_width - margin_right) / overlay_width,
            (base_height - margin_top) / overlay_height
        )
        new_overlay_width = int(overlay_width * scale_factor)
        new_overlay_height = int(overlay_height * scale_factor)
    
    # Resize the overlay using LANCZOS resampling
    resized_overlay = overlay.resize((new_overlay_width, new_overlay_height), Image.Resampling.LANCZOS)
    
    # Calculate the position for the overlay (from top-right corner)
    overlay_x = base_width - new_overlay_width - margin_right
    overlay_y = margin_top  # Changed to margin_top for top-right positioning
    
    # Create a copy of the base image to avoid modifying the original
    result_image = base_image.copy()
    
    # Paste the overlay onto the base image (with transparency handling if necessary)
    result_image.paste(resized_overlay, (overlay_x, overlay_y), resized_overlay)
    
    # Save the result to the provided output directory
    output_path = os.path.join(output_subdir, os.path.basename(base_image_path))
    result_image.save(output_path)

    print(f"Saved processed image to: {output_path}")

    print(f"Saved processed image to: {output_path}")

def process_images(input_dir, overlay_image_path, overlay_area_percentage, margin_percentage, output_dir):
    """Processes all images in the input directory and saves them in a single timestamped output directory."""
    
    # Create the timestamped output subdirectory (only once)
    output_subdir = create_output_subdir(output_dir)
    
    # Get list of image files from the input directory
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')  # Add more extensions as needed
    file_list = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]

    # Check if there are any image files to process
    if not file_list:
        print(f"No image files found in {input_dir}.")
        return

    # Process each image file found in the input directory
    for filename in file_list:
        image_path = os.path.join(input_dir, filename)
        try:
            # Call the overlay_image function to process the image and save it in the same output directory
            overlay_image(image_path, overlay_image_path, overlay_area_percentage, margin_percentage, output_subdir)
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

def main():
    """Main function to handle user input and run the script directly."""
    # Get user inputs
    input_dir = input("Enter the input image directory: ")
    output_dir = input("Enter the output image directory: ")
    overlay_image_path = input("Enter the path to the overlay image: ")
    
    # Ensure valid input for percentages
    while True:
        try:
            overlay_area_percentage = float(input("Enter the overlay area as a percentage of the base image area (0-100): "))
            if 0 <= overlay_area_percentage <= 100:
                break
            else:
                print("Please enter a number between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            margin_percentage = float(input("Enter the margin size as a percentage of the base image size (0-100): "))
            if 0 <= margin_percentage <= 100:
                break
            else:
                print("Please enter a number between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Call the function to process images
    process_images(input_dir, overlay_image_path, overlay_area_percentage, margin_percentage, output_dir)

# Allow script to be run directly
if __name__ == "__main__":
    main()
