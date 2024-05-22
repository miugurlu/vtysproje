import mysql.connector
from mysql.connector import Error

def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
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
    cursor.execute("SELECT rol, temsilci_no, takim_lideri_no, grup_yoneticisi_no FROM kullanicilar WHERE kullanici_adi=%s AND sifre=%s", (username, password))
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


def register_new_employee(username, password, role, temsilci_no=None, takim_lideri_no=None, grup_yoneticisi_no=None):
    connection = get_database_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, rol, temsilci_no, takim_lideri_no, grup_yoneticisi_no) VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, password, role, temsilci_no, takim_lideri_no, grup_yoneticisi_no))
        connection.commit()
        return True
    except Error as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
