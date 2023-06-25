import ttkbootstrap as ttk
from ttkbootstrap import Style, OUTLINE, INFO
from model.betcard import BetCard
from model.matchcard import MatchCard
from view.registration import *
from database.admin_privilege_handler import show_add_privilege_window, show_del_privilege_window

# Tworzenie głównego okna aplikacji
root = ttk.Window()
root.title("Zakłady")
root.state('zoomed')
root.geometry("1200x500+35+100")

style = Style(theme='darkly')

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
    username_entry.delete(0, ttk.END)
    password_entry.delete(0, ttk.END)


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
                show_admin_panel(username)
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

    app_label = ttk.Label(root, text="Aplikacja Bukmacherska", font=("Comic Sans MS", 36))
    app_label.pack(pady=10)

    login_label = ttk.Label(root, text="Zaloguj się", font=("Bahnschrift", 16))
    login_label.pack(pady=(120, 20))

    username_label = ttk.Label(root, text="Login:")
    username_label.pack()
    username_entry = ttk.Entry(root)
    username_entry.pack(pady=(0, 20))

    password_label = ttk.Label(root, text="Hasło:")
    password_label.pack()
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=(0, 20))

    login_button = ttk.Button(root, text="Zaloguj się", command=login)
    login_button.pack(pady=10)

    # Przycisk do otwierania okna rejestracji
    register_button = ttk.Button(root, text="Zarejestruj się",  bootstyle=(INFO, OUTLINE), command=lambda: open_registration_window(root))
    register_button.pack(side=ttk.RIGHT, padx=10, pady=10)


# Widok panelu administratora
def show_admin_panel(username):
    clear_window()

    admin_label = ttk.Label(root, text="Panel administratora", font=("Arial", 16))
    admin_label.pack(pady=10)

    left_column = ttk.Frame(root)
    left_column.pack(side=ttk.LEFT, padx=50)

    login_value_label = ttk.Label(left_column, text="Zalogowano jako:")
    login_value_label.pack(anchor=ttk.W, padx=(20, 10), pady=(5, 5))

    login_value = ttk.Label(left_column, text=f"{username}")
    login_value.pack(anchor=ttk.W, padx=(20, 10), pady=(0, 100))

    add_privileges_button = ttk.Button(left_column, text="Nadaj uprawnienia administratora", width=30, bootstyle=(SUCCESS, OUTLINE), command=lambda: show_add_privilege_window(root))
    add_privileges_button.pack(anchor=ttk.W, padx=(20, 10), pady=(0, 25))

    del_privileges_button = ttk.Button(left_column, text="Odbierz uprawnienia administratora", width=30, bootstyle=(DANGER, OUTLINE), command=lambda: show_del_privilege_window(root, username))
    del_privileges_button.pack(anchor=ttk.W, padx=(20, 10))

    logout_button = ttk.Button(root, text="Wyloguj", width=10, bootstyle=(INFO, OUTLINE), command=logout)
    logout_button.pack(side=ttk.BOTTOM, padx=(750, 0), pady=(0, 20))

    middle_column = ttk.Frame(root)
    middle_column.pack(side=ttk.LEFT, padx=50)

    zaklady_label = ttk.Label(middle_column, text="Lista zakładów:")
    zaklady_label.pack(anchor=ttk.W, pady=(0, 10))

    # Dodanie przewijania do listy zakładów
    zaklady_frame = ttk.Frame(middle_column, relief=ttk.SOLID)
    zaklady_frame.pack(fill=ttk.BOTH, expand=1)

    canvas = ttk.Canvas(zaklady_frame)
    canvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=1)

    scrollbar = ttk.Scrollbar(zaklady_frame, orient=ttk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    zaklady_inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=zaklady_inner_frame, anchor=ttk.NW)

    zaklady_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    zaklady = [
        ("Gra 1", "Wynik 1", "100", "Wygrany", "2023-06-19"),
        ("Gra 2", "Wynik 2", "50", "Przegrany", "2023-06-18"),
        ("Gra 3", "Wynik 3", "200", "Oczekujący", "2023-06-17"),
        ("Gra 4", "Wynik 4", "150", "Wygrany", "2023-06-16"),
        ("Gra 5", "Wynik 5", "80", "Przegrany", "2023-06-15"),
        ("Gra 6", "Wynik 6", "120", "Oczekujący", "2023-06-14"),
        ("Gra 7", "Wynik 7", "90", "Wygrany", "2023-06-13"),
        ("Gra 8", "Wynik 8", "70", "Przegrany", "2023-06-12"),
        ("Gra 9", "Wynik 9", "110", "Oczekujący", "2023-06-11"),
        ("Gra 10", "Wynik 10", "180", "Wygrany", "2023-06-10")
    ]

    for zaklad in zaklady:
        game_name, bet_result, bet_value, bet_status, bet_date = zaklad
        card = BetCard(zaklady_inner_frame, game_name, bet_value, bet_result, bet_status, bet_date)
        card.pack(pady=20, fill="x", expand=1)

    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox("all"))

    right_column = ttk.Frame(root)
    right_column.pack(side=ttk.LEFT)

    mecze_label = ttk.Label(right_column, text="Lista meczy:")
    mecze_label.pack(anchor=ttk.W, pady=(0, 10))

    # Dodanie przewijania do listy meczów
    mecze_frame = ttk.Frame(right_column, relief=ttk.SOLID)
    mecze_frame.pack(fill=ttk.BOTH, expand=True)

    mecze_canvas = ttk.Canvas(mecze_frame)
    mecze_canvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)

    mecze_scrollbar = ttk.Scrollbar(mecze_frame, orient=ttk.VERTICAL, command=mecze_canvas.yview)
    mecze_scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

    mecze_canvas.configure(yscrollcommand=mecze_scrollbar.set)
    mecze_canvas.bind("<Configure>", lambda e: mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all")))

    mecze_inner_frame = ttk.Frame(mecze_canvas)
    mecze_canvas.create_window((0, 0), window=mecze_inner_frame, anchor=ttk.NW)

    mecze_inner_frame.bind("<Configure>", lambda e: mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all")))

    mecze = [
        ("Match 1", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 2", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 3", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 4", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 5", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 6", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 7", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 8", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 9", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 10", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data")
    ]

    # Dodawanie kart meczów
    for mecz in mecze:
        match_name, team_1, team_2, country, city, discipline, date = mecz
        card = MatchCard(mecze_inner_frame, match_name, team_1, team_2, country, city, discipline, date)
        card.pack(pady=20, fill=ttk.X)

    mecze_canvas.update_idletasks()
    mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all"))


# Widok panelu użytkkownika
def show_user_panel(username):
    clear_window()

    user_label = ttk.Label(root, text="Panel użytkkownika", font=("Arial", 16))
    user_label.pack(pady=10)

    left_column = ttk.Frame(root)
    left_column.pack(side=ttk.LEFT, padx=50)

    login_value_label = ttk.Label(left_column, text="Zalogowano jako:")
    login_value_label.pack(anchor=ttk.W, padx=(20, 10), pady=(5, 5))

    login_value = ttk.Label(left_column, text=f"{username}")
    login_value.pack(anchor=ttk.W, padx=(20, 10))

    balance_label = ttk.Label(left_column, text="Aktualny balans konta:")
    balance_label.pack(anchor=ttk.W, padx=(20, 10), pady=(20, 10))

    balance_value = ttk.Label(left_column, text="", font=("Arial", 22))
    balance_value.pack(anchor=ttk.W, padx=(20, 10), pady=(20, 10))

    # Pobieranie aktualnego salda z bazy danych
    balance = database.mysql_select(table="user", column="user_balance", conditions=f"where user_login = '{username}';")
    balance_value.config(text=f"${balance[0]}")

    logout_button = ttk.Button(root, text="Wyloguj", width=10,  bootstyle=(INFO, OUTLINE), command=logout)
    logout_button.pack(side=ttk.BOTTOM, padx=(750, 0), pady=(0, 20))

    middle_column = ttk.Frame(root)
    middle_column.pack(side=ttk.LEFT, padx=50)

    zaklady_label = ttk.Label(middle_column, text="Twoje zakłady:")
    zaklady_label.pack(anchor=ttk.W, pady=(0, 10))

    # Dodanie przewijania do listy zakładów
    zaklady_frame = ttk.Frame(middle_column, relief=ttk.SOLID)
    zaklady_frame.pack(fill=ttk.BOTH, expand=True)

    canvas = ttk.Canvas(zaklady_frame)
    canvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(zaklady_frame, orient=ttk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    zaklady_inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=zaklady_inner_frame, anchor=ttk.NW)

    zaklady_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    zaklady = [
        ("Gra 1", "Wynik 1", "100", "Wygrany", "2023-06-19"),
        ("Gra 2", "Wynik 2", "50", "Przegrany", "2023-06-18"),
        ("Gra 3", "Wynik 3", "200", "Oczekujący", "2023-06-17"),
        ("Gra 4", "Wynik 4", "150", "Wygrany", "2023-06-16"),
        ("Gra 5", "Wynik 5", "80", "Przegrany", "2023-06-15"),
        ("Gra 6", "Wynik 6", "120", "Oczekujący", "2023-06-14"),
        ("Gra 7", "Wynik 7", "90", "Wygrany", "2023-06-13"),
        ("Gra 8", "Wynik 8", "70", "Przegrany", "2023-06-12"),
        ("Gra 9", "Wynik 9", "110", "Oczekujący", "2023-06-11"),
        ("Gra 10", "Wynik 10", "180", "Wygrany", "2023-06-10")
    ]

    for zaklad in zaklady:
        game_name, bet_result, bet_value, bet_status, bet_date = zaklad
        card = BetCard(zaklady_inner_frame, game_name, bet_value, bet_result, bet_status, bet_date)
        card.pack(pady=5, fill=ttk.X)

    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox("all"))

    right_column = ttk.Frame(root)
    right_column.pack(side=ttk.LEFT)

    mecze_label = ttk.Label(right_column, text="Dostępne mecze do obstawienia:")
    mecze_label.pack(anchor=ttk.W, pady=(0, 10))

    # Dodanie przewijania do listy meczów
    mecze_frame = ttk.Frame(right_column, relief=ttk.SOLID)
    mecze_frame.pack(fill=ttk.BOTH, expand=True)

    mecze_canvas = ttk.Canvas(mecze_frame)
    mecze_canvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)

    mecze_scrollbar = ttk.Scrollbar(mecze_frame, orient=ttk.VERTICAL, command=mecze_canvas.yview)
    mecze_scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

    mecze_canvas.configure(yscrollcommand=mecze_scrollbar.set)
    mecze_canvas.bind("<Configure>", lambda e: mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all")))

    mecze_inner_frame = ttk.Frame(mecze_canvas)
    mecze_canvas.create_window((0, 0), window=mecze_inner_frame, anchor=ttk.NW)

    mecze_inner_frame.bind("<Configure>", lambda e: mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all")))

    mecze = [
        ("Match 1", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 2", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 3", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 4", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 5", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 6", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 7", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 8", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 9", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data"),
        ("Match 10", "Zespół 1", "Zespół 2", "Kraj", "Miasto", "Dyscyplina", "Data")
    ]

    # Dodawanie kart meczów
    for mecz in mecze:
        match_name, team_1, team_2, country, city, discipline, date = mecz
        card = MatchCard(mecze_inner_frame, match_name, team_1, team_2, country, city, discipline, date)
        card.pack(pady=5, fill=ttk.X)

    mecze_canvas.update_idletasks()
    mecze_canvas.configure(scrollregion=mecze_canvas.bbox("all"))


# Funkcja do czyszczenia okna
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# Wyświetlanie widoku logowania jako domyślnego widoku startowego
show_login()

root.mainloop()
