import ttkbootstrap as ttk


class BetCard(ttk.Frame):
    def __init__(self, parent, game_name, bet_value, bet_result, bet_status, bet_date):
        super().__init__(parent, relief=ttk.SOLID)

        game_label = ttk.Label(self, text=game_name, font=("Arial", 12, "bold"))
        game_label.pack(anchor=ttk.W)

        result_label = ttk.Label(self, text=bet_result, font=("Arial", 12, "bold"))
        result_label.pack(anchor=ttk.W)

        value_label = ttk.Label(self, text=f"Kwota: {bet_value}")
        value_label.pack(anchor=ttk.W)

        status_label = ttk.Label(self, text=f"Status: {bet_status}")
        status_label.pack(anchor=ttk.W)

        date_label = ttk.Label(self, text=bet_date, font=("Arial", 9))
        date_label.pack(anchor=ttk.W)
