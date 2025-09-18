import requests
import pandas as pd 
import os
import logging
import time
from tqdm import tqdm  # Import tqdm for progress bar
from dotenv import load_dotenv  # Import python-dotenv

# Load environment variables from .env file
load_dotenv()
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## ensure error.log file exists
if not os.path.exists(f'{c_dir}/error.log'):
    with open(f'{c_dir}/error.log', 'w'):
        pass

## configure logging
logging.basicConfig(filename=f'{c_dir}/error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_repositories(gh_pat, org_name):
    try:
        ## page number
        i = 1
        repositories_info = []
        # Initialize tqdm for repository pages
        with tqdm(desc="Fetching repositories", unit="page") as pbar:
            while True:
                # request header
                headers = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {gh_pat}",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                ## parameters for the API
                params = {
                    "per_page": 100,
                    "page": i,
                }
                url = f"https://api.github.com/orgs/{org_name}/repos"
                response = requests.get(url, headers=headers, params=params)
                
                # Check if response is successful
                if response.status_code != 200:
                    error_msg = f"API request failed with status {response.status_code}: {response.text}"
                    print(error_msg)
                    logging.error(error_msg)
                    return repositories_info  # Return what we have so far
                
                # Parse JSON response
                results = response.json()
                
                # Check if results is a list (expected for repo data)
                if not isinstance(results, list):
                    error_msg = f"Unexpected API response format: {results}"
                    print(error_msg)
                    logging.error(error_msg)
                    return repositories_info  # Return what we have so far
                
                # If no repositories in this page, break
                if not results:
                    break
                
                # Process each repository
                for repository in results:
                    # Verify repository is a dict and has 'full_name'
                    if isinstance(repository, dict) and 'full_name' in repository:
                        repositories_info.append(repository['full_name'])
                    else:
                        error_msg = f"Invalid repository data: {repository}"
                        print(error_msg)
                        logging.error(error_msg)
                
                i += 1
                pbar.update(1)  # Update progress bar for each page
        return repositories_info
    except requests.exceptions.RequestException as e:
        error_msg = f'Error occurred while fetching data: {e}'
        print(error_msg)
        logging.error(error_msg)
        return []

def get_lang_in_repositories(gh_pat, repo_names):
    try:
        # Initialize DataFrame
        columns = ['repo_name', 'language_used']
        df = pd.DataFrame(columns=columns)
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {gh_pat}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        # Use tqdm to show progress for repositories
        for repo_name in tqdm(repo_names, desc="Fetching languages", unit="repo"):
            url = f"https://api.github.com/repos/{repo_name}/languages"
            response = requests.get(url, headers=headers)
            
            # Check if response is successful
            if response.status_code != 200:
                error_msg = f"API request failed for {repo_name} with status {response.status_code}: {response.text}"
                print(error_msg)
                logging.error(error_msg)
                continue  # Skip to next repo
            
            # Parse JSON response
            results = response.json()
            
            # Verify results is a dictionary (language data)
            if not isinstance(results, dict):
                error_msg = f"Unexpected language data format for {repo_name}: {results}"
                print(error_msg)
                logging.error(error_msg)
                continue
            
            # Process languages
            keys = list(results.keys())
            for lang in keys:
                data = [[repo_name, lang]]
                n_df = pd.DataFrame(data, columns=columns)
                df = pd.concat([df, n_df], axis=0, ignore_index=True)
        return df
    except requests.exceptions.RequestException as e:
        error_msg = f'Error occurred while fetching language data: {e}'
        print(error_msg)
        logging.error(error_msg)
        return pd.DataFrame(columns=columns)

if __name__ == "__main__":
    # GitHub Personal Access Token
    gh_pat = os.environ.get("GH_PAT")
    if not gh_pat:
        print("Error: GH_PAT environment variable not set")
        exit(1)
    
    # GitHub Organization Name
    org_name = "freeCodeCamp"
    start = time.time()
    repo_names = get_user_repositories(gh_pat, org_name)
    df = get_lang_in_repositories(gh_pat, repo_names)
    df.to_csv(f'{c_dir}/listing_languages_1.csv', index=False)
    end = time.time()
    print(f"Time taken to execute the script: {end - start:.2f} seconds")