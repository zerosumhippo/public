from flask import Flask, render_template, url_for
from mock_hestia import Hestia
from github_api import GitHubPuller
from dataset_management import DatasetManagement

app = Flask(__name__)
hestia = Hestia()
ghpuller = GitHubPuller()
dm = DatasetManagement()


@app.route("/")
def home():
    org_dict = hestia.get_org_metadata(123456789)
    client_list = hestia.all_org_metadata["clients"]
    return render_template("index.html", org_dict=org_dict, client_list=client_list)


@app.route("/client/<int:client_id>")
def call_page(client_id):
    client_dict = hestia.get_client_metadata(client_id)
    org_dict = hestia.get_org_metadata(int(client_dict["organization id"]))
    return render_template("call_page.html", org_dict=org_dict, client_dict=client_dict)


@app.route("/client/update_client_oneviews/<int:client_id>")
def update_client_oneviews(client_id):
    client_dict = hestia.get_client_metadata(client_id)
    org_dict = hestia.get_org_metadata(client_dict["organization id"])
    org_shell_oneview_list = ghpuller.get_oneviews_in_org_shell_script(cmx_org_schema_name=org_dict["schema name"])
    client_oneview_list = ghpuller.get_client_specific_oneviews(cmx_org_schema_name=org_dict["schema name"],
                                                                cmx_client_schema_name=client_dict["schema name"])
    org_shell_oneview_list_no_path = []
    for n in range(len(org_shell_oneview_list)):
        oneview_without_path = org_shell_oneview_list[n][::-1].split("/", 1)[0][::-1]
        print(oneview_without_path)
        org_shell_oneview_list_no_path += oneview_without_path
    print(org_shell_oneview_list)
    print(org_shell_oneview_list_no_path)


update_client_oneviews(12345)

# if __name__ == "__main__":
#     app.run(debug=True)
