from flask import Flask, render_template, url_for
from dataset_management import DatasetManagement
from github_api import GitHubPuller

app = Flask(__name__)
dm = DatasetManagement()
ghpuller = GitHubPuller()


@app.route("/")
def home():
    org_dict = dm.get_org_metadata(123456789)
    client_list = dm.all_org_metadata["clients"]
    return render_template("index.html", org_dict=org_dict, client_list=client_list)


@app.route("/client/<int:client_id>")
def call_page(client_id):
    client_dict = dm.get_client_metadata(client_id)
    org_dict = dm.get_org_metadata(int(client_dict["organization id"]))
    return render_template("call_page.html", org_dict=org_dict, client_dict=client_dict)


@app.route("/client/update_client_oneviews/<int:client_id>")
def update_client_oneviews(client_id, oneview_list, redshift_cluster_id):
    client_dict = dm.get_client_metadata(client_id)
    org_dict = dm.get_org_metadata(client_dict["organization id"])
    org_shell_oneview_list = ghpuller.get_oneviews_in_org_shell_script(cmx_org_schema_name=org_dict["schema name"])
    print(client_dict)
    print(org_dict)
    print(org_shell_oneview_list)
    # redshift_cluster_id = [n["redshift cluster id"] for n in dm.redshift_clusters
    #                        if int(client_id) == int(client["id"])][0]


# update_client_oneviews(12345, ["thing"], 99999)

if __name__ == "__main__":
    app.run(debug=True)
