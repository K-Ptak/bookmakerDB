import tkinter as tk
from tkinter import messagebox

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Zakłady")
root.geometry("1200x500+35+100")

# Dane tymczasowe do celów demonstracyjnych
# Zastąp je odpowiednimi danymi z bazy danych
admin_user = {"username": "admin", "password": "admin"}
regular_user = {"username": "user", "password": "user"}

# Aktualnie zalogowany użytkownik
current_user = None

# Funkcja do logowania
def login():
    global username_entry
    global password_entry

    username = username_entry.get()
    password = password_entry.get()

    if username == admin_user["username"] and password == admin_user["password"]:
        # Zalogowano jako administrator
        show_admin_panel()
    elif username == regular_user["username"] and password == regular_user["password"]:
        # Zalogowano jako zwykły użytkownik
        show_user_panel()
    else:
        messagebox.showerror("Błąd logowania", "Nieprawidłowy login lub hasło.")

# Funkcja do wylogowywania
def logout():
    global current_user
    current_user = None
    show_login()

# Funkcja do otwierania okna rejestracji
def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Rejestracja")
    registration_window.geometry("300x200")

    registration_label = tk.Label(registration_window, text="Formularz rejestracji", font=("Arial", 16))
    registration_label.pack(pady=10)

    # Tutaj możesz dodać pola do rejestracji, przyciski itp.

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
    register_button = tk.Button(root, text="Zarejestruj się", command=open_registration_window)
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
