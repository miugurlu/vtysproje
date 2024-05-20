import tkinter as tk
from login import create_login_screen


def main():
    app = tk.Tk()
    app.title("Giriş Ekranı")
    app.attributes('-fullscreen', True)

    create_login_screen(app)

    app.mainloop()


if __name__ == "__main__":
    main()
