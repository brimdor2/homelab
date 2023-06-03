import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cloudflare Global API Key and zone ID from environment variables
CLOUDFLARE_GLOBAL_API_KEY = os.environ.get("CLOUDFLARE_GLOBAL_API_KEY")
if CLOUDFLARE_GLOBAL_API_KEY is None or CLOUDFLARE_GLOBAL_API_KEY.strip() == "":
    CLOUDFLARE_GLOBAL_API_KEY = input("Enter Cloudflare Global API Key: ")
    os.environ["CLOUDFLARE_GLOBAL_API_KEY"] = CLOUDFLARE_GLOBAL_API_KEY
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_GLOBAL_API_KEY={}\n".format(CLOUDFLARE_GLOBAL_API_KEY))

CLOUDFLARE_EMAIL = os.environ.get("CLOUDFLARE_EMAIL")
if CLOUDFLARE_EMAIL is None or CLOUDFLARE_EMAIL.strip() == "":
    CLOUDFLARE_EMAIL = input("Enter Cloudflare Email: ")
    os.environ["CLOUDFLARE_EMAIL"] = CLOUDFLARE_EMAIL
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_EMAIL={}\n".format(CLOUDFLARE_EMAIL))

CLOUDFLARE_ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID")
if CLOUDFLARE_ZONE_ID is None or CLOUDFLARE_ZONE_ID.strip() == "":
    CLOUDFLARE_ZONE_ID = input("Enter Cloudflare Zone ID: ")
    os.environ["CLOUDFLARE_ZONE_ID"] = CLOUDFLARE_ZONE_ID
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_ZONE_ID={}\n".format(CLOUDFLARE_ZONE_ID))

# Specify the keywords to match in the content attribute
KEYWORDS = os.environ.get("KEYWORDS")
if KEYWORDS is None or KEYWORDS.strip() == "":
    KEYWORDS = input("Enter keywords (comma-separated): ")
    keywords = [keyword.strip() for keyword in KEYWORDS.split(",")]
    os.environ["KEYWORDS"] = ",".join(keywords)
    with open(".env", "a") as env_file:
        env_file.write("KEYWORDS={}\n".format(",".join(keywords)))
else:
    keywords = KEYWORDS.split(",")

def delete_dns_entries(CLOUDFLARE_GLOBAL_API_KEY, CLOUDFLARE_EMAIL, CLOUDFLARE_ZONE_ID, keywords):
    headers = {
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'Content-Type': 'application/json'
    }

    url = f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records'
    params = {
        'per_page': 100,  # Maximum number of records per page
    }

    # Fetch all DNS records
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        dns_records = response.json()['result']
        record_count = len(dns_records)
        if record_count == 0:
            print('No DNS records found.')
            return

        # Filter DNS records based on keywords
        filtered_records = []
        for record in dns_records:
            for keyword in keywords:
                if keyword in record