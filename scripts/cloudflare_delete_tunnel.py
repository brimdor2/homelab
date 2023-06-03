import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cloudflare Global API Key
CLOUDFLARE_GLOBAL_API_KEY = os.environ.get("CLOUDFLARE_GLOBAL_API_KEY")
if CLOUDFLARE_GLOBAL_API_KEY is None or CLOUDFLARE_GLOBAL_API_KEY.strip() == "":
    CLOUDFLARE_GLOBAL_API_KEY = input("Enter Cloudflare Global API Key: ")
    os.environ["CLOUDFLARE_GLOBAL_API_KEY"] = CLOUDFLARE_GLOBAL_API_KEY
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_GLOBAL_API_KEY={}\n".format(CLOUDFLARE_GLOBAL_API_KEY))

CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
if CLOUDFLARE_ACCOUNT_ID is None or CLOUDFLARE_ACCOUNT_ID.strip() == "":
    CLOUDFLARE_ACCOUNT_ID = input("Enter Cloudflare Account ID: ")
    os.environ["CLOUDFLARE_ACCOUNT_ID"] = CLOUDFLARE_ACCOUNT_ID
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_ACCOUNT_ID={}\n".format(CLOUDFLARE_ACCOUNT_ID))

CLOUDFLARE_EMAIL = os.environ.get("CLOUDFLARE_EMAIL")
if CLOUDFLARE_EMAIL is None or CLOUDFLARE_EMAIL.strip() == "":
    CLOUDFLARE_EMAIL = input("Enter Cloudflare Email: ")
    os.environ["CLOUDFLARE_EMAIL"] = CLOUDFLARE_EMAIL
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_EMAIL={}\n".format(CLOUDFLARE_EMAIL))


# Make the GET request
url = "https://api.cloudflare.com/client/v4/accounts/{}/cfd_tunnel".format(CLOUDFLARE_ACCOUNT_ID)
headers = {
    "X-Auth-Email": CLOUDFLARE_EMAIL,
    "X-Auth-Key": CLOUDFLARE_GLOBAL_API_KEY,
}
response = requests.get(url, headers=headers)

# Check the status code
if response.status_code == 200:
    # The request was successful
    data = response.json()
    tunnels = data["result"]
    non_deleted_tunnels = [tunnel for tunnel in tunnels if tunnel.get("deleted_at") is None]
    if not non_deleted_tunnels:
        print("No Tunnels")
        sys.exit()
    print("Tunnels:")
    for i, tunnel in enumerate(non_deleted_tunnels):
        print("{}. Name: {} - Tunnel ID: {}".format(i + 1, tunnel["name"], tunnel["id"]))
else:
    # The request failed
    print("Error: {}".format(response.status_code))
    sys.exit()

# Delete the selected tunnel
selected_tunnel_index = input("Enter the tunnel number to delete: ")
try:
    selected_tunnel_index = int(selected_tunnel_index)
    print(" ")
    if 1 <= selected_tunnel_index <= len(non_deleted_tunnels):
        selected_tunnel = non_deleted_tunnels[selected_tunnel_index - 1]
        tunnel_id = selected_tunnel["id"]
        tunnel_name = selected_tunnel["name"]
        print("Selected tunnel: {} - Tunnel ID: {}".format(tunnel_name, tunnel_id))

        confirmation = input("Are you sure you want to delete this tunnel? (y/n): ")
        if confirmation.lower() == "y":
            delete_url = "https://api.cloudflare.com/client/v4/accounts/{}/cfd_tunnel/{}".format(CLOUDFLARE_ACCOUNT_ID, tunnel_id)
            response = requests.delete(delete_url, headers=headers)

            if response.status_code == 200:
                print("Tunnel deleted successfully")
            else:
                print("Error deleting tunnel: {}".format(response.status_code))
        else:
            print("Deletion canceled")
    else:
        print("Invalid tunnel number")
except ValueError:
    print("Invalid input. Please enter a valid tunnel number.")
