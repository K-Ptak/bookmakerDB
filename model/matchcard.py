import ttkbootstrap as ttk


class MatchCard(ttk.Frame):
    def __init__(self, parent, match_name, team_1, team_2, country, city, discipline, date):
        super().__init__(parent, relief=ttk.SOLID)

        # Nazwa meczu
        match_name_label = ttk.Label(self, text=match_name, font=("Arial", 14, "bold"))
        match_name_label.pack(anchor=ttk.W)

        # Nazwy drużyn
        team_names_label = ttk.Label(self, text=f"{team_1} - {team_2}", font=("Arial", 12, "bold"))
        team_names_label.pack(anchor=ttk.W)

        # Lokalizacja meczu
        location_label = ttk.Label(self, text=f"{city}, {country}", font=("Arial", 10))
        location_label.pack(anchor=ttk.W)

        # Informacje o dyscyplinie
        discipline_label = ttk.Label(self, text=discipline, font=("Arial", 10))
        discipline_label.pack(anchor=ttk.W)

        # Data
        date_label = ttk.Label(self, text=date, font=("Arial", 8))
        date_label.pack(anchor=ttk.W)
