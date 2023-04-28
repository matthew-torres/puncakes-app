# Project setup

Mac Commands:
1. Setup Virtual Environment Steps in Windows PowerShell
    - python3 -m venv venv ( on my pc -> 1.1- python -m venv venv )
    - source venv/bin/activate (  on my pc -> 1.2.- venv\Scripts\activate )
    More can be found here: https://realpython.com/python-virtual-environments-a-primer/
2. Install packages
    - pip install -r requirements.txt ( on my pc -> 2.- pip install -r requirements.txt )
3. Create .env file to store secrets 
    - Current secret is URL for ElephantSQL DB and Secret key for flask sessions that are not checked into the Github repo
4. Use command 'flask run' to fire up development server  (on my pc -> 4.- flask run)
5. In any internet browser run the deployed by flask app with http address -> http://127.0.0.1:5000

Flask Documentation: https://flask.palletsprojects.com/en/2.2.x/quickstart/
