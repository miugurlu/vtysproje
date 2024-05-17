# customer_representative_screen.py

import tkinter as tk
from customer_call_list import show_customer_call_list
from monthly_bonus_list import show_monthly_bonus_list
from bonus_objection_list import show_bonus_objection_list

def open_customer_representative_screen():
    customer_representative_window = tk.Toplevel()
    customer_representative_window.title("Müşteri Temsilcisi Ekranı")

    # Müşteri çağrı listesi menüsü için buton
    tk.Button(customer_representative_window, text="Müşteri Çağrı Listesi", command=show_customer_call_list).pack(pady=10)

    # Sistemde aktif olan asistana ait aylık prim listesi menüsü için buton
    tk.Button(customer_representative_window, text="Aylık Prim Listesi", command=show_monthly_bonus_list).pack(pady=10)

    # Asistanların primlerine yaptıkları itirazlar listesi menüsü için buton
    tk.Button(customer_representative_window, text="Prim İtiraz Listesi", command=show_bonus_objection_list).pack(pady=10)
