import os
import shutil
from pathlib import Path

def create_folder_with_pyfile(folder_name):
    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")
    
    # Path to the sample .py file within the package
    current_dir = Path(__file__).parent
    source_file = current_dir / 'ai.py'
    
    # Destination path inside the newly created folder
    destination_file = Path(folder_name) / 'ai.py'
    
    # Copy the file to the new folder
    shutil.copy(source_file, destination_file)
    print(f"File 'ai.py' copied to '{folder_name}'.")
