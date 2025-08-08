import mysql.connector
__cnx = None
def connect_to_db():
    global __cnx 
    if __cnx is None:
        #connection to the database 
        cnx = mysql.connector.connect(
        host='kali', # * it can '127.0.0.1' also
        user="root",
        password="root",
        database="gs"
        )
    return cnx