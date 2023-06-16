from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import post
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.posts = [] 

#! CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL('dojo_wall').query_db(query, data)
        return result

#! READ
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('dojo_wall').query_db(query, data)
        if result:
            return cls(result[0])
        return None

#! VALIDATION
    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        existing_email = connectToMySQL('dojo_wall').query_db(query, user)
        #? First Name Checks
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 letters.", category = 'register')
            is_valid = False
        if not user['first_name'].isalpha():
            flash("Please enter only letters for your first name.", category = 'register')
            is_valid = False
        #? Last Name Checks
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 letters.", category = 'register')
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Please enter only letters for your last name.", category = 'register')
            is_valid = False
        #? Email Checks
        if not EMAIL_REGEX.match(user['email']):
            flash("Please use a valid email format.", category = 'register')
            is_valid = False
        # if User.get_user_by_email(user['email']): #? Could not get this to work this way, needed a workaround.
        if len(existing_email) >= 1:
            flash("This email is already registered. Please try again.", category = 'register')
            is_valid = False
        #? Password Checks
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters.", category = 'register')
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Passwords do not match. Please try again.", category = 'register')
            is_valid = False
        return is_valid