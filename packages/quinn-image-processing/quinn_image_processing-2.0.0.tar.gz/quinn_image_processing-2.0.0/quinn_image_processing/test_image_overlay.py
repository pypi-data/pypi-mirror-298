import os
from overlayScript import process_images  # Import the new process_images function from overlayScript.py

def test_run():
    # Hardcoded test inputs
    input_dir = r'C:\Users\brand\Pictures\testInput'
    output_dir = r'C:\Users\brand\Pictures\testOutput'
    overlay_image_path = r'C:\Users\brand\Desktop\image_manipulation\logo.png'
    overlay_area_percentage = 10  # Overlay area as a percentage of the base image area
    margin_percentage = 0  # Margin size as a percentage of the base image size

    # Call the process_images function to handle all the images and save them to a single timestamped folder
    process_images(input_dir, overlay_image_path, overlay_area_percentage, margin_percentage, output_dir)

if __name__ == '__main__':
    test_run()
