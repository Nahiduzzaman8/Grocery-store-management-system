import mysql.connector
from get_sql_connection import connect_to_db




def get_all_data_from_orders(cnx):
    cursor = cnx.cursor(dictionary = True) 
    
    order_query = """SELECT orders.order_id, customers.customer_name, orders.total, orders.datetime FROM orders
                    inner join customers
                    on orders.customers_id = customers.customer_id """   
    cursor.execute(order_query) 
    
    orders = cursor.fetchall()      
    return orders


#delete
def delete_data_from_orders(cnx, order_id):
    cursor = cnx.cursor()
    delete_sql = "delete from orders where order_id = %s"
    
    cursor.execute(delete_sql,(order_id,))
    cnx.commit()

#add_order
def add_order_into_order(cnx,order_data):
    cursor = cnx.cursor()
    
    order_query = ("INSERT INTO orders "
                "(customer_name, total,datetime) "
                "VALUES (%s, %s,%s)")
    
    cursor.execute(order_query, order_data)
    cnx.commit()



#update 
def update_data_in_order(cnx, update_data):
    cursor = cnx.cursor()
    update_query = """UPDATE product
                        SET customer_name = %s,
                        total = %s,
                        datetime = %s
                        WHERE order_id = %s;
    """
    cursor.execute(update_query, update_data)
    cnx.commit()
    



def get_order_id_from_order_by_using_customer_id(cnx,customer_id):
    cursor = cnx.cursor()
    query_for_order_id = """SELECT order_id FROM orders WHERE customers_id = %s"""
    
    customer_id = (customer_id,)
    cursor.execute(query_for_order_id, customer_id)
    
    order_id = cursor.fetchall()
    
    
    if not order_id:
        return None 
    order_id = order_id[0][0]
    return order_id
    

    return order_id






if __name__ == '__main__':
    cnx = connect_to_db()
    