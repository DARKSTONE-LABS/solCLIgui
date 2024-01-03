import re

def extract_wallet_addresses(log_file_path, output_file_path):
    # Regex pattern to match the wallet addresses
    address_pattern = r'\b[A-Za-z0-9]{40,45}\b'

    with open(log_file_path, 'r') as file:
        log_content = file.read()

    addresses = re.findall(address_pattern, log_content)

    with open(output_file_path, 'w') as output_file:
        for address in addresses:
            output_file.write(address + '\n')

    print(f"Extracted addresses are written to {output_file_path}")

# Usage
log_file_path = 'dist\wallets.txt'  # Replace with the path to your log file
output_file_path = 'wallets.txt'  # Output file
extract_wallet_addresses(log_file_path, output_file_path)
