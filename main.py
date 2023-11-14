import git
import requests
import sys
import shutil
import os
import time

from utils import empty_folder, copy_folder, on_rm_error, exit_program, prettify
from variables import destination_namespace_id_mapping, working_dir, gitlab_url, source_token, destination_token, source_namespace, destination_namespace


def apply_changes(repo : git.Repo, tag_name : str):
    """
    Commit and push all the files contained in the repository, using
    tag name as commit message.
    """
    try:
        repo.git.execute(["git", "rm", "-r", "--cached", "."]) # Remove all the files from the tracking to make .gitignore retroactive
    except:
        pass
    finally:
        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "-m", tag_name])
        repo.git.execute(["git", "push", "origin"]) 
        print("Committed and pushed latest changes to destination repository.")

def clone_project(project_path : str):
    """
    Clone the source and destination repositories, copy the content 
    of the source to the destination repository, commit and push the 
    changes to the destination repository using the source latest tag
    as message.
    """
    
    source_url = f"https://oauth2:{source_token}@{gitlab_url}/{project_path}.git"
    destination_url = f"https://oauth2:{destination_token}@{gitlab_url}/{project_path}.git".replace(source_namespace, destination_namespace)
    
    try:
        local_path = os.path.join(working_dir, "localRepos") 
        local_source_path = os.path.join(local_path, "Source") 
        local_destination_path = os.path.join(local_path, "Destination") 

        os.mkdir(local_path)
        os.mkdir(local_source_path)
        os.mkdir(local_destination_path)

        source_repo = git.Repo.clone_from(source_url, local_source_path) # Clone source project to the local folder
        latest_tag_name = source_repo.git.describe("--tags") # Get the name of the latest tag of the source project
        if ("-" in latest_tag_name):
            latest_tag_name = prettify(latest_tag_name)
        destination_repo = git.Repo.clone_from(destination_url, local_destination_path) # Clone destination project to the local folder

        time.sleep(5)
        empty_folder(local_destination_path)
        copy_folder(local_source_path, local_destination_path)
        apply_changes(destination_repo, latest_tag_name)
    
    except Exception as e:
        print(f"An error occured: {e}")  
    
    finally:
        print("Deleting working folders...")
        shutil.rmtree(local_path, onexc=on_rm_error)
        print("Working folders deleted.")
    
def create_project(destination_namespace : str, project : dict) -> int:
    """
    Create new GitLab project in the destination namespace, copying all
    the project information from the source namespace.
    """
    creation_url = f"https://{gitlab_url}/api/v4/projects"
    headers = {
        "Private-Token" : destination_token
    }
    params = {
        "name" : project["name"],
        "description" : project["description"],
        "namespace_id" : destination_namespace,
        "visibility" : "private"
    }
    print("Creating project in the destination namespace.")
    response = requests.post(creation_url, params=params, 
                             headers=headers)
    return response.status_code
                
def main():

    source_path = sys.argv[1] # Get the project's path from the arguments
    source_headers = {
        "Private-Token" : source_token
    }
    destination_headers = {
        "Private-Token" : destination_token
    }
    source_path_encoded = source_path.replace("/", "%2f") # Encode the path for the API endpoint
    destination_path_encoded = source_path_encoded.replace(source_namespace, destination_namespace)
    response = requests.get(f"https://{gitlab_url}/api/v4/projects/{destination_path_encoded}", # Check if the project already exists
                            headers=destination_headers) 

    if (response.status_code == 404 and "Project Not Found" in response.text): # If the project doesn't exist, create it
        project = requests.get(f"https://{gitlab_url}/api/v4/projects/{source_path_encoded}", # Get the original project information
                               headers=source_headers).json() 
        destination_namespace_id = destination_namespace_id_mapping.get(project["namespace"]["path"]) # Get the corresponding project id of the destination namespace 
        status_code = create_project(destination_namespace_id, project) # Create project and retrieve the status of the operation

        if (int(status_code) != 201): # If there was an error creating the project, exit the program
            exit_program()

        print("Project created successfully.")
    else:
        print("The project already exists in the destination namespace, committing latest changes.")
    clone_project(source_path)

if __name__ == "__main__":
    # Check if the program was executed with at least an argument"
    if len(sys.argv) < 2:
        print("Missing argument.")
        sys.exit(1)
    main()