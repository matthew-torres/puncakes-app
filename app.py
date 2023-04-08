import db
import os
from flask import Flask, render_template, request, redirect, jsonify, session
from controllers import user_managerment


app = Flask(__name__)
app.secret_key = os.environ.get("API_SECRET")

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

# TODO: fix rendering on failed login 
@app.route("/login", methods=["POST", "GET"])
def customer_login():
    if request.method == "POST":
        data = request.get_json()
        user = db.select_customer_by_uname_pass(data["email"], data["password"]) # retrieve from customers db
        if user: # check if exists
            user_managerment.create_session(user) # create new session
            return redirect(f"/user/customer/{session['id']}") # redirect to their customer page
        else:
            return render_template("login.html", msg='User does not exist.')
    else:
        return render_template("login.html", msg='')

@app.route("/employee_login", methods=["POST", "GET"])
def employee_login():
    if request.method == "POST":
        data = request.get_json()
        user = db.select_employee_by_uname_pass(data["email"], data["password"]) # retrieve from customers db
        if user: # check if exists
            user_managerment.create_session(user) # create new session
            return redirect(f"/user/employee/{session['id']}") # redirect to their customer page
        else:
            return render_template("employee_login.html", msg='User does not exist.')
    else:
        return render_template("employee_login.html", msg='')
    
@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect('/')
    
@app.get("/aboutus")
def get_about_us():
    return render_template("about.html") # place holder

@app.get("/faq")
def get_faq():
    return render_template("faq.html") # place holder

# TODO: fix issue where customer page is not rendered after sign in
@app.get("/user/employee/<eid>")
def get_employee_page(eid):
    employee = db.select_employee_by_eid(eid)
    return render_template("employeeprofile.html", fname=employee[1], jobTitle=employee[6], salary=employee[3])

# TODO: fix issue where customer page is not rendered after sign in
@app.get("/user/customer/<cid>")
def get_customer_page(cid):
    return render_template("about.html")

@app.get("/products/")
def get_product_page():
    products = db.select_all_products()
    return render_template("list_products.html", products=products)


