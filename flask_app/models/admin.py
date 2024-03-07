from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+')

PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Admin:
    db_name = "bioMarket"
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def get_admin_by_email(cls, data):
        query = 'SELECT * FROM admin where email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_admin_by_id(cls, data):
        query = 'SELECT * FROM admin where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
        
    
    @staticmethod
    def validate_user(admin):
        is_valid = True
        if not EMAIL_REGEX.match(admin['email']): 
            flash("Invalid email address!", 'emailLoginAdmin')
            is_valid = False
        if len(admin['password'])<1:
            flash("Password is required!", 'passwordLoginAdmin')
            is_valid = False
        return is_valid