
# GitLab cloner

The purpose of this script, fully containerized via docker, and ideally used with GitLab pipelines is to transfer the source files of a GitLab project to a parallel group each time a tag is created, so that there are two separate environments and thus access and modification can be limited. The source files are uploaded to the clone group via commits whose name matches that of the last tag of the source project, consequently, in the clone group, it will only be possible to see the differences between one version and another, thus hiding all intermediate commits.

## How it works
Whenever a tag is created in a GitLab project with pipelines laced with this script, it is checked to see if the project in question exists in the clone group, and if not, it is created by copying exactly the name, description, and features of the original project. At this point the files are transferred from one group to the other except for those in the .productiongitignore file which will be ignored instead (here you can insert any type of file you want to keep private), then a commit will be performed in the clone project which will have as name the tag just created in the source group
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SOURCE_NAMESPACE`

`DESTINATION_NAMESPACE`

You will also need to create two files called .source_token and .destination_token which will contain the GitLab tokens necessary to use its APIs


## Features

- The script can also run on Self-hosted instances of GitLab, all you have to do is change the variable `gitlab_url` in variables.py


