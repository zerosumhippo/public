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
