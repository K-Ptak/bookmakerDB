import tkinter as tk
from tkinter import messagebox
from view.registration import *
from database.database_handler import DatabasePointer

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Zakłady")
root.geometry("1200x500+35+100")

# Pobieranie z bazy danych
database = DatabasePointer()
usernames = database.mysql_select("user_login", "user")
passwords = database.mysql_select("user_password", "user")
admin_privileges = database.mysql_select("user_admin", "user")
credentials = {}

for i in range(len(usernames)):
    login = usernames[i]
    password = passwords[i]
    credentials[login] = password
    is_admin = admin_privileges[i]
    credentials[login] = {'password': password, 'is_admin': is_admin}

# Aktualnie zalogowany użytkownik
current_user = None

#funkcja do zwracania okna z blędem
def login_error():
    messagebox.showerror("Błąd logowania", "Nieprawidłowy login lub hasło.")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# Funkcja do logowania
def login():
    global username_entry
    global password_entry

    username = username_entry.get()
    password = password_entry.get()

    if username in credentials:
        user_info = credentials[username]
        password_output = user_info['password']
        is_admin_output = user_info['is_admin']

        if password == password_output:
            if is_admin_output:
                show_admin_panel()
            else:
                show_user_panel()
        else:
            login_error()
    else:
        login_error()


# Funkcja do wylogowywania
def logout():
    global current_user
    current_user = None
    show_login()

# Funkcja do otwierania okna rejestracji


# Widok logowania
def show_login():
    global username_entry
    global password_entry

    clear_window()

    login_label = tk.Label(root, text="Zaloguj się", font=("Arial", 16))
    login_label.pack(pady=(60, 10))

    username_label = tk.Label(root, text="Nazwa użytkownika:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Hasło:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_button = tk.Button(root, text="Zaloguj się", command=login)
    login_button.pack(pady=10)

    # Przycisk do otwierania okna rejestracji
    register_button = tk.Button(root, text="Zarejestruj się", command=lambda: open_registration_window(root))
    register_button.pack(side=tk.RIGHT, padx=10, pady=10)


# Widok panelu administratora
def show_admin_panel():
    clear_window()

    admin_label = tk.Label(root, text="Panel administratora", font=("Arial", 16))
    admin_label.pack(pady=10)

    # Tutaj możesz dodać odpowiednie elementy interfejsu do wyświetlania i zmiany danych

    logout_button = tk.Button(root, text="Wyloguj", command=logout)
    logout_button.pack(anchor=tk.SE, padx=10, pady=10)


# Widok panelu użytkownika
def show_user_panel():
    clear_window()

    user_label = tk.Label(root, text="Panel użytkownika", font=("Arial", 16))
    user_label.pack(pady=10)

    # Tutaj możesz dodać odpowiednie elementy interfejsu do wyświetlania zakładów i meczy

    logout_button = tk.Button(root, text="Wyloguj", command=logout)
    logout_button.pack(anchor=tk.SE, padx=10, pady=10)


# Funkcja do czyszczenia okna
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# Wyświetlanie widoku logowania jako domyślnego widoku startowego
show_login()

root.mainloop()
