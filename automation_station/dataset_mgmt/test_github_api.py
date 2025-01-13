import unittest
from unittest.mock import patch
from github_api import GitHubPuller
import requests
import base64


class TestGitHubApi(unittest.TestCase):

    def setUp(self):
        self.puller = GitHubPuller()

    #Adjust these tests to more specifically call out the difference in client vs org scripts.
    @patch('requests.get')
    def test_get_repo_contents_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}
        result = self.puller.get_repo_contents('some/file/path')
        self.assertEqual(result, {'key': 'value'})

    @patch('requests.get')
    def test_get_repo_contents_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException('Error')
        result = self.puller.get_repo_contents('some/file/path')
        self.assertIsNone(result)

    def test_create_file_name_and_path_dict(self):
        response = [
            {'name': 'file1.sql', 'path': 'path1'},
            {'name': 'file2.sql', 'path': 'path2'}
        ]
        expected = {
            "file names": ['file1.sql', 'file2.sql'],
            "file paths": ['path1', 'path2']
        }
        result = self.puller._create_file_name_and_path_dict(response)
        self.assertEqual(result, expected)

    @patch.object(GitHubPuller, 'get_repo_contents')
    def test_get_sql_files_in_org_shell_script(self, mock_get_repo_contents):
        mock_get_repo_contents.return_value = [
            {'name': 'file1.sql', 'path': 'path1'},
            {'name': 'file2.sql', 'path': 'path2'}
        ]
        result = self.puller.get_sql_files_in_org_shell_script('org_schema')
        expected = {
            "file names": ['file1.sql', 'file2.sql'],
            "file paths": ['path1', 'path2']
        }
        self.assertEqual(result, expected)

    @patch.object(GitHubPuller, 'get_repo_contents')
    def test_get_sql_files_specific_to_client(self, mock_get_repo_contents):
        mock_get_repo_contents.return_value = [
            {'name': 'file1.sql', 'path': 'path1'},
            {'name': 'file2.sql', 'path': 'path2'}
        ]
        result = self.puller.get_sql_files_specific_to_client('org_schema', 'client_schema')
        expected = {
            "file names": ['file1.sql', 'file2.sql'],
            "file paths": ['path1', 'path2']
        }
        self.assertEqual(result, expected)

    @patch.object(GitHubPuller, 'get_repo_contents')
    def test_get_sql_file_content(self, mock_get_repo_contents):
        mock_get_repo_contents.return_value = {
            'content': base64.b64encode(b'SELECT * FROM table;').decode('utf-8')
        }
        result = self.puller.get_sql_file_content('some_path')
        self.assertEqual(result, 'SELECT * FROM table;')
