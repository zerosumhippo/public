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
        self.all_org_metadata = {
            "organizations": [
                {
                    "id": 123456789,
                    "pretty name": "Starship Agency",
                    "schema name": "starship_agency"
                },
                {
                    "id": 987654321,
                    "pretty name": "Mars Fleet",
                    "schema name": "mars_fleet"
                }

            ],
            "clients": [
                {
                    "id": 12345,
                    "organization_id": 123456789,
                    "pretty name": "Crush Bugs Corp",
                    "schema name": "crush_bugs_corp"
                },
                {
                    "id": 24689,
                    "organization_id": 123456789,
                    "pretty name": "Ed's Bomb Depot",
                    "schema name": "ed_s_bomb_depot"
                },
                {
                    "id": 35791,
                    "organization_id": 987654321,
                    "pretty name": "Mars Fleet",
                    "schema name": "mars_fleet"
                }
            ]
        }
        self.redshift_clusters = [
            {
                "redshift cluster id": 589,
                "organization id": 123456789
            },
            {
                "redshift cluster id": 603,
                "organization id": 987654321
            }
        ]

    def get_client_metadata(self, client_id):
        return [client for client in self.all_org_metadata["clients"] if int(client_id) == int(client["id"])][0]

    def get_org_metadata(self, org_id):
        return [org for org in self.all_org_metadata["organizations"] if int(org_id) == int(org["id"])][0]
