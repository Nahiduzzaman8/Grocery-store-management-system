import mysql.connector
from get_sql_connection import connect_to_db

#read 
def get_all_data_from_product(cnx):
    cursor = cnx.cursor()         # create cursor for execute sql
    product_query = """SELECT product.product_id, product.name,product.price_per_unit, uom.name, product.uom_id FROM product
                   inner join uom
                   on product.uom_id = uom.uom_id """   
    cursor.execute(product_query) # execute the sql
    data = cursor.fetchall()      # after executing cursor hold all the data from the db. this line will fetch all data from the cursor to spesific variable 
    
    data_in_list_as_dict = []
    for (a,b,c,d,e) in data:
        data_in_list_as_dict.append(
            {'product_id':a,
            'name':b,
            'price_per_unit':c,
            'uom_name':d,
            'uom_id':e
            }
        )
    return data_in_list_as_dict

#*insert_data_into_product
def insert_data_into_product(cnx, product):
    cursor = cnx.cursor()
    
    product_insert_query = ("INSERT INTO product "
                "(name, price_per_unit, uom_id) "
                "VALUES (%s, %s,%s)")
    product_insert_data = (product[0], product[1], product[2])
    
    cursor.execute(product_insert_query, product_insert_data)
    cnx.commit()

#update 
def update_data_in_product(cnx, update_info):
    cursor = cnx.cursor()
    update_query = """UPDATE product
                        SET name = %s,
                        price_per_unit = %s,
                        uom_id = %s
                        WHERE product_id = %s;
    """
    cursor.execute(update_query, update_info)
    cnx.commit()


#delete
def delete_data_from_product(cnx, id):
    cursor = cnx.cursor()
    delete_query = "delete from product where product_id = %s"
    delete_data = (id,)
    cursor.execute(delete_query,delete_data)
    cnx.commit()

def get_product_details_using_product_id(cnx,product_id):
    cursor = cnx.cursor(dictionary = True)
    product_sql = """SELECT * FROM product WHERE product_id = %s"""
    
    product_id = (product_id,)
    cursor.execute(product_sql, product_id)
    
    product = cursor.fetchone()

    return product

if __name__ == '__main__':
    boom = connect_to_db()
    print(get_product_details_using_product_id(boom,1))
