import unittest
from github_api import GitHubPuller
from mock_hestia import Hestia
from random import randint

hestia = Hestia()
ghpuller = GitHubPuller()


class GetSQLFileListTest(unittest.TestCase):

    def setUp(self):
        self.random_organization_schema_name = [org["schema name"] for org
                                                in hestia.all_org_metadata["organizations"]
                                                ][randint(0, (len(hestia.all_org_metadata["organizations"]) - 1))]
        self.org_shell_script_sql_file_list = ghpuller.get_sql_files_in_org_shell_script(
            self.random_organization_schema_name)

    def tearDown(self):
        self.random_organization_schema_name = ""
        self.org_shell_script_sql_file_list = []

    def test_org_shell_script_list_not_empty(self):
        self.assertNotEqual(self.org_shell_script_sql_file_list, [], "Organization shell script list is empty.")
