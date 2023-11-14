import os
import shutil
import sys
import stat
    
def copy_folder(source_path : str, destination_path : str):
    """
    Copy all the files contained in the source path to the destination 
    path, ignoring the .git folder.
    """
    try:
        for item in os.listdir(source_path):
            source_item = os.path.join(source_path, item)
            destination_item = os.path.join(destination_path, item)
            
            if item != ".git":
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                elif item != ".gitignore":
                    shutil.copy2(source_item, destination_item)

        os.rename(os.path.join(destination_path, ".productiongitignore"), os.path.join(destination_path, ".gitignore"))
        
    except FileNotFoundError:
        raise ValueError("missing .productiongitignore file in the source project.")
    except Exception as e:
        raise ValueError(e)
    
def empty_folder(folder_path : str):
    """
    Delete all files and subfolders contained in the folder path, ignoring the .git folder.
    """
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if ".git" not in root:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if dir != ".git" and ".git/" not in dir_path:
                    print(dir_path)
                    shutil.rmtree(dir_path)
    except Exception as e:
        raise ValueError(e)
    
def exit_program():
    """
    Exit program throwing an error.
    """
    print("An error occured...")
    sys.exit(1)

def on_rm_error( func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE )
    os.unlink(path)
    
def prettify(latest_tag : str) -> str:
    """
    Get actual tag name.
    Example: release_5_0_0-4-ga986d3e -> release_5_0_0
    """
    index = latest_tag.rfind("-")
    if index != -1:
        truncated = latest_tag[:index].rfind("-")
    if truncated != -1:
        latest_tag_name = latest_tag[:truncated]
        return latest_tag_name
    else:
        raise ValueError("cannot parse project's latest tag")