# from wrappers import github_auth
import requests
import base64


class GitHubPuller:
    """Interacts with the GitHub API."""

    def __init__(self):
        self.user_name = 'zerosumhippo'
        self.repo_name = 'mock-redshift-admin'
        self.repo_contents_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/contents/"

    def get_repo_contents(self, repo_contents_path):
        try:
            response = requests.get(self.repo_contents_url + repo_contents_path)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return None
        else:
            return response.json()

    def _create_file_name_and_path_dict(self, get_repo_contents_response):
        return {
            "file names": [sql_file["name"] for sql_file in get_repo_contents_response],
            "file paths": [sql_file["path"] for sql_file in get_repo_contents_response]
        }

    def get_sql_files_in_org_shell_script(self, cmx_org_schema_name):
        """The shell script is a representation of all files that the organization has,
        which includes OneViews and other SQL files, so getting all names from the shell
        script should provide us with all possible OneViews for a specific organization.
        Pulls from: mock-redshift-admin/shell_scripts/{cmx_org_schema_name}"""
        in_org_shell_script = f"shell_scripts/{cmx_org_schema_name}"
        repo_contents = self.get_repo_contents(repo_contents_path=in_org_shell_script)
        return self._create_file_name_and_path_dict(get_repo_contents_response=repo_contents)

    def get_sql_files_specific_to_client(self, cmx_org_schema_name, cmx_client_schema_name):
        """Gets a list of the contents that exist in the client-specific folder.
        Pulls from: mock-redshift-admin/clients/{cmx_org_schema_name}/{cmx_client_schema_name}."""
        specific_to_client = f"clients/{cmx_org_schema_name}/{cmx_client_schema_name}"
        repo_contents = self.get_repo_contents(repo_contents_path=specific_to_client)
        return self._create_file_name_and_path_dict(get_repo_contents_response=repo_contents)

    def get_contents_of_sql_file(self, file_path):
        """Gets the contents of a SQL file.

        When fed by DatasetManagement.get_sql_file_paths_for_client or
        DatasetManagement.get_sql_file_paths_for_all_clients_in_org, this pulls from either:
        mock-redshift-admin/shell_scripts/
        or
        mock-redshift-admin/clients/

        The file_path parameter should look like one of the below:
        'shell_scripts/{cmx_org_schema_name}/{file_name.sql}'
        'clients/{cmx_org_schema_name}/{cmx_client_schema_name}/{file_name.sql}'
        """
        file_contents = self.get_repo_contents(repo_contents_path=file_path)
        if file_contents and 'content' in file_contents:
            sql_content = base64.b64decode(file_contents['content']).decode('utf-8')
            return sql_content
