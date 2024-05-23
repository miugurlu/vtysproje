import tkinter as tk
from tkinter import messagebox
from database import get_database_connection, aylik_prim_hesapla
from datetime import datetime

def musteri_temsilcisi_ekrani_ac(app, temsilci_no):
    new_window = tk.Toplevel(app)
    new_window.title("Müşteri Temsilcisi")
    tk.Label(new_window, text="Müşteri Temsilcisi").pack()

    btn_call_list = tk.Button(new_window, text="Müşteri Çağrı Listesi", command=lambda: musteri_cagri_listesi_ac(new_window, temsilci_no))
    btn_call_list.pack(pady=10)

    btn_monthly_bonus_list = tk.Button(new_window, text="Aylık Prim Listesi", command=lambda: aylik_prim_listesi_ac(new_window, temsilci_no))
    btn_monthly_bonus_list.pack(pady=10)

    btn_objection_list = tk.Button(new_window, text="İtirazlarım", command=lambda: itiraz_listesi_ac(new_window, temsilci_no))
    btn_objection_list.pack(pady=10)


#MÜŞTERİ TEMSİLCİSİ ÇAĞRI LİSTESİ GÖRME VE EKLEME
def musteri_cagri_listesi_ac(parent_window, temsilci_no):
    if hasattr(parent_window, 'call_list_window') and parent_window.call_list_window.winfo_exists():
        parent_window.call_list_window.lift()
        return

    call_list_window = tk.Toplevel(parent_window)
    parent_window.call_list_window = call_list_window
    call_list_window.title("Müşteri Çağrı Listesi")
    tk.Label(call_list_window, text=f"Müşteri Temsilcisi {temsilci_no} için Müşteri Çağrı Listesi").pack()

    call_listbox = tk.Listbox(call_list_window, width=100)
    call_listbox.pack(pady=10)
    call_list_window.call_listbox = call_listbox

    btn_new_call = tk.Button(call_list_window, text="Yeni Çağrı", command=lambda: yeni_cagri_ekle(call_list_window, call_listbox, temsilci_no))
    btn_new_call.pack(pady=10)

    load_calls(call_listbox, temsilci_no)

def load_calls(listbox, musteri_id):
    listbox.delete(0, tk.END)
    connection = get_database_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT musteri_ad_soyad, gorusme_konusu, gorusme_tarihi, gorusme_baslama_saati, gorusme_bitis_saati, gorusme_durum "
            "FROM vw_gorusme_detaylari WHERE musteri_id=%s",
            (musteri_id,)
        )
        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}")
        cursor.close()
        connection.close()


def yeni_cagri_ekle(parent_window, listbox, temsilci_no):
    new_call_window = tk.Toplevel(parent_window)
    new_call_window.title("Yeni Çağrı Ekle")

    def save_new_call():
        musteri_ad_soyad = entry_musteri_ad_soyad.get()
        gorusme_konusu = entry_gorusme_konusu.get()
        gorusme_tarihi = entry_gorusme_tarihi.get()
        gorusme_baslama_saati = entry_gorusme_baslama_saati.get()
        gorusme_bitis_saati = entry_gorusme_bitis_saati.get()
        gorusme_durum = entry_gorusme_durum.get()

        if not (musteri_ad_soyad and gorusme_konusu and gorusme_tarihi and gorusme_baslama_saati and gorusme_bitis_saati and gorusme_durum):
            messagebox.showerror("Hata", "Tüm alanları doldurmanız gerekmektedir.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc('spGorusmeEkle', [temsilci_no, musteri_ad_soyad, gorusme_konusu, gorusme_tarihi, gorusme_baslama_saati, gorusme_bitis_saati, gorusme_durum])
                connection.commit()
                listbox.insert(0, f"{musteri_ad_soyad} - {gorusme_konusu} - {gorusme_tarihi} - {gorusme_baslama_saati} - {gorusme_bitis_saati} - {gorusme_durum}")
                new_call_window.destroy()
                # Yeni kayıt eklendikten sonra çağrı listesi penceresini güncelle
                load_calls(parent_window.call_listbox, temsilci_no)
            except Exception as e:
                messagebox.showerror("Hata", f"Görüşme eklenirken hata oluştu: {str(e)}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı.")

    tk.Label(new_call_window, text="Müşteri Ad Soyad").pack(pady=5)
    entry_musteri_ad_soyad = tk.Entry(new_call_window)
    entry_musteri_ad_soyad.pack(pady=5)

    tk.Label(new_call_window, text="Görüşme Konusu").pack(pady=5)
    entry_gorusme_konusu = tk.Entry(new_call_window)
    entry_gorusme_konusu.pack(pady=5)

    tk.Label(new_call_window, text="Görüşme Tarihi (YYYY-MM-DD)").pack(pady=5)
    entry_gorusme_tarihi = tk.Entry(new_call_window)
    entry_gorusme_tarihi.pack(pady=5)

    tk.Label(new_call_window, text="Görüşme Başlama Saati (HH:MM:SS)").pack(pady=5)
    entry_gorusme_baslama_saati = tk.Entry(new_call_window)
    entry_gorusme_baslama_saati.pack(pady=5)

    tk.Label(new_call_window, text="Görüşme Bitiş Saati (HH:MM:SS)").pack(pady=5)
    entry_gorusme_bitis_saati = tk.Entry(new_call_window)
    entry_gorusme_bitis_saati.pack(pady=5)

    tk.Label(new_call_window, text="Görüşme Durumu").pack(pady=5)
    entry_gorusme_durum = tk.Entry(new_call_window)
    entry_gorusme_durum.pack(pady=5)

    btn_save = tk.Button(new_call_window, text="Kaydet", command=save_new_call)
    btn_save.pack(pady=10)



#MÜŞTERİ TEMSİLCİSİ PRİMLERİNİ GÖRME
def aylik_prim_hesapla(musteri_temsilcisi_id, baslangic_tarihi, bitis_tarihi):
    db_connection = get_database_connection()
    if db_connection is None:
        return 0

    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT aylik_prim_hesapla(%s, %s, %s)", (musteri_temsilcisi_id, baslangic_tarihi, bitis_tarihi))
        prim_miktari = cursor.fetchone()[0]
    except Exception as e:
        print(f"Fonksiyonu çalıştırırken hata : {e}")
        prim_miktari = 0
    finally:
        cursor.close()
        db_connection.close()

    return prim_miktari


def itiraz_et(musteri_temsilcisi_no):
    # İtiraz etme işlemi burada yapılacak
    itiraz_aciklama_penceresi = tk.Toplevel()
    itiraz_aciklama_penceresi.title("İtiraz Açıklaması")

    tk.Label(itiraz_aciklama_penceresi, text="İtiraz Açıklaması:").pack(pady=10)
    itiraz_aciklama_entry = tk.Entry(itiraz_aciklama_penceresi, width=50)
    itiraz_aciklama_entry.pack(pady=10)

    def itiraz_gonder():
        aciklama = itiraz_aciklama_entry.get()
        if aciklama:
            # İtiraz kaydını veri tabanına ekle
            db_connection = get_database_connection()
            if db_connection is not None:
                cursor = db_connection.cursor()
                try:
                    cursor.callproc("spItirazOlustur", (musteri_temsilcisi_no, aciklama, datetime.now().date()))
                    db_connection.commit()
                except Exception as e:
                    print(f"İtiraz kaydedilirken hata oluştu: {e}")
                finally:
                    cursor.close()
                    db_connection.close()
            itiraz_aciklama_penceresi.destroy()

    tk.Button(itiraz_aciklama_penceresi, text="Gönder", command=itiraz_gonder).pack(pady=10)


def aylik_prim_listesi_ac(parent_window, musteri_temsilcisi_no):
    new_window = tk.Toplevel(parent_window)
    new_window.title("Aylık Prim Listesi")

    primler = {}
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    for i in range(12):
        ay = current_month - i
        yil = current_year
        if ay <= 0:
            ay += 12
            yil -= 1
        baslangic_tarihi = f'{yil}-{ay:02d}-01'
        bitis_tarihi = f'{yil}-{ay:02d}-28'
        prim_miktari = aylik_prim_hesapla(musteri_temsilcisi_no, baslangic_tarihi, bitis_tarihi)
        primler[f"{yil}-{ay:02d}"] = prim_miktari

    # Aylık primleri tkinter tablosunda göster
    prim_table = tk.Frame(new_window)
    prim_table.pack(padx=10, pady=10)

    tk.Label(prim_table, text="Ay").grid(row=0, column=0)
    tk.Label(prim_table, text="Prim Miktarı").grid(row=0, column=1)

    row = 1
    for ay, prim in primler.items():
        tk.Label(prim_table, text=ay).grid(row=row, column=0)
        tk.Label(prim_table, text=str(prim)).grid(row=row, column=1)
        if row == 1:
            tk.Button(prim_table, text="İtiraz Et",
                      command=lambda: itiraz_et(musteri_temsilcisi_no)).grid(
                row=row, column=2)
        row += 1



#İTİRAZ LİSTESİNİ GÖRME
def itiraz_listesi_ac(parent_window, temsilci_no):
    new_window = tk.Toplevel(parent_window)
    new_window.title("İtirazlarım")

    # Başlık etiketi
    tk.Label(new_window, text=f"Müşteri Temsilcisi {temsilci_no} için İtiraz Listesi").pack()

    # Görünümün sorgulanması
    db_connection = get_database_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            # itirazlar_view görünümünden verileri al
            cursor.execute("SELECT itiraz_aciklamasi, itiraz_cevabi, itiraz_durumu FROM vw_itirazlar WHERE musteri_temsilcisi_no = %s", (temsilci_no,))
            itirazlar = cursor.fetchall()

            # Tablo oluşturma
            itiraz_table = tk.Frame(new_window)
            itiraz_table.pack(padx=20, pady=20)

            # Başlık satırı
            tk.Label(itiraz_table, text="İtiraz Açıklaması").grid(row=0, column=0, padx=10, pady=10)
            tk.Label(itiraz_table, text="İtiraz Cevabı").grid(row=0, column=1, padx=10, pady=10)
            tk.Label(itiraz_table, text="İtiraz Durumu").grid(row=0, column=2, padx=10, pady=10)

            # Veri satırları
            for i, itiraz in enumerate(itirazlar, start=1):
                tk.Label(itiraz_table, text=itiraz[0]).grid(row=i, column=0, padx=10, pady=10)
                tk.Label(itiraz_table, text=itiraz[1]).grid(row=i, column=1, padx=10, pady=10)
                tk.Label(itiraz_table, text=itiraz[2]).grid(row=i, column=2, padx=10, pady=10)

        except Exception as e:
            print(f"İtiraz listesi alınırken hata oluştu: {e}")
        finally:
            cursor.close()
            db_connection.close()
    else:
        print("Veritabanı bağlantısı sağlanamadı.")