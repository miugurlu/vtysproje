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

def aylik_prim_hesapla(musteri_temsilcisi_id, ay, yil):
    db_connection = get_database_connection()
    if db_connection is None:
        return 0

    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT aylikPrimHesapla(%s, %s, %s)",
                       (musteri_temsilcisi_id, ay, yil))
        prim_miktari = cursor.fetchone()[0]
    except Error as e:
        print(f"Fonksiyonu çalıştırırken hata! : {e}")
        prim_miktari = 0
    finally:
        cursor.close()
        db_connection.close()

    return prim_miktari

def prim_ekle(primler, musteri_temsilcisi_no):
    connection = get_database_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        for tarih, prim_miktari in primler.items():
            tarih = f"{tarih}-01"  # Tarihi 'YYYY-MM-DD' formatına dönüştür

            cursor.execute(
                "SELECT * FROM primler WHERE musteri_temsilcisi_no = %s AND prim_tarihi = %s",
                (musteri_temsilcisi_no, tarih)
            )
            prim_var = cursor.fetchone()

            if prim_var:
                cursor.execute(
                    "UPDATE primler SET prim_miktari = %s WHERE musteri_temsilcisi_no = %s AND prim_tarihi = %s",
                    (prim_miktari, musteri_temsilcisi_no, tarih)
                )
            else:
                cursor.execute(
                    "INSERT INTO primler (musteri_temsilcisi_no, prim_tarihi, prim_miktari) VALUES (%s, %s, %s)",
                    (musteri_temsilcisi_no, tarih, prim_miktari)
                )

        connection.commit()
        return True
    except Error as e:
        print(f"Error processing bonus: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def yeni_kullanici_kayit(kullanici_adi, sifre, rol, müsteri_temsilcisi_no=None, takim_lideri_no=None, grup_yoneticisi_no=None):
    connection = get_database_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, rol, musteri_temsilcisi_no, takim_lideri_no, grup_yoneticisi_no) VALUES (%s, %s, %s, %s, %s, %s)",
                       (kullanici_adi, sifre, rol, müsteri_temsilcisi_no, takim_lideri_no, grup_yoneticisi_no))
        connection.commit()
        return True
    except Error as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
def temsilci_atayici(ad_soyad,sicil_no,takim_lideri_no):
    pass
def lider_atayici(ad_soyad,sicil_no,yonetici_no):
    pass

def yonetici_atayici(ad_soyad,sicil_no,mail_adresi):
    pass