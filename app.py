import os
import psycopg2, db
from dotenv import load_dotenv

from flask import Flask, render_template, request

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/employee_signup")
def employee_signup():
    data = request.get_json()
    # TOOD: add check box in frontend to determine if manager or staff
    if (employee_type == "manager"):
        db.insert_new_manager(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])
    else:
        db.insert_new_staff(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])
