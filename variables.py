import os

working_dir = os.getcwd()
dotenv_path =  os.path.join(working_dir, ".env") 
gitlab_url = "gitlab.com"

with open(os.getenv("SOURCE_TOKEN"), "r") as file:
    source_token = file.readline()
with open(os.getenv("DESTINATION_TOKEN"), "r") as file:
    destination_token = file.readline()
source_namespace = os.getenv("SOURCE_NAMESPACE")
destination_namespace = os.getenv("DESTINATION_NAMESPACE")

destination_namespace_id_mapping = {
    # Add the name of the source group namespace associated with the destination group namespace id
    # "sourcenamespacename : destinationnamespaceid"
}