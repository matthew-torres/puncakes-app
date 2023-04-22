# Project setup

Mac Commands:
1. Setup Virtual Environment
    - python3 -m venv venv
    - source venv/bin/activate
    More can be found here: https://realpython.com/python-virtual-environments-a-primer/
2. Install packages
    - pip install -r requirements.txt
3. Create .env file to store secrets which are the following:
    - Current secret is URL for ElephantSQL DB : DATABASE_URL=[URL]
    - Secret key for flask sessions that are not checked into the Github repo : API_SECRET=[random string]
4. Use command 'flask run' to fire up development server

Flask Documentation: https://flask.palletsprojects.com/en/2.2.x/quickstart/
