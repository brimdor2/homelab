import requests
import json
import os

from dotenv import load_dotenv
from requests.exceptions import RequestException

# Load environment variables from .env file
load_dotenv()

# Get the Zerotier API token
ZEROTIER_API_TOKEN = os.environ.get("ZEROTIER_API_TOKEN")
if ZEROTIER_API_TOKEN is None or ZEROTIER_API_TOKEN.strip() == "":
    ZEROTIER_API_TOKEN = input("Enter Zerotier API Token: ")
    os.environ["ZEROTIER_API_TOKEN"] = ZEROTIER_API_TOKEN
    with open(".env", "a") as env_file:
        env_file.write("ZEROTIER_API_TOKEN={}\n".format(ZEROTIER_API_TOKEN))

# Check if the network exists
url = "https://api.zerotier.com/api/v1/network"
headers = {
    "Authorization": "Bearer {}".format(ZEROTIER_API_TOKEN)
}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # The network exists, display the network name and id
        networks = response.json()

        if len(networks) == 0:
            print("No networks found")
            exit()

        # Display the networks with unique numbering
        print("Select a network to delete:")
        for i, network in enumerate(networks, start=1):
            print("{}. {} - {}".format(i, network["config"]["name"], network["id"]))

        # Delete the selected network
        selection = int(input("Enter the network number: "))
        print(" ")

        if selection < 1 or selection > len(networks):
            print("Invalid network number")
        else:
            network_id = networks[selection - 1]["id"]
            url = "https://api.zerotier.com/api/v1/network/{}".format(network_id)
            headers = {
                "Authorization": "Bearer {}".format(ZEROTIER_API_TOKEN),
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                print("Network deleted successfully")
            else:
                print("Error deleting network: {}".format(response.status_code))
    else:
        print("Error: {}".format(response.status_code))

except RequestException as e:
    print("Error: {}".format(str(e)))
