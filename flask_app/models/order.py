from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Order:
    db_name = "bioMarket"
    def __init__(self,data):
        self.id = data['id']
        self.customer = data['customer']
        self.product_name = data['product_name']
        self.quantity = data['quantity']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.product_id = data['product_id']
        self.client_id = data['client_id']
    
    @classmethod
    def make_order(cls,data):
        query = "insert into orders(customer,product_name,quantity,location,product_id, client_id) values (%(customer)s, %(product_name)s, %(quantity)s, %(location)s, %(product_id)s, %(client_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_order_by_id(cls,data):
        query = "select * from orders where id = %(order_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_all_orders(cls):
        query = "select * from orders left join products on orders.product_id = products.id ;"
        result = connectToMySQL(cls.db_name).query_db(query)
        orders = []   
        if result:
            for order in result:
                orders.append(order)
            return orders
        return orders
    
    @classmethod
    def get_all_client_orders(cls, data):
        query = "select * from orders left join clients on orders.client_id = clients.id where orders.client_id = %(client_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        orders = []   
        if result:
            for order in result:
                orders.append(order)
            return orders
        return orders
    
    @classmethod
    def get_order_all_info_by_id(cls, data):
        query = "select * from orders left join products on orders.product_id = products.id where orders.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def update_order(cls, data):
        query = "update orders set customer = %(customer)s, product_name = %(product_name)s, quantity = %(quantity)s, location = %(location)s, product_id = %(product_id)s where id = %(order_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def delete_order(cls, data):
        query = "delete from orders where id = %(order_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def delete_all_client_orders(cls, data):
        query = "delete from orders where client_id = %(client_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(order):
        is_valid = True
        # test whether a field matches the pattern
        
        if len(order['customer'])< 1:
            flash('Customer Name must not be empty', 'customer')
            is_valid = False
        if len(order['quantity'])< 1:
            flash('Quantity must not be empty', 'quantity')
            is_valid = False
        return is_valid