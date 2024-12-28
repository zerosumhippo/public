from wrappers import github_auth
import requests


class GitHubPuller:
    """Interacts with the GitHub API."""

    def __init__(self):
        self.user_name = 'zerosumhippo'
        self.repo_name = 'mock-redshift-admin'
        self.repo_contents_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/contents/"

    def _get_repo_contents(self, repo_contents_path):
        try:
            response = requests.get(self.repo_contents_url + repo_contents_path)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return None
        else:
            return {
                "file names": [sql_file["name"] for sql_file in response.json()],
                "file paths": [sql_file["path"] for sql_file in response.json()]
            }

    def get_sql_files_in_org_shell_script(self, cmx_org_schema_name):
        """The shell script is a representation of all files that the organization has,
        which includes OneViews and other SQL files, so getting all names from the shell
        script should provide us with all possible OneViews for a specific organization.
        Pulls from: mock-redshift-admin/shell_scripts/{cmx_org_schema_name}"""
        in_org_shell_script = f"shell_scripts/{cmx_org_schema_name}"
        return self._get_repo_contents(repo_contents_path=in_org_shell_script)

    def get_sql_files_specific_to_client(self, cmx_org_schema_name, cmx_client_schema_name):
        """Gets a list of the contents that exist in the client-specific folder.
        Pulls from: mock-redshift-admin/clients/{cmx_org_schema_name}/{cmx_client_schema_name}."""
        specific_to_client = f"clients/{cmx_org_schema_name}/{cmx_client_schema_name}"
        return self._get_repo_contents(repo_contents_path=specific_to_client)
