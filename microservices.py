import sqlite3

import flask
from flask_bcrypt import Bcrypt
from flask import request, jsonify, g, current_app, make_response
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)
app.config["DEBUG"] = True
bcrypt = Bcrypt(app)


# Check for Authentication when needed.
class Authentication(BasicAuth):
    def check_credentials(self, username, password):
        print('check_credentials')
        # query from database
        query = "SELECT * from users where username ='{}'".format(username)
        user = query_db(query)
        if user == []:
            return False
        # if user[0]['username'] and bcrypt.check_password_hash(user[0]["password"], 'password'):
        if user[0]['password'] == password:
            print("Hit")
            current_app.config['BASIC_AUTH_USERNAME'] = username
            current_app.config['BASIC_AUTH_PASSWORD'] = password
            return True
        else:
            print("FALSE HIT")
            return False


basic_auth = Authentication(app)
DATABASE = './init.db'


# Function Connect Database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Function  execute script
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Create Command initdb
# To use command, run in terminal (export FLASK_APP=appname) Or (Set FLASK_APP=appname)
# flask init_db
@app.cli.command('init_db')
def initdb_command():
    init_db()
    print('Initialize the database.')


# This function returns items from the database
# as dictionaries instead of lists (Better for outputting to JSON)
# Procedure taken from the programming historian website:
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Function using for query database
# Fetch each data one by one based on the query provided
def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    fetch = cur.execute(query).fetchall()
    return fetch


@app.route("/")
def hello():
    return "Hello World!"


# Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    # hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

    username = data['username']
    password = data['password']

    query = 'SELECT username FROM users'
    listusername = query_db(query)
    for user_name in listusername:
        if user_name['username'] == username:
            error = '409 A username already exists'
            return make_response(jsonify({'error': error}), 409)
    db = get_db()
    db.execute('insert into users(username, password) values (?,?)', (username, password))
    db.commit()

    response = make_response('Success: account created')
    response.status_code = 201
    return response


# Change User Password
@app.route('/users/<string:user>', methods=['PUT'])
@basic_auth.required
def change_password(user):
    data = request.get_json(force=True)
    # newpassword = bcrypt.generate_password_hash('password').decode('utf-8')
    newpassword = data['password']
    creator = current_app.config['BASIC_AUTH_USERNAME']

    # check if username is in database
    query = "SELECT Id FROM USERS WHERE username = '{}'".format(str(user))
    useracc = query_db(query)
    if not useracc:
        error = '404 No user exists with the user of ' + str(user)
        return make_response(jsonify({'error': error}), 404)

    # Check if the username is the same with account authenticated
    if creator == str(user):
        db = get_db()
        print("=======================")
        db.execute("UPDATE users SET password= ? WHERE username= ?", (newpassword, str(user)))
        db.commit()
        response = make_response("Success: User password Changed")
        response.status_code = 201
        return response
    error = '409 CONFLICT Authenticated Account does not match user ' + str(user)
    return make_response(jsonify({'error': error}), 409)


# Delete User
@app.route('/users/<string:user>', methods=['DELETE'])
@basic_auth.required
def delete_user(user):
    # data = request.get_json(force=True)
    creator = current_app.config['BASIC_AUTH_USERNAME']

    # check if username is in database
    query = "SELECT Id FROM USERS WHERE username = '{}'".format(str(user))
    user_acc = query_db(query)
    if not user_acc:
        error = '404 No user exists with the user of ' + str(user)
        return make_response(jsonify({'error': error}), 404)

    # Check if the username is the same with account authenticated
    if creator == str(user):
        db = get_db()
        print("=======================")
        db.execute("DELETE FROM users WHERE username= '{}'".format(str(user)))
        db.commit()
        response = make_response("Success: User account deleted")
        response.status_code = 201
        return response
    error = '409 CONFLICT Authenticated Account does not match user ' + str(user)
    return make_response(jsonify({'error': error}), 409)


@app.route('/articles', methods=['POST'])
@basic_auth.required
def articles():
    pass


if __name__ == "__main__":
    app.run(debug=True)
