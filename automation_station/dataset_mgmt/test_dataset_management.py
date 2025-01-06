import unittest
from dataset_management import DatasetManagement


class TestDatasetManagement(unittest.TestCase):

    def setUp(self):
        self.dataset_management = DatasetManagement()

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
