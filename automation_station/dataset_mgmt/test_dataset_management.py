import unittest
from unittest.mock import MagicMock, patch
from github_api import GitHubPuller
from mock_hestia import Hestia
from dataset_management import DatasetManagement
from random import randint


class TestDatasetManagement(unittest.TestCase):

    def setUp(self):
        self.dataset_management = DatasetManagement()

        # Mocking Hestia and GitHubPuller
        self.hestia_mock = patch('dataset_management.Hestia').start()
        self.github_mock = patch('dataset_management.GitHubPuller').start()

        self.addCleanup(patch.stopall)

    def test_only_retain_sql_files(self):
        input_data = {
            "file names": ["script1.sql", "script2.txt", "script3.sql"],
            "file paths": ["/path/script1.sql", "/path/script2.txt", "/path/script3.sql"]
        }
        expected_output = {
            "file names": ["script1.sql", "script3.sql"],
            "file paths": ["/path/script1.sql", "/path/script3.sql"]
        }
        result = self.dataset_management._only_retain_sql_files(input_data)
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
        result = self.dataset_management._prioritize_client_folder_over_org_shell(org_shell_contents,
                                                                                  client_folder_contents)
        self.assertEqual(result, expected_output)

    def test_get_sql_file_paths_for_client(self):
        # Mock Hestia responses
        self.hestia_mock.return_value.get_client_metadata.return_value = {
            "schema name": "client_schema",
            "organization id": "org_id"
        }
        self.hestia_mock.return_value.get_org_metadata.return_value = {
            "schema name": "org_schema"
        }

        # Mock GitHubPuller responses
        self.github_mock.return_value.get_sql_files_in_org_shell_script.return_value = {
            "file names": ["script1.sql", "script2.sql"],
            "file paths": ["/path/org/script1.sql", "/path/org/script2.sql"]
        }
        self.github_mock.return_value.get_sql_files_specific_to_client.return_value = {
            "file names": ["script2.sql", "script3.sql"],
            "file paths": ["/path/client/script2.sql", "/path/client/script3.sql"]
        }

        expected_output = ["/path/org/script1.sql", "/path/client/script2.sql", "/path/client/script3.sql"]
        result = self.dataset_management.get_sql_file_paths_for_client(123)
        self.assertEqual(result, expected_output)
#         this is returning an index error...i think its calling the actual hestia module instead of hestiamock
# https://stackoverflow.com/questions/57044593/python-unittest-mock-class-and-class-method
