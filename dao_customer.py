import mysql.connector
from get_sql_connection import connect_to_db

#read 
def get_all_data_from_customers(cnx):
    #cursor = cnx.cursor(dictionary=True)  
    cursor = cnx.cursor()         
    customers_query = """SELECT * FROM customers """   
    
    cursor.execute(customers_query)
    data = cursor.fetchall()     
    
    data_in_list_as_dict = []
    for (a,b,c,d,e) in data:
        data_in_list_as_dict.append(
            {'customer_id':a,
            'customer_name':b,
            'email':c,
            'contact':d,
            'address':e
            }
        )
    return data_in_list_as_dict






#delete
def delete_data_from_customer(cnx, id):
    cursor = cnx.cursor()
    delete_query = "delete from customers where customer_id = %s"
    delete_data = (id,)
    cursor.execute(delete_query,delete_data)
    cnx.commit()



#update 
def update_data_in_customers(cnx, update_data):
    cursor = cnx.cursor()
    update_query = """UPDATE customers
                        SET customer_name = %s, email = %s, contact = %s, address = %s
                        WHERE customer_id = %s;
    """
    cursor.execute(update_query, update_data)
    cnx.commit()


def get_customers_id_from_customers_by_using_customer_name(cnx,customer_name):
    cursor = cnx.cursor()
    query_for_customers_id = """SELECT customer_id FROM customers WHERE customer_name = %s"""
    
    customer_name = (customer_name,)
    cursor.execute(query_for_customers_id, customer_name)
    
    
    customer_id = cursor.fetchall()
    
    if not customer_id:
        return None
    
    customer_id = customer_id[0][0]

    return customer_id

def get_customer_by_id(cnx, customer_id):
    cursor = cnx.cursor(dictionary = True)
    sql =''' select * from customers 
             where customer_id = %s'''
    cursor.execute(sql,(customer_id,))
    customers = cursor.fetchone()
    return customers


    
if __name__ == "__main__":
    cnx = connect_to_db() 
    
    print(get_customer_by_id(cnx,2))