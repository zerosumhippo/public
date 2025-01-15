import unittest
from unittest.mock import patch, MagicMock
from dataset_management import DatasetManagement
from github_api import GitHubPuller
from imitation_hestia import Hestia


class TestDatasetManagement(unittest.TestCase):

    @patch('dataset_management.Hestia')
    @patch('dataset_management.GitHubPuller')
    def setUp(self, MockGitHubPuller, MockHestia):
        self.mock_hestia = MockHestia.return_value
        self.mock_github = MockGitHubPuller.return_value
        self.dm = DatasetManagement()

    def test_only_retain_sql_files(self):
        input_data = {
            "file names": ["script1.sql", "script2.txt", "script3.sql"],
            "file paths": ["/path/script1.sql", "/path/script2.txt", "/path/script3.sql"]
        }
        expected_output = {
            "file names": ["script1.sql", "script3.sql"],
            "file paths": ["/path/script1.sql", "/path/script3.sql"]
        }
        result = self.dm._only_retain_sql_files(input_data)
        self.assertEqual(result, expected_output)

    def test_prioritize_client_folder_over_org_shell(self):
        org_shell_contents = {
            "file names": ["script1.sql", "script2.sql"],
            "file paths": ["/path/org/script1.sql", "/path/org/script2.sql"]
        }
        client_folder_contents = {
            "file names": ["script2.sql", "script3.sql"],
            "file paths": ["/path/client/script2.sql", "/path/client/script3.sql"]
        }
        expected_output = ["/path/org/script1.sql", "/path/client/script2.sql", "/path/client/script3.sql"]
        result = self.dm._prioritize_client_folder_over_org_shell(org_shell_contents, client_folder_contents)
        self.assertEqual(result, expected_output)

    # @patch('dataset_management.DatasetManagement._only_retain_sql_files')
    # def test_get_sql_file_paths_for_client(self, mock_only_retain_sql_files):
    #     self.mock_hestia.get_client_metadata.return_value = {"schema name": "client_schema", "organization id": 123}
    #     self.mock_hestia.get_org_metadata.return_value = {"schema name": "org_schema"}
    #     self.mock_github.get_sql_files_in_org_shell_script.return_value = {"file names": ["file1.sql"], "file paths": ["path1/file1.sql"]}
    #     self.mock_github.get_sql_files_specific_to_client.return_value = {"file names": ["file2.sql"], "file paths": ["path2/file2.sql"]}
    #     mock_only_retain_sql_files.side_effect = lambda x: x
    #
    #     expected_output = ["path1/file1.sql", "path2/file2.sql"]
    #     result = self.dm.get_sql_file_paths_for_client(1)
    #     self.assertEqual(result, expected_output)

    # @patch('dataset_management.DatasetManagement.get_sql_file_paths_for_client')
    # def test_get_sql_file_paths_for_all_clients_in_org(self, mock_get_sql_file_paths_for_client):
    #     self.mock_hestia.get_client_ids_for_org.return_value = [1, 2]
    #     mock_get_sql_file_paths_for_client.side_effect = [
    #         ["path1/file1.sql", "path2/file2.sql"],
    #         ["path3/file3.sql", "path4/file4.sql"]
    #     ]
    #
    #     expected_output = [
    #         {"client_id": 1, "client_sql_file_list": ["path1/file1.sql", "path2/file2.sql"]},
    #         {"client_id": 2, "client_sql_file_list": ["path3/file3.sql", "path4/file4.sql"]}
    #     ]
    #     result = self.dm.get_sql_file_paths_for_all_clients_in_org(123)
    #     self.assertEqual(result, expected_output)

    @patch('dataset_management.GitHubPuller.get_sql_file_content')
    @patch('dataset_management.DatasetManagement.get_sql_file_paths_for_client')
    def test_execute_sql_files_for_client(self, mock_get_sql_file_paths_for_client, mock_get_sql_file_content):
        mock_get_sql_file_paths_for_client.return_value = ["path1/file1.sql", "path2/file2.sql"]
        mock_get_sql_file_content.side_effect = ["SELECT * FROM table1;", "SELECT * FROM table2;"]
        with patch('builtins.print') as mock_print:
            self.dm.execute_sql_files_for_client(1, 589)
            mock_print.assert_any_call('Execute the below sql in redshift cluster id: 589\n\n"SELECT * FROM table1;"\n')
            mock_print.assert_any_call('Execute the below sql in redshift cluster id: 589\n\n"SELECT * FROM table2;"\n')
            mock_print.assert_any_call("Run metadata generation.")

    @patch('dataset_management.Hestia.get_client_ids_for_org')
    @patch('dataset_management.DatasetManagement.execute_sql_files_for_client')
    def test_execute_sql_files_for_all_clients_in_org(self, mock_get_client_ids_for_org, mock_execute_sql_files_for_client):
        mock_get_client_ids_for_org.return_value = [1, 2]
        self.dm.execute_sql_files_for_all_clients_in_org(org_id=123, redshift_cluster_id=589)
        mock_execute_sql_files_for_client.assert_any_call(client_id=1, redshift_cluster_id=589)
        mock_execute_sql_files_for_client.assert_any_call(client_id=2, redshift_cluster_id=589)
        # shit wont fucking work...i dont get it
