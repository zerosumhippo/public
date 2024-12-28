import unittest
from github_api import GitHubPuller
from mock_hestia import Hestia
from random import randint


class TestGitHubApi(unittest.TestCase):

    def setUp(self):
        self.hestia = Hestia()
        self.github = GitHubPuller()
        self.random_organization_list_index = randint(0, (len(self.hestia.all_org_metadata["organizations"]) - 1))
        self.random_organization_schema_name = [org["schema name"] for org
                                                in self.hestia.all_org_metadata["organizations"]
                                                ][self.random_organization_list_index]
        self.random_organization_id = [org["id"] for org in self.hestia.all_org_metadata["organizations"]
                                       ][self.random_organization_list_index]
        self.random_organization_client_list = [client["schema name"] for client
                                                in self.hestia.all_org_metadata["clients"]
                                                if client["organization id"] == self.random_organization_id]
        self.random_client_list_index = randint(0, (len(self.random_organization_client_list) - 1))
        self.random_client_schema_name = self.random_organization_client_list[self.random_client_list_index]
        self.org_shell_script_sql_file_list = self.github.get_sql_files_in_org_shell_script(
            self.random_organization_schema_name)
        self.client_specific_sql_file_list = self.github.get_sql_files_specific_to_client(
            self.random_organization_schema_name, self.random_client_schema_name
        )

    def tearDown(self):
        self.random_organization_list_index = None
        self.random_organization_schema_name = ""
        self.random_organization_id = None
        self.random_organization_client_list = []
        self.random_client_list_index = None
        self.random_client_schema_name = ""
        self.org_shell_script_sql_file_list = []
        self.client_specific_sql_file_list = []

    def test_org_shell_script_list_not_empty(self):
        self.assertNotEqual(self.org_shell_script_sql_file_list, [], "Organization shell script list is empty.")
