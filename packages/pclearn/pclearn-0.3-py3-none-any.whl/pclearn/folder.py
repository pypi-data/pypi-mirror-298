import os
import shutil
from pathlib import Path

def build(folder_name):
    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")
    
    # Path to the current directory
    current_dir = Path(__file__).parent
    
    # List of .py files to copy
    py_files = ['Astar.py', 'BFS.py', 'DFS.py','DLS.py','dtree.py','emsemble.py','gbfs.py','IDDFS.py','knn.py','Navies.py','svm.py']  # Add the names of your .py files here
    
    # Iterate over the list of files and copy each to the new folder
    for file_name in py_files:
        source_file = current_dir / file_name
        destination_file = Path(folder_name) / file_name
        
        if source_file.exists():  # Check if the source file exists
            shutil.copy(source_file, destination_file)
            print(f"File '{file_name}' copied to '{folder_name}'.")
        else:
            print(f"File '{file_name}' not found in the package directory.")
