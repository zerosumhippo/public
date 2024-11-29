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
        self.starship_agency_org_metadata = {
            "organization": {
                "id": 123456789,
                "pretty name": "Starship Agency",
                "schema_name": "starship_agency"
            },
            "clients": [
                {
                    "id": 12345,
                    "pretty name": "Crush Bugs Corp",
                    "schema_name": "crush_bugs_corp"
                },
                {
                    "id": 24689,
                    "pretty name": "Ed's Bomb Depot",
                    "schema_name": "ed_s_bomb_depot"
                }
            ]
        }

    def get_org_metadata(self):
        return self.starship_agency_org_metadata
