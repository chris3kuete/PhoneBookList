from flask import Flask, render_template, request, redirect, url_for, jsonify
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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///PhoneBook.db")

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

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contactpage")
def contactpage():
    return render_template("add.html")


@app.route("/finderpage")
def finderpage():
    return render_template("entername.html")


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


@app.route("/search_contact", methods=["GET"])
def search_contact():
    query_num = request.args.get("name")
    result2 = db.session.execute(db.select(list_tbl).where(list_tbl.name == query_num))
    print(result2)
    all_num = result2.scalars().all()
    print(all_num)
    if all_num:
        return render_template("result1.html", all_num=all_num)
        # return jsonify(num1=[n.to_dict() for n in all_num])
    else:
        return "Sorry! This number is not in your phone book"
        # return jsonify(error={"NOT FOUND": "SORRY MISTER!!"}), 404


@app.route("/enterNew/")
def enterNew():
    return render_template("newnumber.html")


@app.route("/updateNumber/<int:id>", methods=["POST", "GET"])
def updateNumber(id):
    if request.method == "POST":
        num_to_update = db.get_or_404(list_tbl, id)
        num_to_update.number = request.form["number"]
        db.session.commit()
        return redirect(url_for('showAll'))
    num = db.get_or_404(list_tbl, id)
    return render_template("newnumber.html", row=num)

    # new_num = request.args.get("new_num")
    # new_num1 = db.get_or_404(list_tbl, id)
    # if new_num1:
    # new_num1.number = new_num
    # new_num2 = new_num1.number
    # db.session.commit()
    # return render_template("newnumber.html", num3=new_num2)
    # else:
    # return "ERROR"


@app.route("/deleteNumber/<int:id>", methods=["POST", "GET"])
def deleteNumber(id):
    name_to_delete = db.get_or_404(list_tbl, id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        return redirect(url_for('showAll'))
    except:

        return "There was an error deleting the record"


if __name__ == "__main__":
    app.run(debug=False)
