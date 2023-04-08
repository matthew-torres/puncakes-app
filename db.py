import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS employees (
                eid             SERIAL PRIMARY KEY NOT NULL,
                fname           VARCHAR(20),
                lname           VARCHAR(25) NOT NULL,
                salary          NUMERIC(8,2),
                email           VARCHAR(20) NOT NULL,
                phone_number    VARCHAR(20),
                jobTitle        VARCHAR(20),
                password        VARCHAR(15),
                startDate       DATE NOT NULL,
                manager         INTEGER,
                CONSTRAINT emp_salary_min CHECK (salary > 0),
                CONSTRAINT emp_email_uk UNIQUE (email)
            );

            CREATE TABLE IF NOT EXISTS jobTitle (
                jid         SERIAL PRIMARY KEY NOT NULL,
                jobTitle    VARCHAR(30) NOT NULL,
                minSalary   MONEY,
                maxSalary   MONEY
            );

            CREATE TABLE IF NOT EXISTS products (
                pid             SERIAL PRIMARY KEY NOT NULL,
                name            varchar(50) NOT NULL,
                qtyStock        INTEGER NOT NULL,
                expireDate      DATE NOT NULL,
                price           NUMERIC(5,2),
                nutritionFacts  VARCHAR(1000) NOT NULL,
                description     VARCHAR(1000)
            );

            CREATE TABLE IF NOT EXISTS customers (
                cid             SERIAL PRIMARY KEY NOT NULL,
                name            VARCHAR(100) NOT NULL,
                phoneNum        CHAR(10),
                password        VARCHAR(20),
                email           VARCHAR(20) NOT NULL,
                street          VARCHAR(20),
                city            VARCHAR(15),
                state           CHAR(2),
                zip             CHAR(5)
            );

            CREATE TABLE IF NOT EXISTS orderStatus (
                osid            INTEGER PRIMARY KEY NOT NULL,
                status          VARCHAR(30)
            );

            CREATE TABLE IF NOT EXISTS orders (
                oid             SERIAL PRIMARY KEY NOT NULL,
                cid             INTEGER NOT NULL,
                orderTotal      MONEY,
                timePlaced      TIMESTAMP(0) NOT NULL,
                timeDone        TIMESTAMP(0),
                orderStatus     INTEGER,
                CONSTRAINT fk_orders_customers FOREIGN KEY (cid) REFERENCES customers(cid),
                CONSTRAINT fk_orders_orderStatus FOREIGN KEY (orderStatus) REFERENCES orderStatus(osid)  
            );

            CREATE TABLE IF NOT EXISTS orderItems (
                oid             INTEGER NOT NULL,
                pid             INTEGER NOT NULL,
                qty             INTEGER NOT NULL,
                CONSTRAINT pk_orderItems PRIMARY KEY (oid, pid),
                CONSTRAINT fk_orderItems_order FOREIGN KEY(oid) REFERENCES orders(oid),
                CONSTRAINT fk_orderItems_product FOREIGN KEY(pid) REFERENCES products(pid)
            );

            CREATE TABLE IF NOT EXISTS shifts (
                sid             INTEGER PRIMARY KEY NOT NULL,
                shiftStartTime  TIME NOT NULL,
                shiftEndTime    TIME NOT NULL
            );

            CREATE TABLE IF NOT EXISTS employeeShifts (
                eid             INTEGER NOT NULL,
                sid             INTEGER NOT NULL,
                beginDate       DATE NOT NULL,       
                endDate         DATE NOT NULL,
                CONSTRAINT pk_employeeShifts PRIMARY KEY(eid, sid),
                CONSTRAINT fk_employeeShifts_employee FOREIGN KEY(eid) REFERENCES employees(eid),
                CONSTRAINT fk_employeeShifts_shifts FOREIGN KEY(sid) REFERENCES shifts(sid)
            );

            CREATE TABLE IF NOT EXISTS reviews (
                rid             SERIAL PRIMARY KEY NOT NULL,
                cid             INTEGER NOT NULL,
                pid             INTEGER NOT NULL,
                rating          INTEGER NOT NULL,
                comments        varchar(2000),
                CONSTRAINT check_rating 
                    CHECK (rating BETWEEN 0 AND 5),
                CONSTRAINT fk_reviews_customer FOREIGN KEY(cid) REFERENCES customers(cid),
                CONSTRAINT fk_reviews_product FOREIGN KEY(pid) REFERENCES products(pid)
            );
            """)


def __drop_table__(table: str):
    choice = input("Are you sure you want to drop table {table}?(y/n)\n")
    if (choice.lower() == 'y'):
        with connection:
            with connection.cursor() as cursor:
                print(f"dropping {table}...")
                cursor.execute(f"DROP TABLE {table}")
                print(f"{table} dropped.")


def insert_new_employee(data: any, manager: int) -> None:
    '''
    Inserts new employee into the employees table
    Parameters:
        data: json object containing form data from employee_signup.html
        manager: bool value to denote whether insertion is classified as a manager
    Returns:
        None
    '''
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                eid             SERIAL PRIMARY KEY NOT NULL,
                fname           VARCHAR(20),
                lname           VARCHAR(25) NOT NULL,
                salary          NUMERIC(8,2),
                email           VARCHAR(20) NOT NULL,
                phone_number    VARCHAR(20),
                jobTitle        VARCHAR(20),
                password        VARCHAR(15),
                startDate       DATE NOT NULL,
                manager         INTEGER,
                CONSTRAINT emp_salary_min CHECK (salary > 0),
                CONSTRAINT emp_email_uk UNIQUE (email)
            );
                INSERT INTO employees(fname, lname, salary, email, phone_number, jobTitle, password, startDate, manager) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (data['fname'], data['lname'], data['salary'], data['email'], data['phone_number'], data['jobTitle'], data['password'], data['startDate'], manager,))

def insert_new_customer(data: any) -> None:
    '''
    Inserts new employee into employees table

    Parameters:
        data: json object containing form data from signup.html
    Returns:
        None
    '''
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS customers (
                cid             SERIAL PRIMARY KEY NOT NULL,
                name            VARCHAR(100) NOT NULL,
                phoneNum        CHAR(10),
                password        VARCHAR(20),
                email           VARCHAR(20) NOT NULL,
                street          VARCHAR(20),
                city            VARCHAR(15),
                state           CHAR(2),
                zip             CHAR(5)
            );
                INSERT INTO customers(name, phoneNum, password, email, street, city, state, zip) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
            """, (data['name'], data['phoneNum'], data['password'], data['email'], data['street'], data['city'], data['state'], data['zip'],))
