from github_api import GitHubPuller
from imitation_hestia import Hestia

hestia = Hestia()
github = GitHubPuller()


class DatasetManagement:
    """Finds OneViews for an agency or client in GitHub and runs the SQL scripts."""

    def __init__(self):
        pass

    def _only_retain_sql_files(self, github_repo_contents_dict):
        for n in range(len(github_repo_contents_dict["file names"]) - 1):
            if ".sql" not in github_repo_contents_dict["file names"][n]:
                github_repo_contents_dict["file names"].remove(github_repo_contents_dict["file names"][n])
                github_repo_contents_dict["file paths"].remove(github_repo_contents_dict["file paths"][n])
        return github_repo_contents_dict

    def _prioritize_client_folder_over_org_shell(self, org_shell_contents, client_folder_contents):
        org_shell_file_path_indices = [org_shell_contents["file names"].index(file_name) for file_name
                                       in org_shell_contents["file names"] if file_name not in
                                       client_folder_contents["file names"]]
        sql_files_to_execute_list = [file_path for file_path in org_shell_contents["file paths"]
                                     if org_shell_contents["file paths"].index(file_path)
                                     in org_shell_file_path_indices]
        return sql_files_to_execute_list + client_folder_contents["file paths"]

    def get_sql_file_paths_for_client(self, client_id):
        client_schema_name = hestia.get_client_metadata(client_id=client_id)["schema name"]
        organization_schema_name = hestia.get_org_metadata(
            org_id=hestia.get_client_metadata(client_id=client_id)["organization id"]
        )["schema name"]
        org_shell_contents = github.get_sql_files_in_org_shell_script(organization_schema_name)
        org_shell_contents = self._only_retain_sql_files(org_shell_contents)
        client_folder_contents = github.get_sql_files_specific_to_client(organization_schema_name, client_schema_name)
        client_folder_contents = self._only_retain_sql_files(client_folder_contents)
        return self._prioritize_client_folder_over_org_shell(org_shell_contents, client_folder_contents)

    def get_sql_file_paths_for_all_clients_in_org(self, org_id):
        client_id_list = hestia.get_client_ids_for_org(org_id)
        client_sql_file_paths_list = []
        for client_id in client_id_list:
            client_sql_file_list = self.get_sql_file_paths_for_client(client_id)
            client_sql_file_path_dict = {"client_id": client_id, "client_sql_file_list": client_sql_file_list}
            client_sql_file_paths_list.append(client_sql_file_path_dict)
        return client_sql_file_paths_list

    def execute_sql_files_for_client(self, client_id, redshift_cluster_id):
        sql_file_list = self.get_sql_file_paths_for_client(client_id)
        for file in sql_file_list:
            sql_in_file = github.get_sql_file_content(file)
            print(f'Execute the below sql in redshift cluster id: {redshift_cluster_id}\n\n"{sql_in_file}"\n')
        print(f"Run metadata generation.")

    def execute_sql_files_for_all_clients_in_org(self, org_id, redshift_cluster_id):
        client_id_list = hestia.get_client_ids_for_org(org_id)
        for client_id in client_id_list:
            self.execute_sql_files_for_client(client_id, redshift_cluster_id)

# dm = DatasetManagement()
# print(dm.get_sql_file_paths_for_client(12345))