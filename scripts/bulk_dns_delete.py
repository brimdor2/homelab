import requests

# Set your Cloudflare API key and zone ID
API_KEY = ''
ZONE_ID = ''

# Specify the keywords to match in the content attribute
KEYWORDS = ['heritage=external-dns','10.0.255.224', 'homelab-tunnel']


def delete_dns_entries(api_key, zone_id, keywords):
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
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
                if keyword in record['name'] or keyword in record['content']:
                    filtered_records.append(record)
                    break

        filtered_count = len(filtered_records)
        if filtered_count == 0:
            print('No DNS records found containing the specified keywords.')
            return

        print(f'Found {filtered_count} DNS record(s) containing the specified keywords.')
        print('Deleting DNS records...')

        # Delete each filtered DNS record
        for record in filtered_records:
            record_id = record['id']
            delete_url = f'{url}/{record_id}'
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 200:
                print(f'Deleted DNS record with ID: {record_id}')
            else:
                print(f'Failed to delete DNS record with ID: {record_id}')
                print('Error message:', delete_response.json())
    else:
        print('Failed to fetch DNS records.')
        print('Error message:', response.json())


# Call the function to delete DNS entries for each keyword
delete_dns_entries(API_KEY, ZONE_ID, KEYWORDS)
