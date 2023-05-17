import requests

def delete_terraform_workspace(workspace_name):
    # Define your Terraform Cloud organization and API token
    organization = 'brimdor'
    api_token = '0ssyzIOnbsX0Fw.atlasv1.XwlvYZ7jdSsDZ4YypLc4Vz4EGrS3aQPKktBWRps2bFDVyJl2SWOipEpI3tixFtovF1M'

    # Check if the workspace exists
    workspace_url = f'https://app.terraform.io/api/v2/organizations/{organization}/workspaces/{workspace_name}'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }
    response = requests.get(workspace_url, headers=headers)

    if response.status_code == 200:
        # Workspace exists
        delete_confirmation = input(f"Workspace '{workspace_name}' already exists. Do you want to delete it and create a new one? (y/n): ")
        if delete_confirmation.lower() == 'y':
            # Delete the workspace
            workspace_id = response.json()['data']['id']
            delete_url = f'https://app.terraform.io/api/v2/workspaces/{workspace_id}'
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code <= 210:
                print(f"Workspace '{workspace_name}' deleted successfully.")
                create_url = f'https://app.terraform.io/api/v2/organizations/{organization}/workspaces'
                data = {
                    'data': {
                        'type': 'workspaces',
                        'attributes': {
                            'name': workspace_name,
                            'execution-mode': 'local'
                    }
                }
            }
            create_response = requests.post(create_url, headers=headers, json=data)

            if create_response.status_code == 201:
                print(f"Workspace '{workspace_name}' created successfully.")
            else:
                print(f"Failed to create workspace '{workspace_name}'.")
                if create_response.content:
                    print("Error:", create_response.content.decode())
                else:
                    print("Error: No content in the response.")
        else:
            print(f"Workspace '{workspace_name}' was not deleted.")
    elif response.status_code == 404:
        # Workspace doesn't exist, prompt user to create it
        create_workspace = input(f"Workspace '{workspace_name}' does not exist. Do you want to create it? (y/n): ")
        if create_workspace.lower() == 'y':
            # Create the workspace with specific attributes
            create_url = f'https://app.terraform.io/api/v2/organizations/{organization}/workspaces'
            data = {
                'data': {
                    'type': 'workspaces',
                    'attributes': {
                        'name': workspace_name,
                        'execution-mode': 'local'
                    }
                }
            }
            create_response = requests.post(create_url, headers=headers, json=data)

            if create_response.status_code == 201:
                print(f"Workspace '{workspace_name}' created successfully.")
            else:
                print(f"Failed to create workspace '{workspace_name}'.")
                if create_response.content:
                    print("Error:", create_response.content.decode())
                else:
                    print("Error: No content in the response.")
        else:
            print(f"Workspace '{workspace_name}' was not created.")
    else:
        print(f"Failed to check workspace '{workspace_name}'.")
        if response.content:
            print("Error:", response.content.decode())
        else:
            print("Error: No content in the response.")

# Set the workspace name
workspace_name = 'homelab-external'

# Call the function to delete or create the workspace
delete_terraform_workspace(workspace_name)