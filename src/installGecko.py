import requests
import os
from platform import machine
import gzip
import gnupg

def get_architecture():
    # Get the machine architecture
    arch = machine()
    if arch == "x86_64":
        return "linux64"
    elif arch == "AMD64":
        return "linux64"
    elif arch == "arm64":
        return "linux-aarch64"
    elif arch == "aarch64":
        return "linux-aarch64"
    else:
        raise ValueError(f"Unsupported architecture: {arch}")

def download_asset(url):
    # Extract the filename from the URL
    filename = os.path.join("./", os.path.basename(url))
    # Download the asset
    response = requests.get(url)
    if response.status_code == 200:
        # Write the downloaded content to a temporary file
        temp_filename = filename + '.temp'
        with open(temp_filename, 'wb') as f:
            f.write(response.content)

        # Extract the .gz file
        with gzip.open(temp_filename, 'rb') as gz_file:
            with open(filename, 'wb') as f:
                f.write(gz_file.read())

        # Remove the temporary file
        os.remove(temp_filename)

        print(f"Downloaded and extracted: {filename}")
    else:
        print(f"Failed to download asset: {response.status_code}")

def fetch_latest_assets(owner, repo):
    # Fetch information about the latest release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Download assets associated with the release
        architecture = get_architecture()
        for asset in data.get('assets', []):
            if architecture in asset['name']:
                download_asset(asset['browser_download_url'])
    else:
        print(f"Failed to fetch latest release: {response.status_code}")

def verify_signature(signed_file, original_file):
    gpg = gnupg.GPG()
    with open(signed_file, 'rb') as f:
        verified = gpg.verify_file(f, original_file)
        if verified:
            print(f"Signature verification successful: {signed_file}")
        else:
            print(f"Signature verification failed: {signed_file}")

if __name__ == "__main__":
    fetch_latest_assets("mozilla", "geckodriver")
