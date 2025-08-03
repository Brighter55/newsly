from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from sqlalchemy.exc import IntegrityError
from helper import is_valid_email
from dotenv import load_dotenv
import os
from pathlib import Path
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)
# connect to local postgresDB for development phase
root_dir = Path(__file__).resolve().parents[1]
load_dotenv(root_dir / ".env")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRESDB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# model for table storing users' gmail
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    categories = db.Column(JSON, nullable=False)

# create table once
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        # validate email server-side
        if not is_valid_email(email):
            return jsonify({"success": False, "error_message": "Email is not valid"})
        # get user's category preference and check if user select at least one category
        categories = request.form.getlist("categories")
        if not categories:
            return jsonify({"success": False, "error_message": "Please select at least one category"})

        # check if email is already in database
        try:
            # insert user's info to postgresDB
            new_user = User(email=email, categories=categories)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"success": False, "error_message": "Email is already taken"})
        return jsonify({"success": True})
    return render_template("index.html")

@app.route("/summary/<string:news_id>")
def summary(news_id):
    # get news data from mongodb
    # direct user to "full_summary.html"
    client = MongoClient("localhost", 27017)
    db = client.testdb
    collection = db.summaries
    news = collection.find({"_id": ObjectId(news_id)})[0]
    return render_template("full_summary.html", news=news)


if __name__ == "__main__":
    app.run(debug=True)
