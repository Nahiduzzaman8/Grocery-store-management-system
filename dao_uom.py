import mysql.connector
from get_sql_connection import connect_to_db

def get_all_uom_names_data_from_uom(cnx):
    cursor = cnx.cursor()         # create cursor for execute sql
    uom_query = """ SELECT name FROM uom """
                   
    cursor.execute(uom_query) # execute the sql
    uom_name_data = cursor.fetchall()   
    uom_name_data_in_list = []
    for item in uom_name_data:
        uom_name_data_in_list.append(item[0])
    
    return uom_name_data_in_list





def get_uom_id_by_using_name(cnx, name):
    cursor = cnx.cursor(dictionary = True)
    id_query = """SELECT uom_id FROM uom WHERE name = %s"""
    name_data = (name,)
    cursor.execute(id_query, name_data)
    uom_id = cursor.fetchone()
    return uom_id
    




if __name__ == '__main__':
    boom = connect_to_db()
    print(get_uom_id_by_using_name(boom,"kg"))
    