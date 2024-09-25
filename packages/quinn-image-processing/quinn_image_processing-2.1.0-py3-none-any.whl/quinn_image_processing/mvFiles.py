import os
import shutil

def move_files(source_dir, destination_dir):
    """
    Move all files from the source directory to the destination directory.
    Overwrites files in the destination directory if they already exist.
    
    Args:
    source_dir (str): The source directory from which files are to be moved.
    destination_dir (str): The destination directory where files will be moved.
    """
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"The source directory '{source_dir}' does not exist.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"The destination directory '{destination_dir}' was created.")

    # Get a list of files in the source directory
    files = os.listdir(source_dir)
    if not files:
        print(f"No files found in the source directory '{source_dir}'.")
        return

    # Move each file from the source to the destination
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)

        # Ensure we're moving files, not directories
        if os.path.isfile(source_file):
            # Overwrite the file if it already exists
            shutil.move(source_file, destination_file)
            print(f"Moved and overwritten: {file}")
        else:
            print(f"Skipping directory: {file}")

    print("All files have been moved and overwritten if necessary.")

def main():
    # Get the source and destination directories from the user
    source_dir = input("Enter the path of the source directory: ")
    destination_dir = input("Enter the path of the destination directory: ")

    # Call the function to move files
    move_files(source_dir, destination_dir)

# Allow script to be run directly
if __name__ == "__main__":
    main()
