import tkinter as tk
from tkinter import ttk
from database import get_database_connection

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
                tk.Label(itiraz_table, text=itiraz[5] if itiraz[5] else "bekliyor").grid(row=i, column=5, padx=10, pady=10)  # İtiraz Durumu
                if itiraz[5] is None or itiraz[5] == "bekliyor":
                    tk.Button(itiraz_table, text="İtiraz Cevapla",
                              command=lambda itiraz_no=itiraz[0]: itiraz_cevapla_penceresi_ac(itiraz_no, new_window, takim_lideri_no)).grid(row=i,column=6,padx=10,pady=10)

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
                # Stored procedure'u çağır
                cursor.callproc('spItirazCevapla', (itiraz_no, cevap_aciklamasi, itiraz_durumu))
                db_connection.commit()
                print("İtiraz cevabı ve durumu güncellendi.")
            except Exception as e:
                print(f"İtiraz cevabı ve durumu güncellenirken hata oluştu: {e}")
            finally:
                cursor.close()
                db_connection.close()
                parent_window.destroy()

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
    gonder_button = tk.Button(cevap_penceresi, text="Gönder", command=cevap_gonder)
    gonder_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
