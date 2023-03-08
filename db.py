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
                    eid         SERIAL PRIMARY KEY,
                    name "      VARCHAR(20),
                    salary      INTEGER,
                    password    VARCHAR(15),
                    startDate   DATE
                );
                CREATE TABLE IF NOT EXISTS manager (
                    eid         SERIAL PRIMARY KEY,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS staff (
                    eid         SERIAL REFERENCES employees,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS customers (
                    cid         SERIAL PRIMARY KEY,
                    name        VARCHAR(20),
                    password    VARCHAR(20),
                    email       VARCHAR(20),
                    phoneNum    CHAR(10),
                    street      VARCHAR(20),
                    city        VARCHAR(15),
                    state       CHAR(2),
                    zip         CHAR(5)    
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
        
    
def insert_new_manager(name, salary, password, startDate, jobTitle):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                 CREATE TABLE IF NOT EXISTS employees (
                    eid         SERIAL PRIMARY KEY,
                    name        VARCHAR(20),
                    salary      INTEGER,
                    password    VARCHAR(15),
                    startDate   DATE
                );
                CREATE TABLE IF NOT EXISTS  manager (
                    eid         SERIAL PRIMARY KEY,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid) ON DELETE CASCADE
                );
                WITH e as (INSERT INTO employees(name, salary, password, startDate) 
                VALUES (%s, %s, %s, %s)
                RETURNING eid)
                INSERT INTO manager(eid, jobTitle) SELECT e.eid, %s  as jobTitle FROM e;
            """, (name, salary, password, startDate, jobTitle,))

def insert_new_staff(name, salary, password, startDate, jobTitle):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                 CREATE TABLE IF NOT EXISTS employees (
                    eid         SERIAL PRIMARY KEY,
                    name        VARCHAR(20),
                    salary      INTEGER,
                    password    VARCHAR(15),
                    startDate   DATE
                );
                CREATE TABLE IF NOT EXISTS  staff (
                    eid         SERIAL PRIMARY KEY,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid) ON DELETE CASCADE
                );
                WITH e as (INSERT INTO employees(name, salary, password, startDate) 
                VALUES (%s, %s, %s, %s) 
                RETURNING eid)
                INSERT INTO staff(eid, jobTitle) SELECT e.eid, %s as jobTitle FROM e;
            """, (name, salary, password, startDate, jobTitle,))

def insert_new_customer(name, password, email, phone_num, street, city, state, zip):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS customers (
                    cid         SERIAL PRIMARY KEY,
                    name        VARCHAR(20),
                    password    VARCHAR(20),
                    email       VARCHAR(20),
                    phoneNum    CHAR(10),
                    street      VARCHAR(20),
                    city        VARCHAR(15),
                    state       CHAR(2),
                    zip         CHAR(5)    
                );
                INSERT INTO customers(name, password, email, phoneNum, street, city, state, zip) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
            """, (name, password, email, phone_num, street, city, state, zip,))

            