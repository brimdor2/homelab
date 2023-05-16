import requests

def delete_all_zerotier_networks(zerotier_token):
    headers = {
        'Authorization': f'Bearer {zerotier_token}',
        'Content-Type': 'application/json'
    }

    # Fetch all networks
    networks_url = 'https://my.zerotier.com/api/network'
    response = requests.get(networks_url, headers=headers)

    if response.status_code == 200:
        networks = response.json()
        network_count = len(networks)

        if network_count == 0:
            print('No networks found.')
            return

        print(f'Found {network_count} network(s):')
        for network in networks:
            network_id = network['id']
            network_name = network['config']['name']
            print(f'- {network_name} ({network_id})')

        delete_networks = input('Do you want to delete all ZeroTier networks? (y/n): ')

        if delete_networks.lower() == 'y':
            print('Deleting networks...')

            # Delete each network
            for network in networks:
                network_id = network['id']
                delete_url = f'{networks_url}/{network_id}'
                delete_response = requests.delete(delete_url, headers=headers)

                if delete_response.status_code == 200:
                    print(f'Deleted network with ID: {network_id}')
                else:
                    print(f'Failed to delete network with ID: {network_id}')
                    print('Error message:', delete_response.json())
        else:
            print('Network deletion cancelled.')
    else:
        print('Failed to fetch networks.')
        print('Error message:', response.json())

# Set your ZeroTier API token
zerotier_token = '4GmtUw3cIonf0CaESdByKqcTukgyRdHZ'

# Call the function to delete all ZeroTier networks
delete_all_zerotier_networks(zerotier_token)