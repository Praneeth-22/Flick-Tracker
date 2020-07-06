from flask import make_response, request, redirect, url_for, session
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


def login_required(f):
    # Middleware
    def wrapped_view(self, **kwargs):
        if 'session_id' not in session:
            # if the session_id is not present in clients browser cookie then redirect to login page
            return ({"Unauthorized": "You must be logged in"}, 401)

        else:
            # if the session_id is present then verify it with the database and then only return the f()
            connection = db.get_db()
            cursor = connection.cursor()

            cursor.execute(
                "select session_id from sessions where session_id=%s;",
                (session['session_id'], )
            )
            user = cursor.fetchone()

            # if the already present session_id in clients browser matches with our db then the user is valid
            if user[0] == session['session_id']:
                return f(self, **kwargs)
            else:
                return ({"Unauthorized": "You must be logged in"}, 401)

    return wrapped_view


class RegisterView(MethodView):
    def post(self):
        connection = db.get_db()
        cursor = connection.cursor()

        # Browser checks all the required fields are submitted or not. Hence, following checks may not be required.
        if 'email' not in request.json or request.json['email'] == "":
            return ({'message': 'Provide email address'})
        elif 'first_name' not in request.json or request.json['first_name'] == "":
            return ({'message': 'First Name is required to register'})
        elif 'password' not in request.json or request.json['password'] == "":
            return ({'message': 'Password is required to register'})
        else:
            last_name = ""
            if 'last_name' in request.json:
                last_name = request.json['last_name']

            cursor.execute(
                "select id from users where email = %s;",
                (request.json['email'], )
            )
            user = cursor.fetchone()

            if user is not None:
                return ({'message': 'Email is already used by someone'}, 409)

            else:
                cursor.execute(
                    "insert into users (first_name, last_name, email, password) values (%s, %s, %s, %s);",
                    (request.json['first_name'], last_name, request.json['email'],
                     generate_password_hash(request.json['password']))
                )
                connection.commit()
                return ({"message": "Registered successfully"}, 201)


class LoginView(MethodView):
    def post(self):
        data = request.json
        email = data['email']
        password = data['password']
        # have to sanitize the data and validate them
        error = None

        connection = db.get_db()
        cursor = connection.cursor()

        cursor.execute("select * from users where email=%s;", (email, ))
        user = cursor.fetchone()

        if user is None or not check_password_hash(user[4], password):
            error = "Please check login credentials"

        if error is None:
            session.clear()
            session['session_id'] = user[0]  # user_id
            cursor.execute(
                "insert into sessions (session_id, user_id) values (%s, %s);",
                (session['session_id'], user[0])
            )
            connection.commit()
            return ({"message": "Logged in successfully"}, 200)

        else:
            return ({"message": error}, 401)


def logoutView():
    session_id = session['session_id']
    session.clear()
    # delete from db
    connection = db.get_db()
    cursor = connection.cursor()
    cursor.execute(
        "delete from sessions where session_id=%s;",
        (session_id, )
    )
    connection.commit()
    return ({"Success": "Logged out successfully"})
