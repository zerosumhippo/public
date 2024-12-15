from github_api import GitHubPuller
from mock_hestia import Hestia
from dataset_management import DatasetManagement
import re

hestia = Hestia()
ghpuller = GitHubPuller()
dm = DatasetManagement()

# print(ghpuller.get_sql_files_in_org_shell_script("mars_fleet"))
# print(ghpuller.get_sql_files_specific_to_client("starship_agency", "crush_bugs_corp"))
# print(len(hestia.all_org_metadata["organizations"]))
print(dm.get_sql_file_paths_for_client(client_id=24689))
# test_str = "shell_scripts/mars_fleet/v_oneview_suppressive_fire.sql"
# temp = re.compile("v_oneview_.*.sql")
# res = temp.search(test_str)
# print(res.group())
# re.compile(f"shell_scripts/mars_fleet/v_oneview.*.sql")
