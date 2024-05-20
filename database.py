import mysql.connector
from mysql.connector import Error

def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ibrahim482",
            database="vtysproje"
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_user_role(username, password):
    connection = get_database_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT rol, musteri_temsilcisi_no, takim_lideri_no, grup_yoneticisi_no FROM kullanicilar WHERE kullanici_adi=%s AND sifre=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
