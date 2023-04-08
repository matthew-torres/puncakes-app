import db
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/employee_signup", methods=["POST", "GET"])
def employee_signup():
    if request.method == 'POST':
        data = request.get_json() # html form data in json form
        # TODO: add check box in frontend to determine if manager or staff
        if (data["employee_type"] == "manager"):
            db.insert_new_employee(data, manager=1) # passes json object to insert function
            return redirect("/") # placeholder redirect after successful account creation
        elif data["employee_type"] == "staff":
            db.insert_new_employee(data, manager=0)
            return redirect("/")

        return render_template("employee_signup.html", error="Unable to create new employee.") # place holder
    else:
        return render_template('employee_signup.html')

@app.route("/signup", methods=["POST", "GET"])
def customer_signup():
    if request.method == "POST":
        data = request.get_json()
        db.insert_new_customer(data)
        return redirect("/")
    else:
        return render_template("signup.html")
    
@app.get("/aboutus")
def get_about_us():
    return render_template("about.html") # place holder

@app.get("/faq")
def get_faq():
    return render_template("faq.html") # place holder

@app.get("/user/employee/<eid>")
def get_employee_page():
    pass

@app.get("/user/customer/<cid>")
def get_customer_page():
    pass

@app.get("/products/")
def get_product_page():
    pass


