from wrappers import github_auth
import requests


class GitHubPuller:
    """Interacts with the GitHub API."""

    def __init__(self):
        self.user_name = 'zerosumhippo'
        self.repo_name = 'mock-redshift-admin'
        self.repo_contents_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/contents/"

    def _transform_response_into_oneview_list(self, api_response):
        return [oneview["name"] for oneview in api_response.json()]

    # @github_auth
    # def _get_repo_contents(self, auth, repo_contents_path):
    #     return requests.get(self.repo_contents_url + repo_contents_path, headers=auth["gh_headers"])

    @github_auth
    def get_oneviews_in_org_shell_script(self, auth, cmx_org_schema_name):
        """The shell script is a representation of all OneViews that the organization has, so
        getting all names from the shell script should provide us with all possible OneViews
        for a specific organization.
        Pulls from mock-redshift-admin/shell_scripts/{cmx_org_schema_name}"""
        repo_contents_path = f"shell_scripts/{cmx_org_schema_name}"
        try:
            response = requests.get(self.repo_contents_url + repo_contents_path, headers=auth["gh_headers"])
            # create an internal function and wrapper to do this
            # once that is done, both of these functions can probably be combined into one
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return None
        else:
            return self._transform_response_into_oneview_list(response)

    @github_auth
    def get_client_specific_oneviews(self, auth, cmx_org_schema_name, cmx_client_schema_name):
        """Gets a list of the OneViews that exist in the client-specific folder in
        mock-redshift-admin/clients/{cmx_org_schema_name}/{cmx_client_schema_name}."""
        repo_contents_path = f"clients/{cmx_org_schema_name}/{cmx_client_schema_name}"
        try:
            response = requests.get(self.repo_contents_url + repo_contents_path, headers=auth["gh_headers"])
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return None
        else:
            return self._transform_response_into_oneview_list(response)
