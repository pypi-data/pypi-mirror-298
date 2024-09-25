import os
import shutil

items = [
    "-ONA",
	"-SERPENT",
    "-MOMA",
    "-ALASKA",
    "-ARENA",
    "-RIBS",
    "-JOURNEY",
    "-SHELTERGAZEBO",
    "-IGLOO",
    "-CONE",
    "-GANESHA",
    "-SANZA",
    "-HOLIDAY"
]

# Get the source directory from the user
source_dir = input("Enter the path to the source directory: ")

# Define the target directory
target_dir = os.path.join(source_dir, "SPECIAL ORDER")

# Create the "SPECIAL ORDER" directory if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Iterate through items in the source directory
for filename in os.listdir(source_dir):
    file_path = os.path.join(source_dir, filename)

    # Convert file path and items to lowercase for case-insensitive comparison
    if any(item.lower() in file_path.lower() for item in items):
        # Move the file to the "SPECIAL ORDER" directory
        shutil.move(file_path, target_dir)
        print(f'Moved: {filename} to {target_dir}')

