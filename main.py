from view.registration import *

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

for p in range(len(passwords)):
    temp = decrypt_value(passwords[p], "storage/enckey.key")
    temp = temp.decode()
    passwords[p] = temp

for i in range(len(usernames)):
    login = usernames[i]
    password = passwords[i]
    credentials[login] = password
    is_admin = admin_privileges[i]
    credentials[login] = {'password': password, 'is_admin': is_admin}


# funkcja do zwracania okna z blędem
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

    usernames = database.mysql_select("user_login", "user")
    passwords = database.mysql_select("user_password", "user")
    admin_privileges = database.mysql_select("user_admin", "user")

    for p in range(len(passwords)):
        temp = decrypt_value(passwords[p], "storage/enckey.key")
        temp = temp.decode()
        passwords[p] = temp

    credentials = {}

    for i in range(len(usernames)):
        login = usernames[i]
        password = passwords[i]
        is_admin = admin_privileges[i]
        credentials[login] = {'password': password, 'is_admin': is_admin}

    if username in credentials:
        user_info = credentials[username]
        password_output = user_info['password']
        is_admin_output = user_info['is_admin']

        if password == password_output:
            if is_admin_output:
                show_admin_panel()
            else:
                show_user_panel(username)
        else:
            login_error()
    else:
        login_error()


# Funkcja do wylogowywania
def logout():
    show_login()


# Funkcja do otwierania okna rejestracji


# Widok logowania
def show_login():
    global username_entry
    global password_entry

    clear_window()

    login_label = tk.Label(root, text="Zaloguj się", font=("Arial", 16))
    login_label.pack(pady=(60, 10))

    username_label = tk.Label(root, text="Login:")
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
def show_user_panel(username):
    clear_window()

    user_label = tk.Label(root, text="Panel użytkownika", font=("Arial", 16))
    user_label.pack(pady=10)

    left_column = tk.Frame(root)
    left_column.pack(side=tk.LEFT, padx=50)
    login_value = tk.Label(left_column, text="Zalogowano jako:")
    login_value.pack(anchor=tk.W, padx=(20, 10), pady=(5,5))
    login_value = tk.Label(left_column, text=f"{username}")
    login_value.pack(anchor=tk.W, padx=(20, 10))

    balance_label = tk.Label(left_column, text="Aktualny balans konta:")
    balance_label.pack(anchor=tk.W, padx=(20, 10), pady=(20, 10))
    balance = database.mysql_select(table="user", column="user_balance", conditions=f"where user_login = '{username}';")
    balance = balance[0]
    balance_value = tk.Label(left_column, text=f"${balance}", font=("Arial", 22))
    balance_value.pack(anchor=tk.W, padx=(20, 10), pady=(20, 10))

    # Środkowa kolumna z listą zakładów użytkownika
    middle_column = tk.Frame(root)
    middle_column.pack(side=tk.LEFT, padx=50)

    bets_label = tk.Label(middle_column, text="Lista zakładów:")
    bets_label.pack(anchor=tk.W, pady=(0, 10))
    bets_listbox = tk.Listbox(middle_column)
    bets_list = ["Zakład 1", "Zakład 2", "Zakład 3", "Zakład 4", "Zakład 5",
                 "Zakład 6", "Zakład 7", "Zakład 8", "Zakład 9", "Zakład 10"]
    for bet in bets_list:
        bets_listbox.insert(tk.END, bet)
    bets_listbox.pack()

    # Prawa kolumna z listą meczy
    right_column = tk.Frame(root)
    right_column.pack(side=tk.LEFT, padx=50)

    matches_label = tk.Label(right_column, text="Lista meczy:")
    matches_label.pack(anchor=tk.W, pady=(0, 10))
    matches_listbox = tk.Listbox(right_column)
    matches_list = ["Mecz 1", "Mecz 2", "Mecz 3", "Mecz 4", "Mecz 5",
                    "Mecz 6", "Mecz 7", "Mecz 8", "Mecz 9", "Mecz 10"]
    for match in matches_list:
        matches_listbox.insert(tk.END, match)
    matches_listbox.pack()

    # Przycisk Wyloguj
    logout_button = tk.Button(root, text="Wyloguj", width=10, command=logout)
    logout_button.pack(side=tk.BOTTOM, pady=20)


# Funkcja do czyszczenia okna
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# Wyświetlanie widoku logowania jako domyślnego widoku startowego
show_login()

root.mainloop()
