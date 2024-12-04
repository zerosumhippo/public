# Gotta take arguments that identify:
# # client
# # oneview
# # redshift cluster
# Then it would reach into github to grab the SQL
# Then update in Redshift
# Then run metadata generation

class DatasetManagement:
    """Finds OneViews for an agency or client in GitHub and runs the SQL scripts."""

    def __init__(self):
        pass

    def update_client_oneviews(self, client_id, org_shell_oneview_list, redshift_cluster_id):
        pass
