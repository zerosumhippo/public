import unittest
from unittest.mock import patch, MagicMock
from dataset_management import DatasetManagement


class TestDatasetManagement(unittest.TestCase):

    def setUp(self):
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

    @patch('dataset_management.GitHubPuller.get_sql_files_specific_to_client')
    @patch('dataset_management.GitHubPuller.get_sql_files_in_org_shell_script')
    @patch('dataset_management.Hestia.get_org_metadata')
    @patch('dataset_management.Hestia.get_client_metadata')
    def test_get_sql_file_paths_for_client(self,
                                           mock_get_client_metadata,
                                           mock_get_org_metadata,
                                           mock_get_sql_files_in_org_shell_script,
                                           mock_get_sql_files_specific_to_client
                                           ):
        mock_get_client_metadata.return_value = {"schema name": "client_schema_name", "organization id": 123}
        mock_get_org_metadata.return_value = {"schema name": "org_schema_name"}
        mock_get_sql_files_in_org_shell_script.return_value = {
            "file names": ['v_oneview_name_1.sql', 'v_oneview_name_2.sql'],
            "file paths": ['mock-redshift-admin/shell_scripts/org_schema_name/v_oneview_name_1.sql',
                           'mock-redshift-admin/shell_scripts/org_schema_name/v_oneview_name_2.sql']
        }
        mock_get_sql_files_specific_to_client.return_value = {
            "file names": ['v_oneview_name_1.sql'],
            "file paths": ['clients/org_schema_name/client_schema_name/v_oneview_name_1.sql']
        }
        expected_output = ['mock-redshift-admin/shell_scripts/org_schema_name/v_oneview_name_2.sql',
                           'clients/org_schema_name/client_schema_name/v_oneview_name_1.sql']
        result = self.dm.get_sql_file_paths_for_client(1)
        self.assertEqual(result, expected_output)

    @patch('dataset_management.DatasetManagement.get_sql_file_paths_for_client')
    @patch('dataset_management.Hestia.get_client_ids_for_org')
    def test_get_sql_file_paths_for_all_clients_in_org(self,
                                                       mock_get_client_ids_for_org,
                                                       mock_get_sql_file_paths_for_client):
        mock_get_client_ids_for_org.return_value = [1, 2]
        mock_get_sql_file_paths_for_client.return_value = ["path1/file1.sql", "path2/file2.sql"]
        expected_output = [
            {"client_id": 1, "client_sql_file_list": ["path1/file1.sql", "path2/file2.sql"]},
            {"client_id": 2, "client_sql_file_list": ["path1/file1.sql", "path2/file2.sql"]}
        ]
        result = self.dm.get_sql_file_paths_for_all_clients_in_org(123)
        self.assertEqual(result, expected_output)

    @patch('dataset_management.GitHubPuller.get_sql_file_content')
    @patch('dataset_management.DatasetManagement.get_sql_file_paths_for_client')
    def test_execute_sql_files_for_client(self, mock_get_sql_file_paths_for_client, mock_get_sql_file_content):
        mock_get_sql_file_paths_for_client.return_value = ["path1/file1.sql", "path2/file2.sql"]
        mock_get_sql_file_content.side_effect = ["SELECT * FROM table1;", "SELECT * FROM table2;"]
        with patch('builtins.print') as mock_print:
            self.dm.execute_sql_files_for_client(1, 456)
            mock_print.assert_any_call('Execute the below sql in redshift cluster id: 456\n\n"SELECT * FROM table1;"\n')
            mock_print.assert_any_call('Execute the below sql in redshift cluster id: 456\n\n"SELECT * FROM table2;"\n')
            mock_print.assert_any_call("Run metadata generation.")

    # @patch('dataset_management.GitHubPuller.get_sql_file_content')
    # @patch('dataset_management.GitHubPuller.get_sql_files_specific_to_client')
    # @patch('dataset_management.GitHubPuller.get_sql_files_in_org_shell_script')
    # @patch('dataset_management.Hestia.get_org_metadata')
    # @patch('dataset_management.Hestia.get_client_metadata')
    # @patch('dataset_management.Hestia.get_client_ids_for_org')
    # def test_execute_sql_files_for_all_clients_in_org(self,
    #                                                   mock_get_client_ids_for_org,
    #                                                   mock_get_client_metadata,
    #                                                   mock_get_org_metadata,
    #                                                   mock_get_sql_files_in_org_shell_script,
    #                                                   mock_get_sql_files_specific_to_client,
    #                                                   mock_get_sql_file_content
    #                                                   ):
    #     org_id = 123
    #     redshift_cluster_id = 456
    #     client_ids = [1, 2]
    #     sql_file_paths = ['file1.sql', 'file2.sql']
    # 
    #     mock_get_client_ids_for_org.return_value.mock_get_client_ids_for_org.return_value = client_ids
    #     mock_get_client_metadata.side_effect = lambda client_id: {'schema name': f'schema_{client_id}', 'organization id': org_id}
    #     mock_get_org_metadata.return_value.mock_get_org_metadata.return_value = {'schema name': 'org_schema'}
    #     mock_get_sql_files_in_org_shell_script.return_value.mock_get_sql_files_in_org_shell_script.return_value = {'file names': ['file1.sql'], 'file paths': ['path1/file1.sql']}
    #     mock_get_sql_files_specific_to_client.return_value.mock_get_sql_files_specific_to_client.return_value = {'file names': ['file2.sql'], 'file paths': ['path2/file2.sql']}
    #     mock_get_sql_file_content.side_effect = lambda file_path: f'SQL content of {file_path}'
    #
    #     with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
    #         # Act
    #         self.dm.execute_sql_files_for_all_clients_in_org(org_id, redshift_cluster_id)
    #
    #         # Assert
    #         mock_get_client_ids_for_org.assert_called_once_with(org_id)
    #         self.assertEqual(mock_get_sql_file_content.call_count, len(sql_file_paths) * len(client_ids))
    #         calls = [
    #             patch('sys.stdout.write', 'Execute the below sql in redshift cluster id: redshift123\n\n"SQL content of path1/file1.sql"\n'),
    #             patch('sys.stdout.write', 'Execute the below sql in redshift cluster id: redshift123\n\n"SQL content of path2/file2.sql"\n'),
    #             patch('sys.stdout.write', 'Run metadata generation.\n')
    #         ]
    #         mock_stdout.write.assert_has_calls(calls, any_order=False)
