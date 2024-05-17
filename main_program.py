import tkinter as tk
from tkinter import messagebox
import mysql.connector

from customer_representative_screen import open_customer_representative_screen

# Kullanıcı girişi kontrolü
def check_login():
    user_id = entry_id.get()
    password = entry_password.get()

    # Veritabanına bağlanma
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='şifren',
        database='vtysproje'
    )
    cursor = conn.cursor()

    query = "SELECT sicil_no FROM giris_bilgileri WHERE giris_id = %s AND sifre = %s"
    cursor.execute(query, (user_id, password))
    result = cursor.fetchone()

    if result:
        sicil_no = result[0]
        cursor.execute("SELECT * FROM musteri_temsilcisi WHERE sicil_no = %s", (sicil_no,))
        if cursor.fetchone():
            # Müşteri temsilcisi ekranını aç
            open_customer_representative_screen()
        else:
            messagebox.showerror("Giriş Başarısız", "Bu ekranı görüntülemek için gerekli yetkiye sahip değilsiniz.")
    else:
        messagebox.showerror("Giriş Başarısız", "Geçersiz giriş ID'si veya şifre.")

    cursor.close()
    conn.close()

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Giriş Ekranı")

tk.Label(root, text="Giriş ID").grid(row=0, column=0, padx=10, pady=10)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Şifre").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Giriş Yap", command=check_login).grid(row=2, columnspan=2, pady=10)

root.mainloop()
