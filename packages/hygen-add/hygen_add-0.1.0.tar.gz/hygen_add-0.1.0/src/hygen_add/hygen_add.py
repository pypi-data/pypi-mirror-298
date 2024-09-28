import os
import requests
from urllib.parse import urlparse
from argparse import ArgumentParser


def extract_repo_info(repo_url: str):
    """Extracts the owner and repository name from the GitHub URL."""
    parsed_url = urlparse(repo_url)
    
    if parsed_url.netloc != 'github.com':
        raise ValueError("Invalid GitHub URL")
    
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        raise ValueError("Invalid repository path")
    
    # Extract the repository owner and name
    REPO_OWNER = path_parts[0]
    REPO_NAME = path_parts[1]
    
    return REPO_OWNER, REPO_NAME

def download_file(file_url: str, file_path: str):
    """Downloads a file from the GitHub file URL."""
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {file_path}")

def download_folder(repo_url, folder_path, local_path, branch):
    """Downloads all files in the folder from the GitHub repository."""
    REPO_OWNER, REPO_NAME = extract_repo_info(repo_url)
    
    # GitHub API URL for the repository content
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{folder_path}?ref={branch}"
    
    # Create local directory if it does not exist
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    response = requests.get(api_url)
    
    if response.status_code == 200:
        folder_contents = response.json()
        
        # Loop through the contents and download each file
        for content in folder_contents:
            if content['type'] == 'file':
                file_url = content['download_url']
                file_name = content['name']
                file_path = os.path.join(local_path, file_name)
                download_file(file_url, file_path)
            elif content['type'] == 'dir':
                # Recursively download subfolders
                subfolder_path = os.path.join(folder_path, content['name'])
                subfolder_local_path = os.path.join(local_path, content['name'])
                download_subfolder(REPO_OWNER, REPO_NAME, subfolder_path, subfolder_local_path, branch)
    else:
        print(f"Failed to retrieve folder contents. Status Code: {response.status_code}")

def download_subfolder(
        repo_owner: str,
        repo_name: str,
        subfolder_path: str,
        subfolder_local_path: str,
        branch: str
    ):
    """Downloads files recursively from subfolders."""
    # GitHub API URL for the subfolder content
    subfolder_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{subfolder_path}?ref={branch}"
    
    if not os.path.exists(subfolder_local_path):
        os.makedirs(subfolder_local_path)

    response = requests.get(subfolder_url)
    
    if response.status_code == 200:
        folder_contents = response.json()
        for content in folder_contents:
            if content['type'] == 'file':
                file_url = content['download_url']
                file_name = content['name']
                file_path = os.path.join(subfolder_local_path, file_name)
                download_file(file_url, file_path)
            elif content['type'] == 'dir':
                # Recursively download deeper subfolders
                sub_subfolder_path = os.path.join(subfolder_path, content['name'])
                sub_subfolder_local_path = os.path.join(subfolder_local_path, content['name'])
                download_subfolder(repo_owner, repo_name, sub_subfolder_path, sub_subfolder_local_path, branch)
    else:
        print(f"Failed to retrieve subfolder contents. Status Code: {response.status_code}")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('url', help='github repository url with hygen template')
    parser.add_argument('-b', '--branch', default='main')
    parser.add_argument('-f', '--folder', default='_templates')
    parser.add_argument('-t', '--target', default='_templates', help='local target')
    return parser.parse_args()

def main():
    args = parse_args()

    download_folder(args.url, args.folder, args.target, args.branch)

if __name__ == "__main__":
    main()
