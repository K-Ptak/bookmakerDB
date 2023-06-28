import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap import SUCCESS, OUTLINE, DANGER, DEFAULT

from database.database_handler import DatabasePointer

database = DatabasePointer


def add_bet(user_balance, game, score, balance_entry, username, root):
    balance_entry = float(balance_entry)
    user_balance = float(user_balance[0])
    if user_balance >= balance_entry:
        new_balance = user_balance - balance_entry
        user_id = database.mysql_select(table="user", column="id", conditions=f"WHERE user_login = '{username}'")
        game_id = database.mysql_select(table="game", column="id", conditions=f"WHERE game_name = '{game}'")
        score_id = database.mysql_select(table="score", column="id", conditions=f"WHERE score_value = '{score}'")
        user_id = user_id[0]
        game_id = game_id[0]
        score_id = score_id[0]
        database.mysql_update(table="user", values=f"user_balance = {new_balance}", conditions=f"user_login = '{username}'")
        database.mysql_insert(table="bet",
                              columns="`user_id`, `game_id`, `bet_value`, `score_id`, `result_id`",
                              values="%s, %s, %s, %s, %s",
                              params=(user_id, game_id, balance_entry, score_id, '3'))
        messagebox.showinfo("Operacja pomyślna", f"Obstawiono mecz")

    else:
        messagebox.showerror("Brak środków", "Za mało środków by dokonać zakładu!")
    return


def show_add_bet_window(balance, username, root):
    add_bet_window = ttk.Toplevel(root)
    add_bet_window.title("Stawianie zakładu")
    add_bet_window.geometry("800x700+700+150")
    add_bet_window.transient(root)

    user_id = database.mysql_select(table="user", column="id", conditions=f"WHERE user_login = '{username}'")
    user_id = user_id[0]

    game_label = ttk.Label(add_bet_window, text="Wybierz mecz, który chcesz obstawić")
    game_label.pack(pady=10)
    games = database.mysql_select(table="game", column="game_name", conditions=f"WHERE id NOT IN (SELECT game_id FROM bet WHERE user_id = {user_id})")
    game_combobox = ttk.Combobox(add_bet_window, values=games)
    game_combobox.pack(pady=(0, 20))

    score_label = ttk.Label(add_bet_window, text="Wybierz wynik, który chcesz obstawić")
    score_label.pack(pady=10)
    scores = database.mysql_select(table="score", column="score_value")
    score_combobox = ttk.Combobox(add_bet_window, values=scores)
    score_combobox.pack(pady=(0, 20))

    balance_label = ttk.Label(add_bet_window, text="Podaj kwote")
    balance_label.pack(pady=10)
    balance_entry = ttk.Entry(add_bet_window)
    balance_entry.pack(pady=(0, 20))

    bet_button = ttk.Button(add_bet_window, text="Postaw zakład", bootstyle=(SUCCESS, OUTLINE),
                                    command=lambda: add_bet(balance, game_combobox.get(), score_combobox.get(), balance_entry.get(), username, add_bet_window))
    bet_button.pack(pady=10)


def show_players(team_name, root):
    show_players_window = ttk.Toplevel(root)
    show_players_window.title("Zawodnicy")
    show_players_window.geometry("800x600+700+150")
    show_players_window.transient(root)

    team = database.mysql_select(column="id", table="team", conditions=f"WHERE team_name = '{team_name}'")
    team = team[0]
    players = database.mysql_select(
        table=f"player p JOIN country c ON p.country_id = c.id JOIN city ct ON p.city_id = ct.id JOIN team_player tp ON p.id = tp.player_id WHERE tp.team_id = '{team}'",
        column="CONCAT(p.player_firstname, ' ', p.player_surname, ' ', p.player_age, ' lata ', c.country_name, ' ', ct.city_name) AS player_info",
        multiple="yes"
    )

    players.sort()

    text = ttk.Text(show_players_window)
    text.pack(side="left", padx=100, pady=(0, 100))
    sb = ttk.Scrollbar(show_players_window, command=text.yview)
    sb.pack(side="right")
    text.configure(yscrollcommand=sb.set)

    for i in players:
        player_label = ttk.Label(show_players_window, text=i[0])
        player_label.pack(padx=10, pady=(5, 5), fill=ttk.BOTH, expand=1)
        text.window_create("end", window=player_label)
        text.insert("end", "\n")

    root.destroy()


def show_team_players_window(root):
    team_players_window = ttk.Toplevel(root)
    team_players_window.title("Wyświetlanie zawodników")
    team_players_window.geometry("800x700+700+150")
    team_players_window.transient(root)

    team_player_label = ttk.Label(team_players_window, text="Wybierz drużyne")
    team_player_label.pack(pady=10)
    teams = database.mysql_select(table="team", column="team_name")
    team_player_combobox = ttk.Combobox(team_players_window, values=teams)
    team_player_combobox.pack(pady=(0, 20))

    team_player_button = ttk.Button(team_players_window, text="Wyświetl", bootstyle=(SUCCESS, OUTLINE),
                                    command=lambda: show_players(team_player_combobox.get(), team_players_window))
    team_player_button.pack(pady=10)
