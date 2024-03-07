from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
import re


class Product:
    db_name = "bioMarket"
    def __init__(self,data):
        self.id = data['id']
        self.product_name = data['product_name']
        self.quantity = data['quantity']
        self.storage = data['storage']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_product(cls,data):
        query = "insert into products (product_name, quantity, storage, price) values(%(product_name)s, %(quantity)s, %(storage)s, %(price)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_product_by_id(cls,data):
        query = "select * from products where id = %(product_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_all_products(cls):
        query = "select * from products;"
        result = connectToMySQL(cls.db_name).query_db(query)
        products = []   
        if result:
            for product in result:
                products.append(product)
            return products
        return products

    @classmethod
    def update_product(cls, data):
        query = "update products set product_name = %(product_name)s, quantity = %(quantity)s, storage = %(storage)s, price = %(price)s WHERE id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "delete from products where id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_user(product):
        is_valid = True
        
        if len(product['product_name'])< 1:
            flash('Product Name must not be empty', 'product_name')
            is_valid = False
        if len(product['quantity'])< 1:
            flash('Quantity must not be more empty', 'quantity')
            is_valid = False
        if len(product['storage'])< 1:
            flash('Storage Date must not be more empty', 'storage')
            is_valid = False
        if len(product['price'])< 1:
            flash('Price must not be more empty', 'price')
            is_valid = False
        return is_valid