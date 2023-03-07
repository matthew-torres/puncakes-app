import os
import db

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.post("/employee_signup")
def employee_signup():
    data = request.get_json()
    # TODO: add check box in frontend to determine if manager or staff
    if (data["employee_type"] == "manager"):
        db.insert_new_manager(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])
    else:
        db.insert_new_staff(data["name"], data["salary"], data["password"], data["startDate"], data["jobTitle"])

@app.post("/customer_signup")
def customer_signup():
    data = request.get_json()
    db.insert_new_customer(data["name"], data["password"], data["email"], data["phoneNum"], data["street"], data["city"], data["state"], data["zip"])


app.get("/user/employee/<eid>")
def get_employee_page():
    pass

app.get("/user/customer/<cid>")
def get_customer_page():
    pass

app.get("/products/")
def get_product_page():
    pass


