from wrappers import github_auth
import requests


class GitHubPuller:
    """Interacts with the GitHub API."""

    def __init__(self):
        self.user_name = 'zerosumhippo'
        self.repo_name = 'mock-redshift-admin'
        self.repo_contents_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/contents/"

    @github_auth
    def get_oneviews_in_org_shell_script(self, auth, cmx_org_schema_name):
        """The shell script is a representation of all OneViews that the organization has, so
        getting all names from the shell script should provide us with all possible OneViews
        for a specific organization."""
        repo_contents_path = f"shell_scripts/{cmx_org_schema_name}"
        try:
            response = requests.get(self.repo_contents_url + repo_contents_path, headers=auth["gh_headers"])
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return None
        else:
            oneview_names = [oneview["name"] for oneview in response.json()]
            return oneview_names
