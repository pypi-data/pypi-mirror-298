# class_sz_data/data_retriever.py
import requests
import zipfile
import os
import io
import shutil

def get_data_from_class_sz_repo(path_to_local_repo):
    """
    Downloads the class_sz repository from GitHub and copies
    selected directories (bbn and class_sz_auxiliary_files/includes)
    to a specified local directory.

    Args:
        path_to_local_repo (str): The local path where the class-sz directories should be copied.
    """
    # GitHub repository URL for the ZIP file
    repo_url = "https://github.com/CLASS-SZ/class_sz/archive/refs/heads/main.zip"

    # Download the ZIP file from GitHub
    response = requests.get(repo_url)
    if response.status_code == 200:
        print("Repository downloaded successfully.")
        
        # Unzip the downloaded repository
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("./")

        # Define paths based on the unzipped repository structure
        repo_dir = 'class_sz-master'
        subdirs_to_copy = ['class-sz/bbn', 'class-sz/class_sz_auxiliary_files/includes']

        # Ensure the destination directory exists
        destination_class_sz = os.path.join(path_to_local_repo, 'class_sz')
        os.makedirs(destination_class_sz, exist_ok=True)

        # Copy the required subdirectories while preserving the structure
        for subdir in subdirs_to_copy:
            src = os.path.join(repo_dir, subdir)
            dest = os.path.join(destination_class_sz, subdir)
            shutil.copytree(src, dest, dirs_exist_ok=True)

        print(f"Selected directories from class-sz/ have been copied to {path_to_local_repo}.")
    else:
        print(f"Failed to download the repository. Status code: {response.status_code}")
