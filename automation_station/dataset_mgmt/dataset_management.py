# Gotta take arguments that identify:
# # client
# # oneview
# # redshift cluster
# Then it would reach into github to grab the SQL
# Then update in Redshift
# Then run metadata generation
from github_api import GitHubPuller
from mock_hestia import Hestia

hestia = Hestia()
ghpuller = GitHubPuller()


class DatasetManagement:
    """Finds OneViews for an agency or client in GitHub and runs the SQL scripts."""

    def __init__(self):
        pass

    # def _prioritize_client_folder_over_org_shell(self, org_shell_contents, client_folder_contents):
    #     org_shell_file_name_list = org_shell_contents["file names"]
    #     client_folder_file_name_list = client_folder_contents["file names"]
    #     org_shell_file_path_list = org_shell_contents["file paths"]
    #     client_folder_file_path_list = client_folder_contents["file paths"]
    #     final_file_path_list = [file_name for file_name in org_shell_contents["file paths"] if ]

    def get_sql_file_paths_for_client(self, client_id):
        client_schema_name = hestia.get_client_metadata(client_id=client_id)["schema name"]
        organization_schema_name = hestia.get_org_metadata(
            org_id=hestia.get_client_metadata(client_id=client_id)["organization id"]
        )["schema name"]
        org_shell_contents = ghpuller.get_sql_files_in_org_shell_script(organization_schema_name)
        client_folder_contents = ghpuller.get_sql_files_specific_to_client(organization_schema_name, client_schema_name)
        # self._prioritize_client_folder_over_org_shell(org_shell_contents)
        return org_shell_contents
        # need to add logic to remove oneviews from org_shell_sql_files if they exist in client_folder_sql_files
