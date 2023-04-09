from flask import session

def create_session(user: tuple, status=False):
            session['loggedin'] = True
            session['id'] = user[0] # index of cid
            session['username'] = user[1] # index of customer name in tuple
            session['user'] = user
            session['employee'] = status
            session['cart'] = list()

def user_logout():
        session.pop('id', None)