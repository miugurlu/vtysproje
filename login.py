import tkinter as tk
from tkinter import messagebox
from database import get_user_role
from musteri_temsilcisi_ekrani import musteri_temsilcisi_ekrani_ac
from takim_lideri_ekrani import takim_lideri_ekrani_ac
from grup_lideri_ekrani import grup_yoneticisi_ekrani_ac

def create_login_screen(app):
    def login():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("HATA", "Kullanıcı adı ve şifre gerekli")
            return

        try:
            result = get_user_role(username, password)
        except Exception as e:
            messagebox.showerror("HATA", f"Veritabanı hatası: {e}")
            return

        if result:
            role, user_id, takim_lideri_no, grup_yoneticisi_no = result
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            login_frame.pack_forget()  # Giriş ekranını gizle
            if role == 'musteri_temsilcisi':
                musteri_temsilcisi_ekrani_ac(app, user_id)
            elif role == 'takim_lideri':
                takim_lideri_ekrani_ac(app, takim_lideri_no)
            elif role == 'grup_yoneticisi':
                grup_yoneticisi_ekrani_ac(app, grup_yoneticisi_no)
        else:
            messagebox.showerror("HATA", "Geçersiz kullanıcı adı veya şifre")

    login_frame = tk.Frame(app)
    login_frame.pack(pady=20)

    tk.Label(login_frame, text="Kullanıcı Adı").pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack()

    tk.Label(login_frame, text="Şifre").pack()
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()

    btn_login = tk.Button(login_frame, text="Giriş Yap", command=login)
    btn_login.pack()
