from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "group-project"
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']

    @classmethod
    def createOne(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def getByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validateRegister(user):
        isValid = True
        users_with_email = User.getByEmail({"email": user['email']})
        if users_with_email:
            flash("Email is already taken")
            isValid = False
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters.")
            isValid = False
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters.")
            isValid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            isValid = False
        if user['password'] != user['confirmPass']:
            flash("passwords must match")
            isValid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            isValid = False
        return isValid

    @staticmethod
    def validate_login(user):
        is_valid = True
        data = {
            'email': user['email']
        }
        user_in_db = User.getByEmail(data)
        if not user_in_db:
            flash("Invalid Email/Passsword")
            is_valid = False
        return is_valid
