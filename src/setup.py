import requests
from os import path, remove
from platform import machine
import tarfile

def main():
    # Fetch the latest release assets for the repository
    print("Setting up geckodriver")
    fetch_latest("mozilla", "geckodriver")


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
    print(f"Downloading: {url}")
    # Extract the filename from the URL
    filename = path.join("./", path.basename(url))
    # Download the asset
    response = requests.get(url)
    if response.status_code == 200:
        #Save the asset to the current directory
        with open(filename, 'wb') as file:
            file.write(response.content)
        # Extract the contents of the archive
        print(f"Extracting to: {filename}")
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall()
        # Remove the archive file
        remove(filename)

        # Check for the geckodriver binary
        if path.exists("geckodriver"):
            print("geckodriver is setup")
        else:
            exit("Failed to download geckodriver binary")        
    else:
        exit(f"Failed to download asset: {response.status_code}")

def fetch_latest(owner, repo):
    # Fetch information about the latest release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Download assets associated with the release
        architecture = get_architecture()
        for asset in data.get('assets', []):
            # Download the asset if it matches the architecture and is a gz archive
            if architecture in asset["name"] and asset["name"].endswith('.gz'):
                download_asset(asset['browser_download_url'])
    else:
        exit(f"Failed to fetch latest release: {response.status_code}")

if __name__ == "__main__":
    main()