from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Client:
    db_name = "bioMarket"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.customer = data['customer']
        self.email = data['email']
        self.password = data['password']
        self.confirmpassword = data['confirmpassword']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_client(cls,data):
        query = "insert into clients (first_name, last_name, customer, email, password, confirmpassword) values(%(first_name)s, %(last_name)s, %(customer)s, %(email)s, %(password)s, %(confirmpassword)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_client_by_id(cls,data):
        query = "select * from clients where id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_client_by_email(cls,data):
        query = "select * from clients where email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def createPayment(cls,data):
        query = "insert into payments (amount, status, client_id, order_id) VALUES (%(amount)s, %(status)s, %(client_id)s, %(order_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_allUserPayments(cls, data):
        query = "select * from payments where client_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        payments = []
        if results:
            for pay in results:
                payments.append(pay)
        return payments
    
    @staticmethod
    def validate_userRegister(client):
        is_valid = True
        if not EMAIL_REGEX.match(client['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False

        if len(client['first_name']) <= 1:
            flash("First Name is required!", 'nameRegister')
            is_valid = False
        if len(client['last_name']) <= 1:
            flash("Last Name is required!", 'last_nameRegister')
            is_valid = False
        if len(client['customer']) <= 1:
            flash("Bussiness Name is required!", ' bussiness_Register')
            is_valid = False
        if len(client['password']) <= 1:
            flash("Password is required!", 'passwordRegister')
            is_valid = False
        elif not any(char.isdigit() for char in client['password']):
            flash("Password must contain at least 1 number!", 'passwordRegister')
            is_valid = False
        elif not any(char.isupper() for char in client['password']):
            flash("Password must contain at least 1 uppercase letter!", 'passwordRegister')
            is_valid = False
            
        if len(client['confirmpassword'])<=1 or client['confirmpassword'] != client['password']:
            flash("Confirm password is incorrect!", 'passwordConfirm')
            is_valid = False
        if len(client['first_name'])<1:
            flash("First name is required!", 'nameRegister')
            is_valid = False
        if len(client['last_name'])<1:
            flash("Last name is required!", 'lastNameRegister')
            is_valid = False
        return is_valid
#till now we made all the validations for user registrations

    @staticmethod
    def validate_user(client):
        is_valid= True
        if not EMAIL_REGEX.match(client['email']): 
            flash("Invalid email address!", 'emailLogin')
            is_valid = False
        if len(client['password'])<1:
            flash("Password is required!", 'passwordLogin')
            is_valid = False
        return is_valid
#this is the validation for the login