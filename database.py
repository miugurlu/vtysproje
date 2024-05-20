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


def aylik_prim_hesapla(musteri_temsilcisi_id, baslangic_tarihi, bitis_tarihi):
    db_connection = get_database_connection()
    if db_connection is None:
        return 0

    cursor = db_connection.cursor()
    try:
        cursor.callproc('calculate_monthly_prim', [musteri_temsilcisi_id, baslangic_tarihi, bitis_tarihi])
        for result in cursor.stored_results():
            prim_miktari = result.fetchone()[0]
    except Error as e:
        print(f"Error executing procedure: {e}")
        prim_miktari = 0
    finally:
        cursor.close()
        db_connection.close()

    return prim_miktari
