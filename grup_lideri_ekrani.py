import tkinter as tk
from tkinter import messagebox
from database import *


def grup_yoneticisi_ekrani_ac(app, grup_yoneticisi_no):
    new_window = tk.Toplevel(app)
    new_window.title("Yeni İşçi Kaydı")
    new_window.attributes('-fullscreen', True)

    # Kullanıcı Adı
    tk.Label(new_window, text="Kullanıcı Adı").pack()
    entry_username = tk.Entry(new_window)
    entry_username.pack()

    # Şifre
    tk.Label(new_window, text="Şifre").pack()
    entry_password = tk.Entry(new_window, show="*")
    entry_password.pack()

    # Rol Seçimi
    tk.Label(new_window, text="Rol").pack()
    combobox_role = tk.Combobox(new_window, values=["musteri_temsilcisi", "takim_lideri", "grup_yoneticisi"])
    combobox_role.pack()

    # Kayıt Butonu
    def register_employee():
        username = entry_username.get()
        password = entry_password.get()
        role = combobox_role.get()  # Kullanıcının seçtiği rolü al

        if not (username and password and role):
            messagebox.showerror("HATA", "Tüm alanları doldurun ve bir rol seçin")
            return

        try:
            register_new_employee(username, password, role)
            messagebox.showinfo("Bilgi", "Yeni işçi başarıyla kaydedildi.")
        except Exception as e:
            messagebox.showerror("HATA", f"Hata: {e}")

    btn_register = tk.Button(new_window, text="Kaydet", command=register_employee)
    btn_register.pack(pady=10)

    new_window.mainloop()
