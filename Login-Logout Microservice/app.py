from flask import Flask, jsonify, request
import pymongo
import json


#MongoDB connection 
connection_url = 'mongodb+srv://ligonj:<password>@logins.izpmd.mongodb.net/'
client = pymongo.MongoClient(connection_url)

#Database
db = client.get_database("logins")
#Collection
logins = db.logins

app = Flask(__name__)

@app.route('/createUserLogin', methods = ['POST'])
def createUserLogin():
    entered_login = request.get_json()
    username = entered_login.get('username')
    password = entered_login.get('password')

    if logins.find_one({'username': username}):
        return jsonify ({'message': f'This user already exists. Please enter a different username.'}), 401

    else:
        logins.insert_one({'username':username, 'password':password})
        return jsonify ({'message': f'Username and password successfully created.'}), 201

@app.route('/login', methods = ['POST'])
def login():
    entered_login = request.get_json()
    username = entered_login.get('username')
    password = entered_login.get('password')

    if logins.find_one({'username':username, 'password':password}):
        return jsonify({'message': f'Login successful'}), 200
    else:
        return jsonify({'message': f'Incorrect username or password'}), 401

if __name__ == "__main__":
    app.run(port=5001, debug=True)


