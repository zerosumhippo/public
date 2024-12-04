from functools import wraps
import os


def github_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Provides GitHub API authentication details."""
        gh_fg_access_token = os.environ.get("GH_FG_DM_ACCESS_TOKEN")
        gh_auth_details = {
            "gh_fg_access_token": gh_fg_access_token,
            "gh_headers": {
                'Authorization': f'Bearer {gh_fg_access_token}',
                'X-GitHub-Api-Version': '2022-11-28'
            }
        }
        return func(*args, **kwargs, auth=gh_auth_details)
    return wrapper


# def define_repo_contents_path(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         """Returns the repo contents path needed based on the function name."""
#         repo_contents_path = ""
#         if func.__name__ == "get_oneviews_in_org_shell_script":
#             repo_contents_path = f"shell_scripts/{func.cmx_org_schema_name}"
#         elif func.__name__ == "get_client_specific_oneviews":
#             repo_contents_path = f"clients/{func.cmx_org_schema_name}/{func.cmx_client_schema_name}"
#         return func(*args, **kwargs, repo_contents_path)
#     return wrapper
