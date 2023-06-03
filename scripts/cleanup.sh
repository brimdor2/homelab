#!/bin/bash

# Find the Python interpreter
python_executable=$(which python3)

if [ -z "$python_executable" ]; then
    echo "Python 3 is not installed. Exiting..."
    exit 1
fi

# Function to run pip install command
run_pip_install() {
    echo "Running pip install..."
    $python_executable -m pip install -r requirements.txt
}

# Function to run cloudflare_bulk_delete_dns.py
run_cloudflare_bulk_delete_dns() {
    echo "Running Cloudflare Bulk DNS Cleanup..."
    $python_executable cloudflare_bulk_delete_dns.py
}

# Function to run cloudflare_delete_tunnel.py
run_cloudflare_delete_tunnel() {
    echo "Running Cloudflare Tunnel Deletion..."
    $python_executable cloudflare_delete_tunnel.py
}

# Function to run terraform_workspace_delete_create.py
run_terraform_workspace_delete_create() {
    echo "Running Terraform Workspace Deletion and Creation.py..."
    $python_executable terraform_workspace_delete_create.py
}

# Function to run zerotier_delete_network.py
run_zerotier_delete_network() {
    echo "Running Zerotier Network Deletion.py..."
    $python_executable zerotier_delete_network.py
}

# Function to run all scripts in the specified order
run_all_scripts() {
    run_pip_install
    run_cloudflare_bulk_delete_dns
    run_cloudflare_delete_tunnel
    run_terraform_workspace_delete_create
    run_zerotier_delete_network
}

# Main menu
while true; do
    echo " "
    echo "<><><><><><><><><><><><><><><><><><><><><><><><>"
    echo "Select an option:"
    echo "1. Run Cloudflare Bulk Deletion"
    echo "2. Run Cloudflare Tunnel Deletion"
    echo "3. Run Terraform Workspace Deletion and Creation"
    echo "4. Run Zerotier Network Deletion"
    echo "5. Run all the things"
    echo "6. Install Python dependencies"
    echo "0. Exit"
    echo "<><><><><><><><><><><><><><><><><><><><><><><><>"
    echo " "
    read -p "Enter your choice: " choice
    
    case $choice in
        0) exit;;
        1) run_cloudflare_bulk_delete_dns;;
        2) run_cloudflare_delete_tunnel;;
        3) run_terraform_workspace_delete_create;;
        4) run_zerotier_delete_network;;
        5) run_all_scripts;;
        6) run_pip_install;;
        *) echo "Invalid choice";;
    esac

    echo
done