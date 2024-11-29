from flask import Flask, render_template, url_for
from dataset_management import DatasetManagement

app = Flask(__name__)
dm = DatasetManagement()


@app.route("/")
def home():
    org_dict = dm.get_org_metadata()
    return render_template("index.html", org_dict=org_dict)


@app.route("/client/<int:client_id>")
def call_page(client_id):
    print(client_id)
    org_dict = dm.get_org_metadata()
    client_name = [client["pretty name"] for client in org_dict["clients"] if int(client_id) == int(client["id"])][0]
    return render_template("call_page.html", client_name=client_name, client_id=client_id)


if __name__ == "__main__":
    app.run(debug=True)
