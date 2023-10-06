from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import Flask
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
import os
import datetime
app = Flask(__name__)

contacts = []

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder, create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///PhoneBook.db"
# os.environ.get("DB_URI", "sqlite:///ContactList.db")

# create the extension
db = SQLAlchemy()
migrate = Migrate(app, db)

# initialize the app with the extension
db.init_app(app)


class list_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    number = db.Column(db.String(250), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.timezone)

    print("created chris table successfully")


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contactpage")
def contactpage():
    return render_template("add.html")


@app.route("/addcontact", methods=['POST'])
def addcontact():
    name = request.form["name"]
    number = request.form["number"]
    date_saved = datetime.datetime.now()
    if name != '' and number != '':
        p = list_tbl(name=name, number=number, date_saved=date_saved)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect('contactpage')


@app.route('/index')
def index():
    profile = list_tbl.query.all()
    return render_template('result.html')


@app.route("/showAll")
def showAll():
    profiles = list_tbl.query.all()
    return render_template("table.html", profiles=profiles)


if __name__ == "__main__":
    app.run(debug=True)
