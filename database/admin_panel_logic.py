import ttkbootstrap as ttk
from tkinter import messagebox

from ttkbootstrap import SUCCESS, OUTLINE, DANGER, DEFAULT

from database.database_handler import DatabasePointer

database = DatabasePointer


def add_discipline(discipline, root):
    disciplines = database.mysql_select(column="discipline_name", table="discipline")

    if discipline in disciplines:
        messagebox.showerror("Błąd", "Dyscyplina już znajduje się w bazie")
        root.country_entry.delete(0, ttk.END)
    else:
        database.mysql_insert(table="discipline",
                              columns="`discipline_name`",
                              values="%s", params=discipline)
        messagebox.showinfo("Operacja pomyślna", f"Dodano {discipline} do bazy danych")
        root.destroy()


def show_add_discipline_window(root):
    add_discipline_window = ttk.Toplevel(root)
    add_discipline_window.title("Dodawanie dyscypliny")
    add_discipline_window.geometry("800x600+700+150")
    add_discipline_window.transient(root)

    discipline_label = ttk.Label(add_discipline_window, text="Wpisz nazwę dyscypliny")
    discipline_label.pack(pady=10)
    discipline_entry = ttk.Entry(add_discipline_window)
    discipline_entry.pack(pady=(0, 20))

    discipline_button = ttk.Button(add_discipline_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                                   command=lambda: add_discipline([discipline_entry.get()], add_discipline_window))
    discipline_button.pack(pady=10)


def add_country(country, root):
    countries = database.mysql_select(column="country_name", table="country")

    if country in countries:
        messagebox.showerror("Błąd", "Kraj już znajduje się w bazie")
        root.country_entry.delete(0, ttk.END)
    else:
        database.mysql_insert(table="country",
                              columns="`country_name`",
                              values="%s", params=country)
        messagebox.showinfo("Operacja pomyślna", f"Dodano {country} do bazy danych")
        root.destroy()


def show_add_country_window(root):
    add_country_window = ttk.Toplevel(root)
    add_country_window.title("Dodawanie kraju")
    add_country_window.geometry("800x600+700+150")
    add_country_window.transient(root)

    country_label = ttk.Label(add_country_window, text="Wpisz nazwę kraju")
    country_label.pack(pady=10)
    country_entry = ttk.Entry(add_country_window)
    country_entry.pack(pady=(0, 20))

    country_button = ttk.Button(add_country_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                                command=lambda: add_country([country_entry.get()], add_country_window))
    country_button.pack(pady=10)


def add_city(city, root):
    cities = database.mysql_select(column="city_name", table="city")

    if city in cities:
        messagebox.showerror("Błąd", "Miasto już znajduje się w bazie")
        root.city_entry.delete(0, ttk.END)
    else:
        database.mysql_insert(table="city",
                              columns="`city_name`",
                              values="%s", params=city)
        messagebox.showinfo("Operacja pomyślna", f"Dodano {city} do bazy danych")
        root.destroy()


def show_add_city_window(root):
    add_city_window = ttk.Toplevel(root)
    add_city_window.title("Dodawanie miasta")
    add_city_window.geometry("800x600+700+150")
    add_city_window.transient(root)

    city_label = ttk.Label(add_city_window, text="Wpisz nazwę miasta")
    city_label.pack(pady=10)
    city_entry = ttk.Entry(add_city_window)
    city_entry.pack(pady=(0, 20))

    city_button = ttk.Button(add_city_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                             command=lambda: add_city([city_entry.get()], add_city_window))
    city_button.pack(pady=10)


def add_player(player_firstname, player_surname, player_age, country_name, city_name, root):
    return


def show_add_player_window(root):
    add_player_window = ttk.Toplevel(root)
    add_player_window.title("Dodawanie gracza")
    add_player_window.geometry("800x700+700+150")
    add_player_window.transient(root)

    player_firstname_label = ttk.Label(add_player_window, text="Imię")
    player_firstname_label.pack(pady=10)
    player_firstname_entry = ttk.Entry(add_player_window)
    player_firstname_entry.pack(pady=(0, 20))

    player_surname_label = ttk.Label(add_player_window, text="Nazwisko")
    player_surname_label.pack(pady=10)
    player_surname_entry = ttk.Entry(add_player_window)
    player_surname_entry.pack(pady=(0, 20))

    player_age_label = ttk.Label(add_player_window, text="Wiek")
    player_age_label.pack(pady=10)
    player_age_entry = ttk.Entry(add_player_window)
    player_age_entry.pack(pady=(0, 20))

    player_country_label = ttk.Label(add_player_window, text="Kraj")
    player_country_label.pack(pady=10)

    countries = database.mysql_select(table="country", column="country_name")

    player_country_combobox = ttk.Combobox(add_player_window, values=countries)
    player_country_combobox.pack(pady=(0, 20))

    city_label = ttk.Label(add_player_window, text="Miasto")
    city_label.pack(pady=10)

    cities = database.mysql_select(table="city", column="city_name")

    player_city_combobox = ttk.Combobox(add_player_window, values=cities)
    player_city_combobox.pack(pady=(0, 20))


    player_button = ttk.Button(add_player_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                               command=lambda: add_player(player_firstname_entry.get(), player_surname_entry.get(), player_age_entry.get(), player_country_combobox.get(),player_city_combobox.get(), add_player_window))
    player_button.pack(pady=10)


def add_team(root):
    return

def show_add_team_window(root):
    return


def add_game(root):
    return

def show_add_game_window(root):
    return


def add_score(root):
    return

def show_add_score_window(root):
    return
