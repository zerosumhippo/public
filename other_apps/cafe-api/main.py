from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL, AnyOf
import os
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db = SQLAlchemy()  # SQLAlchemy(app)
db.init_app(app)

API_KEY = os.environ.get("API_KEY")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# with app.create_connect():
#     db.create_all()


class AddCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = URLField("Map URL For Cafe", validators=[URL()])
    img_url = URLField("Image URL For Cafe", validators=[URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    has_toilet = BooleanField("Cafe Has Toilet?")
    has_wifi = BooleanField("Cafe Has Wifi?")
    has_sockets = BooleanField("Cafe Has Power Outlets?")
    can_take_calls = BooleanField("Can Take Calls in Cafe?")
    coffee_price = StringField("Price of Black Cup of Coffee (e.g. $5.25)", validators=[DataRequired()])
    submit = SubmitField(label="Add Cafe")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafe_dict = {"cafes": []}
    for cafe in all_cafes:
        ind_cafe = {
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        }
        cafe_dict["cafes"].append(ind_cafe)
    return jsonify(cafe_dict)


@app.route("/search")
def search_cafes():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    query_result = result.scalars().all()
    if not query_result:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
    else:
        cafe_dict = {"cafes": []}
        for cafe in query_result:
            ind_cafe = {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price,
            }
            cafe_dict["cafes"].append(ind_cafe)
        return jsonify(cafe_dict)


@app.route("/add", methods=["GET", "POST"])
def add_new_cafe():
    form = AddCafeForm()
    if form.validate_on_submit() and request.method == "POST":
        boolean_field_dict = {}
        max_id = db.session.query(func.max(Cafe.id)).scalar()
        for field in form:
            if field.type == "BooleanField":
                try:
                    request.form[field.name]
                except KeyError:
                    boolean_field_dict[field.name] = False
                else:
                    boolean_field_dict[field.name] = True
        new_cafe = Cafe(id=(int(max_id) + 1),
                        name=request.form["name"],
                        map_url=request.form["map_url"],
                        img_url=request.form["img_url"],
                        location=request.form["location"],
                        seats=request.form["seats"],
                        has_toilet=boolean_field_dict["has_toilet"],
                        has_wifi=boolean_field_dict["has_wifi"],
                        has_sockets=boolean_field_dict["has_sockets"],
                        can_take_calls=boolean_field_dict["can_take_calls"],
                        coffee_price=request.form["coffee_price"])
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe."})
    return render_template("add_cafe.html", form=form)


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("coffee_price")
    cafe_to_update = db.session.get(Cafe, cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": f"Successfully updated the coffee price for {cafe_to_update.name} "
                                            f"to {new_price}."}), 200
    else:
        return jsonify(response={"Error": f"Sorry, a cafe with ID {cafe_id} does not exist in the database."}), 404


@app.route("/delete-cafe/<int:cafe_id>", methods=["GET", "DELETE"])
def delete_cafe(cafe_id):
    user_api_key = request.args.get("api-key")
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if cafe_to_delete and user_api_key == API_KEY:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"Success": f"Successfully deleted the record for {cafe_to_delete.name}."}), 200
    elif user_api_key != API_KEY:
        return jsonify(response={"Error": f'Sorry, "{user_api_key}" is not a valid API key.'}), 403
    else:
        return jsonify(response={"Error": f"Sorry, a cafe with ID {cafe_id} does not exist in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
