import requests
import os

GH_FG_DM_ACCESS_TOKEN = os.environ.get("GH_FG_DM_ACCESS_TOKEN")
GH_BASE_URL = 'https://api.github.com'
gh_headers = {
    'Authorization': f'Bearer {GH_FG_DM_ACCESS_TOKEN}'
    # 'X-GitHub-Api-Version': '2022-11-28'
}
gh_user_name = 'zerosumhippo'
gh_repo_name = 'mock-redshift-admin'
gh_repository_url = f"{GH_BASE_URL}/repos/{gh_user_name}/{gh_repo_name}"

# Send the GET request
response = requests.get(gh_repository_url, headers=gh_headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")