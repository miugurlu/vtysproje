import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from database import yeni_kullanici_kayit

def grup_yoneticisi_ekrani_ac(app, grup_yoneticisi_no):
    new_window = tk.Toplevel(app)
    new_window.title("Yeni İşçi Kaydı")
    new_window.attributes('-fullscreen', True)

    # Kullanıcı Adı
    tk.Label(new_window, text="Kullanıcı Adı").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_username = tk.Entry(new_window)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    # Şifre
    tk.Label(new_window, text="Şifre").grid(row=1, column=0, padx=10, pady=10)
    entry_password = tk.Entry(new_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    # Rol Seçimi
    tk.Label(new_window, text="Rol").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    combobox_role = Combobox(new_window, values=["musteri_temsilcisi", "takim_lideri", "grup_yoneticisi"])
    combobox_role.grid(row=2, column=1, padx=10, pady=10)

    # Kayıt Butonu
    def register_employee():
        username = entry_username.get()
        password = entry_password.get()
        role = combobox_role.get()  # Kullanıcının seçtiği rolü al

        if not (username and password and role):
            messagebox.showerror("HATA", "Tüm alanları doldurun ve bir rol seçin")
            return

        try:
            # Rol seçimine göre uygun parametreleri geç
            if role == "musteri_temsilcisi":
                success = yeni_kullanici_kayit(username, password, role, müsteri_temsilcisi_no=grup_yoneticisi_no)
            elif role == "takim_lideri":
                success = yeni_kullanici_kayit(username, password, role, takim_lideri_no=grup_yoneticisi_no)
            elif role == "grup_yoneticisi":
                success = yeni_kullanici_kayit(username, password, role, grup_yoneticisi_no=grup_yoneticisi_no)
            else:
                messagebox.showerror("HATA", "Geçersiz rol")
                return

            if success:
                messagebox.showinfo("Bilgi", "Yeni kullanıcı başarıyla kaydedildi.")
            else:
                messagebox.showerror("HATA", "Kullanıcı kaydedilirken bir hata oluştu.")

        except Exception as e:
            messagebox.showerror("HATA", f"Hata: {e}")

    btn_register = tk.Button(new_window, text="Kaydet", command=register_employee)
    btn_register.grid(row=3, column=0, columnspan=2, pady=10)

    new_window.mainloop()

