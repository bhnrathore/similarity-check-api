from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017/')
db = client.SimilarityDB
users = db["Users"]

class Register(Resource):
    def post(self):
        data = request.get_json()


        username = data.get('username')
        password = data.get('password')


        # Check if the user already exists
        if users.find_one({"Username": username}):
            return {'message': 'User already exists', "status": 301}

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the user in the database
        users.insert_one({
            "Username": username, 
            "Password": hashed_password,
            "Tokens": 6
            })

        return {'message': 'User registered successfully', "status": 200}
    
class Detect(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        text1 = data.get('text1')
        text2 = data.get('text2')

        # Check if the user exists
        user = users.find_one({"Username": username})
        if not user:
            return {'message': 'User not found', "status": 301}

        # Check if the password is correct
        if not bcrypt.checkpw(password.encode('utf-8'), user['Password']):
            return {'message': 'Incorrect password', "status": 302}

        # Check if the user has enough tokens
        if user['Tokens'] <= 0:
            return {'message': 'Not enough tokens, please refill', "status": 303}

        # Deduct a token
        users.update_one({"Username": username}, {"$inc": {"Tokens": -1}})

        # Here you would call your detection function
        # For demonstration, we'll just return a dummy response
        #using spacy

        nlp = spacy.load("en_core_web_sm")
        doc1 = nlp(text1)
        doc2 = nlp(text2)

        # Ratio is a number between 0 and 1, where 1 means identical
        # and 0 means completely different
        # You can use different methods to calculate similarity
        ratio = doc1.similarity(doc2)
        return {"similarity": ratio, "msg": "Similarity score calculated","status": 200}
    
class Refill(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        admin_password = data.get('admin_pw')
        refill_amout = data.get('refill')

        # Check if the user exists
        user = users.find_one({"Username": username})
        if not user:
            return {'message': 'User not found', "status": 301}

        checked_pw = "admin"
        # Check if the password is correct
        if not admin_password == checked_pw:
            return {'message': 'Incorrect admin password', "status": 304}
        # Refill current tokens ny incrementing it by refill amount
        users.update_one({"Username": username}, {"$inc": {"Tokens": refill_amout}})

        return {'message': 'Tokens refilled successfully', "status": 200}
    
api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)