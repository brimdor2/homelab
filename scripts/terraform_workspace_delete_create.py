import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Terraform.io API token
TERRAFORM_IO_API_TOKEN = os.environ.get("TERRAFORM_IO_API_TOKEN")
if TERRAFORM_IO_API_TOKEN is None or TERRAFORM_IO_API_TOKEN.strip() == "":
    TERRAFORM_IO_API_TOKEN = input("Enter Terraform.io API Token: ")
    os.environ["TERRAFORM_IO_API_TOKEN"] = TERRAFORM_IO_API_TOKEN
    with open(".env", "a") as env_file:
        env_file.write("TERRAFORM_IO_API_TOKEN={}\n".format(TERRAFORM_IO_API_TOKEN))

# Get the OAuth token ID
TERRAFORM_OAUTH_TOKEN_ID = os.environ.get("TERRAFORM_OAUTH_TOKEN_ID")
if TERRAFORM_OAUTH_TOKEN_ID is None or TERRAFORM_OAUTH_TOKEN_ID.strip() == "":
    TERRAFORM_OAUTH_TOKEN_ID = input("Enter Terraform OAuth Token ID: ")
    os.environ["TERRAFORM_OAUTH_TOKEN_ID"] = TERRAFORM_OAUTH_TOKEN_ID
    with open(".env", "a") as env_file:
        env_file.write("TERRAFORM_OAUTH_TOKEN_ID={}\n".format(TERRAFORM_OAUTH_TOKEN_ID))

# Get the VCS Identifier
VCS_IDENTIFIER = os.environ.get("VCS_IDENTIFIER")
if VCS_IDENTIFIER is None or VCS_IDENTIFIER.strip() == "":
    VCS_IDENTIFIER = input("Enter VCS Identifier (ex. github_username/repo): ")
    os.environ["VCS_IDENTIFIER"] = VCS_IDENTIFIER
    with open(".env", "a") as env_file:
        env_file.write("VCS_IDENTIFIER={}\n".format(VCS_IDENTIFIER))

# Get the repository token
REPO_TOKEN = os.environ.get("REPO_TOKEN")
if REPO_TOKEN is None or REPO_TOKEN.strip() == "":
    REPO_TOKEN = input("Enter repository token: ")
    os.environ["REPO_TOKEN"] = REPO_TOKEN
    with open(".env", "a") as env_file:
        env_file.write("REPO_TOKEN={}\n".format(REPO_TOKEN))

# Get the organization
ORGANIZATION = os.environ.get("ORGANIZATION")
if ORGANIZATION is None or ORGANIZATION.strip() == "":
    ORGANIZATION = input("Enter organization: ")
    os.environ["ORGANIZATION"] = ORGANIZATION
    with open(".env", "a") as env_file:
        env_file.write("ORGANIZATION={}\n".format(ORGANIZATION))

# Check if the workspace exists
url = "https://app.terraform.io/api/v2/organizations/{}/workspaces".format(ORGANIZATION)
headers = {
    "Authorization": "Bearer {}".format(TERRAFORM_IO_API_TOKEN),
    "Content-Type": "application/vnd.api+json"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    workspace_name = "homelab-external"
    workspaces = response.json().get("data")
    for workspace in workspaces:
        if workspace["attributes"]["name"] == workspace_name:
            print("Workspace 'homelab-external' already exists.")
            delete_confirmation = input("Do you want to delete it? (yes/no): ")
            if delete_confirmation.lower() == "yes":
                print("Deleting workspace 'homelab-external'...")
                delete_url = "https://app.terraform.io/api/v2/organizations/{}/workspaces/{}".format(ORGANIZATION, workspace_name)
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 204:
                    print("Workspace 'homelab-external' deleted successfully")
                else:
                    print("Error deleting workspace: {}".format(delete_response.status_code))
            else:
                print("Cancelling deletion.")
                exit()
else:
    print("No homelab-external workspace exists.")

# Create a new workspace
create_url = "https://app.terraform.io/api/v2/organizations/{}/workspaces".format(ORGANIZATION)
create_payload = {
    "data": {
        "attributes": {
            "name": "homelab-external",
            "execution-mode": "local",
            "vcs-repo": {
                "identifier": VCS_IDENTIFIER,
                "oauth-token-id": TERRAFORM_OAUTH_TOKEN_ID,
                "branch": "main"
            }
        },
        "type": "workspaces"
    }
}

create_response = requests.post(create_url, headers=headers, json=create_payload)

if create_response.status_code == 201:
    print("Workspace 'homelab-external' created successfully")
else:
    print("Error creating workspace: {}".format(create_response.status_code))
