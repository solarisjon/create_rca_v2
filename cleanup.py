import os
import shutil

# Function to clean and recreate the uploads directory
def clean_and_recreate_directory(directory_path: str) -> None:
    if not isinstance(directory_path, str):
        raise TypeError("The directory path must be a string.")
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)