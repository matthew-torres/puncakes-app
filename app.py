import os
import db
from dotenv import load_dotenv

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/employee_signup")
def employee_signup():
    data = request.get_json()
    # TODO: add check box in frontend to determine if manager or staff
    if (employee_type == "manager"):
        db.insert_new_manager(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])
    else:
        db.insert_new_staff(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])
