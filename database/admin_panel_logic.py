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
    country = database.mysql_select(column="id", table="country", conditions=f"WHERE country_name = '{country_name}'")
    city = database.mysql_select(column="id", table="city", conditions=f"WHERE city_name = '{city_name}'")
    country = country[0]
    city = city[0]
    database.mysql_insert(table="player",
                          columns="`player_firstname`, `player_surname`, `player_age`, `country_id`, `city_id`",
                          values="%s, %s, %s, %s, %s",
                          params=(player_firstname, player_surname, player_age, country, city))
    messagebox.showinfo("Operacja pomyślna", f"Dodano gracza do bazy danych")
    root.destroy()


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
                               command=lambda: add_player(player_firstname_entry.get(), player_surname_entry.get(),
                                                          player_age_entry.get(), player_country_combobox.get(),
                                                          player_city_combobox.get(), add_player_window))
    player_button.pack(pady=10)


def add_team(team_country, team_city, team_name, root):
    country = database.mysql_select(column="id", table="country", conditions=f"WHERE country_name = '{team_country}'")
    city = database.mysql_select(column="id", table="city", conditions=f"WHERE city_name = '{team_city}'")
    country = country[0]
    city = city[0]
    database.mysql_insert(table="team",
                          columns="`country_id`, `city_id`, `team_name`",
                          values="%s, %s, %s",
                          params=(country, city, team_name))
    messagebox.showinfo("Operacja pomyślna", f"Dodano drużynę do bazy danych")
    root.destroy()


def show_add_team_window(root):
    add_team_window = ttk.Toplevel(root)
    add_team_window.title("Dodawanie drużyny")
    add_team_window.geometry("800x700+700+150")
    add_team_window.transient(root)

    team_name_label = ttk.Label(add_team_window, text="Nazwa Drużyny")
    team_name_label.pack(pady=10)
    team_name_entry = ttk.Entry(add_team_window)
    team_name_entry.pack(pady=(0, 20))

    team_country_label = ttk.Label(add_team_window, text="Kraj")
    team_country_label.pack(pady=10)
    countries = database.mysql_select(table="country", column="country_name")
    team_country_combobox = ttk.Combobox(add_team_window, values=countries)
    team_country_combobox.pack(pady=(0, 20))

    team_city_label = ttk.Label(add_team_window, text="Miasto")
    team_city_label.pack(pady=10)
    cities = database.mysql_select(table="city", column="city_name")
    team_city_combobox = ttk.Combobox(add_team_window, values=cities)
    team_city_combobox.pack(pady=(0, 20))

    team_button = ttk.Button(add_team_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                             command=lambda: add_team(team_country_combobox.get(), team_city_combobox.get(),
                                                      team_name_entry.get(), add_team_window))
    team_button.pack(pady=10)


def add_game(game_name, game_discipline, game_country, game_city, cal, root):
    discipline = database.mysql_select(column="id", table="discipline",
                                       conditions=f"WHERE discipline_name = '{game_discipline}'")
    country = database.mysql_select(column="id", table="country", conditions=f"WHERE country_name = '{game_country}'")
    city = database.mysql_select(column="id", table="city", conditions=f"WHERE city_name = '{game_city}'")
    country = country[0]
    city = city[0]
    discipline = discipline[0]
    database.mysql_insert(table="game",
                          columns="`game_name`, `discipline_id`, `country_id`, `city_id`, `game_date`",
                          values="%s, %s, %s, %s, %s",
                          params=(game_name, discipline, country, city, cal))
    messagebox.showinfo("Operacja pomyślna", f"Dodano mecz do bazy danych")
    root.destroy()


def show_add_game_window(root):
    add_game_window = ttk.Toplevel(root)
    add_game_window.title("Dodawanie meczu")
    add_game_window.geometry("800x700+700+150")
    add_game_window.transient(root)

    game_name_label = ttk.Label(add_game_window, text="Nazwa meczu")
    game_name_label.pack(pady=10)
    game_name_entry = ttk.Entry(add_game_window)
    game_name_entry.pack(pady=(0, 20))

    game_discipline_label = ttk.Label(add_game_window, text="Dyscyplina")
    game_discipline_label.pack(pady=10)
    disciplines = database.mysql_select(table="discipline", column="discipline_name")
    game_discipline_combobox = ttk.Combobox(add_game_window, values=disciplines)
    game_discipline_combobox.pack(pady=(0, 20))

    game_country_label = ttk.Label(add_game_window, text="Kraj")
    game_country_label.pack(pady=10)
    countries = database.mysql_select(table="country", column="country_name")
    game_country_combobox = ttk.Combobox(add_game_window, values=countries)
    game_country_combobox.pack(pady=(0, 20))

    game_city_label = ttk.Label(add_game_window, text="Miasto")
    game_city_label.pack(pady=10)
    cities = database.mysql_select(table="city", column="city_name")
    game_city_combobox = ttk.Combobox(add_game_window, values=cities)
    game_city_combobox.pack(pady=(0, 20))

    game_date_label = ttk.Label(add_game_window, text="Data")
    game_date_label.pack(pady=10)
    game_date_entry = ttk.Entry(add_game_window)
    game_date_entry.pack(pady=(0, 20))

    game_button = ttk.Button(add_game_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                             command=lambda: add_game(game_name_entry.get(), game_discipline_combobox.get(),
                                                      game_country_combobox.get(), game_city_combobox.get(),
                                                      game_date_entry.get(), add_game_window))
    game_button.pack(pady=10)


def add_score(score_game, score_value, root):
    score = database.mysql_select(column="id", table="score", conditions=f"WHERE score_value = '{score_value}'")
    score = score[0]
    database.mysql_update(table="game", values=f"score_id = {score}", conditions=f"game_name = '{score_game}'")
    messagebox.showinfo("Operacja pomyślna", f"Ogłoszono wynik meczu!")
    root.destroy()


def show_add_score_window(root):
    add_score_window = ttk.Toplevel(root)
    add_score_window.title("Ogłaszanie wyniku meczu")
    add_score_window.geometry("800x700+700+150")
    add_score_window.transient(root)

    score_game_label = ttk.Label(add_score_window, text="Wybierz mecz")
    score_game_label.pack(pady=10)
    games = database.mysql_select(table="game", column="game_name", conditions="WHERE score_id is NULL")
    score_game_combobox = ttk.Combobox(add_score_window, values=games)
    score_game_combobox.pack(pady=(0, 20))

    score_value_label = ttk.Label(add_score_window, text="Wybierz wynik")
    score_value_label.pack(pady=10)
    values = database.mysql_select(table="score", column="score_value")
    score_value_combobox = ttk.Combobox(add_score_window, values=values)
    score_value_combobox.pack(pady=(0, 20))

    score_button = ttk.Button(add_score_window, text="Ogłoś wynik", bootstyle=(SUCCESS, OUTLINE),
                              command=lambda: add_score(score_game_combobox.get(), score_value_combobox.get(),
                                                        add_score_window))
    score_button.pack(pady=10)


def add_team_player(team_name, player_name, root):
    team = database.mysql_select(column="id", table="team", conditions=f"WHERE team_name = '{team_name}'")
    player = database.mysql_select(column="id", table="player", conditions=f"WHERE CONCAT(player_firstname, ' ', player_surname) = '{player_name}'")
    team = team[0]
    player = player[0]

    database.mysql_insert(table="team_player",
                          columns="`team_id`, `player_id`",
                          values="%s, %s",
                          params=(team, player))
    messagebox.showinfo("Operacja pomyślna", f"Dodano gracza do drużyny!")
    root.destroy()


def show_add_team_player_window(root):
    add_team_player_window = ttk.Toplevel(root)
    add_team_player_window.title("Dodawanie gracza do drużyny")
    add_team_player_window.geometry("800x700+700+150")
    add_team_player_window.transient(root)

    team_player_tname_label = ttk.Label(add_team_player_window, text="Wybierz drużyne")
    team_player_tname_label.pack(pady=10)
    teams = database.mysql_select(table="team", column="team_name")
    team_player_tname_combobox = ttk.Combobox(add_team_player_window, values=teams)
    team_player_tname_combobox.pack(pady=(0, 20))

    team_player_pname_label = ttk.Label(add_team_player_window, text="Wybierz gracza")
    team_player_pname_label.pack(pady=10)
    players = database.mysql_select(table="player", column="CONCAT(player_firstname, ' ', player_surname)")
    team_player_pname_combobox = ttk.Combobox(add_team_player_window, values=players)
    team_player_pname_combobox.pack(pady=(0, 20))

    team_player_button = ttk.Button(add_team_player_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                              command=lambda: add_team_player(team_player_tname_combobox.get(), team_player_pname_combobox.get(), add_team_player_window))
    team_player_button.pack(pady=10)


def add_game_team(game_name, team_name, root):
    team = database.mysql_select(column="id", table="team", conditions=f"WHERE team_name = '{team_name}'")
    game = database.mysql_select(column="id", table="game", conditions=f"WHERE game_name = '{game_name}'")
    team = team[0]
    game = game[0]

    database.mysql_insert(table="game_team",
                          columns="`game_id`, `team_id`",
                          values="%s, %s",
                          params=(game, team))
    messagebox.showinfo("Operacja pomyślna", f"Dodano drużynę do meczu!")
    root.destroy()


def show_add_game_team_window(root):
    add_game_team_window = ttk.Toplevel(root)
    add_game_team_window.title("Dodawanie drużyny do meczu")
    add_game_team_window.geometry("800x700+700+150")
    add_game_team_window.transient(root)

    game_team_gname_label = ttk.Label(add_game_team_window, text="Wybierz mecz")
    game_team_gname_label.pack(pady=10)
    games = database.mysql_select(table="game g", column="g.game_name", conditions="LEFT JOIN game_team gt ON g.id = gt.game_id GROUP BY g.id HAVING COUNT(gt.game_id) < 2")
    game_team_gname_combobox = ttk.Combobox(add_game_team_window, values=games)
    game_team_gname_combobox.pack(pady=(0, 20))

    game_team_tname_label = ttk.Label(add_game_team_window, text="Wybierz drużyne")
    game_team_tname_label.pack(pady=10)
    teams = database.mysql_select(table="team", column="team_name")
    game_team_tname_combobox = ttk.Combobox(add_game_team_window, values=teams)
    game_team_tname_combobox.pack(pady=(0, 20))

    game_team_button = ttk.Button(add_game_team_window, text="Dodaj", bootstyle=(SUCCESS, OUTLINE),
                                    command=lambda: add_game_team(game_team_gname_combobox.get(), game_team_tname_combobox.get(), add_game_team_window))
    game_team_button.pack(pady=10)
