from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


class Analyse:
    db_name = "bioMarket"
    def __init__(self,data):
        self.id = data['id']
        self.product_name = data['product_name']
        self.pesticide = data['pesticide']
        self.allowed = data['allowed']
        self.allowedAmount = data['allowedAmount']
        self.constatedAmount = data['constatedAmount']
        self.control = data['control']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.product_id = data['product_id']
    
    @classmethod
    def create_analyse(cls,data):
        query = "insert into analyses (product_name, pesticide, allowed, allowedAmount, constatedAmount, control, product_id) values(%(product_name)s, %(pesticide)s, %(allowed)s, %(allowedAmount)s, %(constatedAmount)s, %(control)s, %(product_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_analyse_by_id(cls,data):
        query = "select * from analyses where id = %(analyse_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_all_analyses(cls):
        query = "select * from analyses left join products on analyses.product_id = products.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        analyses = []   
        if result:
            for analyse in result:
                analyses.append(analyse)
            return analyses
        return analyses

    @classmethod
    def get_all_product_analyses(cls, data):
        query = "select * from analyses left join products on analyses.product_id = products.id where analyses.product_id = %(product_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        analyses = []
        if results:
            for analyse in results:
                analyses.append( analyse )
            return analyses
        return analyses

    @classmethod
    def update_analyse(cls, data):
        query = "update analyses set product_name = %(product_name)s, pesticide = %(pesticide)s, allowed = %(allowed)s, allowedAmount = %(allowedAmount)s, constatedAmount = %(constatedAmount)s, control = %(control)s, product_id = %(product_id)s where id = %(analyse_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_analyse(cls, data):
        query = "delete from analyses where id = %(analyse_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def delete_all_product_analyses(cls, data):
        query = "delete from analyses where product_id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(analyse):
        is_valid = True
        # test whether a field matches the pattern
        
        if len(analyse['product_name'])< 2:
            flash('Product Name must be more than 2 characters', 'product_name')
            is_valid = False
        if len(analyse['pesticide'])< 1:
            flash('Pesticide Name must not be more empty', 'pesticide')
            is_valid = False
        if len(analyse['allowed'])< 1:
            flash('Allowed must not be more empty', 'allowed')
            is_valid = False
        if len(analyse['allowedAmount'])< 1:
            flash('Allowed Amount must not be more empty', 'allowedAmount')
            is_valid = False
        if len(analyse['constatedAmount'])< 1:
            flash('Constated Amount must not be more empty', 'constatedAmount')
            is_valid = False
        if len(analyse['control'])< 1:
            flash('Control Date must not be more empty', 'control')
            is_valid = False
        return is_valid