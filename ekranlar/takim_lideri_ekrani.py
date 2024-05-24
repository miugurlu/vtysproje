import tkinter as tk
from tkinter import ttk
from database import get_database_connection,mail_gonder

def takim_lideri_ekrani_ac(app, takim_lideri_no):
    new_window = tk.Toplevel(app)
    new_window.title("Takım Lideri")
    tk.Label(new_window, text="Takım Lideri Ekranı").pack(pady=10)

    # Veritabanı bağlantısı kur
    db_connection = get_database_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.callproc('spTakimLideriItirazlariGetir', (takim_lideri_no,))

            # Sonuçları almak için cursor'u kullan
            for result in cursor.stored_results():
                itirazlar = result.fetchall()

            # Tablo oluşturma
            itiraz_table = tk.Frame(new_window)
            itiraz_table.pack(padx=20, pady=20)

            # Başlık satırı
            tk.Label(itiraz_table, text="İtiraz No").grid(row=0, column=0, padx=10, pady=10)
            tk.Label(itiraz_table, text="Asistan Sicil No").grid(row=0, column=1, padx=10, pady=10)
            tk.Label(itiraz_table, text="Asistan Ad Soyad").grid(row=0, column=2, padx=10, pady=10)
            tk.Label(itiraz_table, text="İtiraz Açıklaması").grid(row=0, column=3, padx=10, pady=10)
            tk.Label(itiraz_table, text="İtiraz Ayı").grid(row=0, column=4, padx=10, pady=10)
            tk.Label(itiraz_table, text="İtiraz Durumu").grid(row=0, column=5, padx=10, pady=10)
            tk.Label(itiraz_table, text="Aksiyon").grid(row=0, column=6, padx=10, pady=10)

            # Veri satırları
            for i, itiraz in enumerate(itirazlar, start=1):
                tk.Label(itiraz_table, text=itiraz[0]).grid(row=i, column=0, padx=10, pady=10)  # İtiraz No
                tk.Label(itiraz_table, text=itiraz[1]).grid(row=i, column=1, padx=10, pady=10)  # Asistan Sicil No
                tk.Label(itiraz_table, text=itiraz[2]).grid(row=i, column=2, padx=10, pady=10)  # Asistan Ad Soyad
                tk.Label(itiraz_table, text=itiraz[3]).grid(row=i, column=3, padx=10, pady=10)  # İtiraz Açıklaması
                tk.Label(itiraz_table, text=itiraz[4]).grid(row=i, column=4, padx=10, pady=10)  # İtiraz Ayı
                itiraz_durumu = itiraz[5] if itiraz[5] else "bekliyor"
                tk.Label(itiraz_table, text=itiraz_durumu).grid(row=i, column=5, padx=10, pady=10)  # İtiraz Durumu

                # İtiraz durumu "bekliyor" olan itirazlar için buton oluştur
                if itiraz_durumu == "Bekliyor":
                    tk.Button(itiraz_table, text="İtiraz Cevapla",
                              command=lambda itiraz_no=itiraz[0]: itiraz_cevapla_penceresi_ac(itiraz_no, new_window, takim_lideri_no)).grid(row=i, column=6, padx=10, pady=10)

        except Exception as e:
            print(f"İtiraz listesi alınırken hata oluştu: {e}")
        finally:
            cursor.close()
            db_connection.close()
    else:
        print("Veritabanı bağlantısı sağlanamadı.")


def itiraz_cevapla_penceresi_ac(itiraz_no, parent_window, takim_lideri_no):
    def cevap_gonder():
        cevap_aciklamasi = aciklama_entry.get()
        secili_durum = durum_combobox.get()
        if secili_durum == "Onaylandı":
            itiraz_durumu = "onaylandi"
        elif secili_durum == "Reddedildi":
            itiraz_durumu = "reddedildi"
        else:
            itiraz_durumu = None

        # Veritabanı bağlantısı
        db_connection = get_database_connection()
        if db_connection is not None:
            cursor = db_connection.cursor()
            try:
                # SQL sorgusu ile itiraz cevabını güncelle
                query = "UPDATE itirazlar SET itiraz_cevabi=%s, itiraz_durumu=%s WHERE itiraz_no=%s"
                cursor.execute(query, (cevap_aciklamasi, itiraz_durumu, itiraz_no))
                db_connection.commit()
                print("İtiraz cevabı ve durumu güncellendi.")
            except Exception as e:
                print(f"İtiraz cevabı ve durumu güncellenirken hata oluştu: {e}")
            finally:
                cursor.close()
                db_connection.close()
                parent_window.destroy()
                # Takım lideri ekranını yenile
                takim_lideri_ekrani_ac(parent_window.master, takim_lideri_no)

    # İtiraz cevapla penceresi oluşturulması
    cevap_penceresi = tk.Toplevel(parent_window)
    cevap_penceresi.title("İtirazı Cevapla")
    tk.Label(cevap_penceresi, text="Açıklama:").grid(row=0, column=0, padx=10, pady=10)
    aciklama_entry = tk.Entry(cevap_penceresi, width=50)
    aciklama_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(cevap_penceresi, text="İtiraz Durumu:").grid(row=1, column=0, padx=10, pady=10)
    durum_combobox = ttk.Combobox(cevap_penceresi, values=["Onaylandı", "Reddedildi"])
    durum_combobox.grid(row=1, column=1, padx=10, pady=10)

    # Gönder butonu
    def mail_gonder_ve_cevap_gonder():
        # Takım liderinin bağlı olduğu grup yöneticisinin mail adresini al
        db_connection = get_database_connection()
        if db_connection is not None:
            cursor = db_connection.cursor()
            try:
                query = "SELECT mail_adresi FROM grup_yoneticisi WHERE grup_yoneticisi_no = (SELECT grup_yoneticisi_no FROM takim_lideri WHERE takim_lideri_no = %s)"
                cursor.execute(query, (takim_lideri_no,))
                grup_yoneticisi_mail = cursor.fetchone()[0]
                # Mail gönderme işlemi
                mail_gonder(mail_icerigi="itiraz cozuldu", mail_address=grup_yoneticisi_mail)
            except Exception as e:
                print(f"Mail gönderilirken hata oluştu: {e}")
            finally:
                cursor.close()
                db_connection.close()

        # İtiraz cevabını işle
        cevap_gonder()

    gonder_button = tk.Button(cevap_penceresi, text="Gönder", command=mail_gonder_ve_cevap_gonder)
    gonder_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


