from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starship_agency.db"
db.init_app(app)


class Table1(db.Model):
    field1 = db.Column(db.Integer, primary_key=True)
    field2 = db.Column(db.String(250), nullable=True)
    field3 = db.Column(db.Float, nullable=True)
    field4 = db.Column(db.Float, nullable=True)


class Table2(db.Model):
    field1 = db.Column(db.Integer, primary_key=True)
    field2 = db.Column(db.String(250), nullable=True)
    field3 = db.Column(db.Float, nullable=True)
    field4 = db.Column(db.Float, nullable=True)


class Table3(db.Model):
    field1 = db.Column(db.Integer, primary_key=True)
    field2 = db.Column(db.String(250), nullable=True)
    field3 = db.Column(db.Float, nullable=True)
    field4 = db.Column(db.Float, nullable=True)


with app.app_context():
    db.create_all()

# with app.app_context():
#     new_entry = Table3(field1=1, field2="Chill, bro.", field3=123.45, field4=986.3)
#     db.session.add(new_entry)
#     db.session.commit()

with app.app_context():
    entry = db.session.execute(db.select(Table3).where(Table3.field1 == 1)).scalar()
    print(entry.field2)

#  how to create a view
with app.app_context():
    db.engine.execute("""
        CREATE VIEW IF NOT EXISTS my_view 
        AS
        SELECT column1, column2
        FROM table1
        WHERE condition;
    """)

# query a view without a model
# results = db.session.execute(db.select(db.text("SELECT * FROM my_view_name"))).scalars().all()
