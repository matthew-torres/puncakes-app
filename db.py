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
                    name        VARCHAR(20),
                    salary      INTEGER,
                    password    VARCHAR(15),
                    startDate   DATE
                );
                CREATE TABLE IF NOT EXISTS  manager (
                    eid         SERIAL PRIMARY KEY,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid)
                );

                CREATE TABLE IF NOT EXISTS  staff (
                    eid         SERIAL REFERENCES employees,
                    jobTitle    VARCHAR(20),
                    FOREIGN KEY (eid) REFERENCES employees(eid)
                );
            """)
            # cursor.execute("""DROP TABLE employees, manager, staff;""")
    
def insert_new_manager(name, salary, password, startDate):
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
                    FOREIGN KEY (eid) REFERENCES employees(eid)
                );
                f"WITH e as (INSERT INTO employees(name, salary, password, startDate) 
                VALUES ({name}, {salary}, {password}, {startDate}) 
                RETURNING eid)
                INSERT INTO manager(eid, jobTitle) SELECT e.eid, {jobTitle} as jobTitle FROM e;"

            """)

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
                    FOREIGN KEY (eid) REFERENCES employees(eid)
                );
                f"WITH e as (INSERT INTO employees(name, salary, password, startDate) 
                VALUES ({name}, {salary}, {password}, {startDate}) 
                RETURNING eid)
                INSERT INTO staff(eid, jobTitle) SELECT e.eid, {jobTitle} as jobTitle FROM e;"

            """)
            