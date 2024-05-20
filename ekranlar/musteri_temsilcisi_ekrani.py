import tkinter as tk
from tkinter import messagebox
from database import get_database_connection

def musteri_temsilcisi_ekrani_ac(app, temsilci_no):
    new_window = tk.Toplevel(app)
    new_window.title("Müşteri Temsilcisi")
    tk.Label(new_window, text="Müşteri Temsilcisi").pack()

    btn_call_list = tk.Button(new_window, text="Müşteri Çağrı Listesi", command=lambda: musteri_cagri_listesi_ac(new_window, temsilci_no))
    btn_call_list.pack(pady=10)

    btn_monthly_bonus_list = tk.Button(new_window, text="Aylık Prim Listesi", command=lambda: aylik_bonus_listesi_ac(new_window, temsilci_no))
    btn_monthly_bonus_list.pack(pady=10)

    btn_objection_list = tk.Button(new_window, text="İtirazlarım", command=lambda: itiraz_listesi_ac(new_window, temsilci_no))
    btn_objection_list.pack(pady=10)

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

def load_calls(listbox, temsilci_no):
    listbox.delete(0, tk.END)
    connection = get_database_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT musteri_ad_soyad, gorusme_konusu, gorusme_tarihi, gorusme_baslama_saati, gorusme_bitis_saati, gorusme_durum FROM gorusme WHERE musteri_id=%s", (temsilci_no,))
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
                cursor.callproc('sp_AddGorusme', [temsilci_no, musteri_ad_soyad, gorusme_konusu, gorusme_tarihi, gorusme_baslama_saati, gorusme_bitis_saati, gorusme_durum])
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

def aylik_bonus_listesi_ac(parent_window, temsilci_no):
    new_window = tk.Toplevel(parent_window)
    new_window.title("Aylık Prim Listesi")
    tk.Label(new_window, text=f"Müşteri Temsilcisi {temsilci_no} için Aylık Prim Listesi").pack()
    # Burada aylık prim listesini görüntülemek için gerekli kodları ekleyin

def itiraz_listesi_ac(parent_window, temsilci_no):
    new_window = tk.Toplevel(parent_window)
    new_window.title("İtirazlarım")
    tk.Label(new_window, text=f"Müşteri Temsilcisi {temsilci_no} için İtiraz Listesi").pack()
    # Burada itiraz listesini görüntülemek için gerekli kodları ekleyin
