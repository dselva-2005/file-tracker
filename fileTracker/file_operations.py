import shutil
import psutil
import os
from pathlib import Path

def rename_folder_with_pathlib(old_name, new_name):
    try:
        path = Path(old_name)
        path.rename(new_name)
        print(f"Folder renamed from '{old_name}' to '{new_name}' successfully.")
    except FileNotFoundError:
        print(f"The folder '{old_name}' was not found.")
    except PermissionError:
        print(f"You don't have permission to rename '{old_name}'.")
    except Exception as e:
        print(f"Error renaming folder: {e}")


def create_file_in_folder(file_path):
    # Create any intermediate directories if they don't exist
    folder = os.path.dirname(file_path)
    os.makedirs(folder, exist_ok=True)

    # Create and open the file
    with open(file_path, 'w'):
        pass  # Write content to the file

    print(f"File '{file_path}' created successfully!")

def create_folder_with_pathlib(folder_path:Path):
    path = folder_path
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully!")
    except FileExistsError:
        print(f"Folder '{folder_path}' already exists!")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_folder_with_pathlib(folder_path):
    """Deletes a folder and its contents using pathlib and shutil."""
    path = Path(folder_path)
    if path.exists() and path.is_dir():
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully!")
    else:
        print(f"Folder '{folder_path}' does not exist or is not a directory.")

def is_folder_accessible(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb+'):  # Try opening in read-write mode
                    pass
            except PermissionError:
                return False  # File is being accessed by another program
    return True

def check_usb():
    # Iterate over all the disk partitions
    for partition in psutil.disk_partitions():
        # Check if the device is a removable USB device
        if 'removable' in partition.opts:
            return True
    return False

def copy_file(source, destination):
    """
    Copies a file from source to destination.
    
    Args:
        source (str): Path to the source file.
        destination (str): Path to the destination file or directory.
    """
    try:
        if source.stat().st_size == destination.stat().st_size:
            return
        shutil.copy(source, destination)
        print(f"File copied from '{source}' to '{destination}' successfully!")
    except FileNotFoundError:
        print(f"Source file '{source}' does not exist!")
    except PermissionError:
        print("Permission denied! Check your access rights.")
    except Exception as e:
        print(f"An error occurred: {e}")

def copy_set_file(path,source,destination):
    base_path = Path(source)
    source_path = Path(path)
    relative_path = source_path.relative_to(base_path)
    destination_path = Path(destination) / relative_path
    if source_path.exists() :
        copy_file(source_path,destination_path)

def rename_file(old_name:Path, new_name):
    try:
        # Create Path object for the file
        file_path = old_name
        # Rename the file
        if not old_name.suffix:
            return
        
        file_path.rename(new_name)
        print(f"File renamed from '{old_name}' to '{new_name}' successfully.")
    except FileNotFoundError:
        print(f"The file '{old_name}' was not found.")
    except PermissionError:
        print(f"You don't have permission to rename '{old_name}'.")
    except Exception as e:
        print(f"Error renaming file: {e}")

def rename_set_file(path, source, destination):
    base_path = Path(source)
    previous_name = Path(path[0])
    new_name = Path(path[1])
    relative_previous_path = previous_name.relative_to(base_path)
    relative_new_path = new_name.relative_to(base_path)
    destination_path = Path(destination)
    full_previous_path = destination_path/relative_previous_path
    new_destination = destination_path/relative_new_path
    if full_previous_path.is_dir():
        rename_folder_with_pathlib(destination_path/relative_previous_path, new_destination)
    else:
        rename_file(destination_path/relative_previous_path, new_destination)
        try:
            if new_destination.stat().st_size == 0:
                copy_file(new_name,new_destination)
        except FileNotFoundError:
            pass

def delete_file(file_path):
    """Deletes a file."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully!")
    else:
        print(f"File '{file_path}' does not exist!")

def delete_file_set(path,source,destination):
    base_path = Path(source)
    source_path = Path(path)
    relative_path = source_path.relative_to(base_path)
    destination_path = Path(destination) / relative_path
    if destination_path.is_dir():
        delete_folder_with_pathlib(destination_path)
    else:
        try:
            if '.pub' in str(destination_path) and source_path.exists():
                pass
            else:
                delete_file(destination_path)
        except FileNotFoundError:
            pass

def create_file(file_path):
    """Creates a file with the given content."""
    if os.path.exists(file_path):
        print(f"File '{file_path}' already exists!")
    else:
        with open(file_path, 'w'):
            pass
        print(f"File '{file_path}' created successfully!")

def create_file_set(path,source,destination):
    base_path = Path(source)
    source_path = Path(path)
    relative_path = source_path.relative_to(base_path)
    destination_path = Path(destination) / relative_path
    if source_path.is_dir():
            create_folder_with_pathlib(destination_path)
    elif not source_path.suffix:
        pass
    else:
        try:
            create_file(destination_path)
            if destination_path.stat().st_size == 0:
                copy_file(source_path,destination_path)
        except FileNotFoundError:
            create_file_in_folder(destination_path)