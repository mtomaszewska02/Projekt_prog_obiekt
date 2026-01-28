import json
import os
from datetime import datetime


class LeaderBoard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.load_data()

    def load_data(self):
        """Ładuje dane z pliku JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = []
        else:
            self.data = []

    def save_data(self):
        """Zapisuje dane do pliku JSON"""
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_score(self, nickname, score):
        """Dodaje nowy wynik do tabeli"""
        entry = {
            "nickname": nickname,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data.append(entry)
        self.sort_data()
        self.keep_top_10()
        self.save_data()

    def sort_data(self):
        """Sortuje wyniki malejąco"""
        self.data.sort(key=lambda x: x["score"], reverse=True)

    def keep_top_10(self):
        """Utrzymuje tylko top 10"""
        if len(self.data) > 10:
            self.data = self.data[:10]

    def get_top_10(self):
        """Zwraca top 10 unikalnych wyników (jeden na gracza)"""
        unique_players = {}

        # Przechodzimy przez wszystkie wyniki (posortowane już malejąco)
        for entry in self.data:
            name = entry['nickname']
            score = entry['score']

            # Jeśli gracza nie ma w słowniku, dodajemy go.
            # Ponieważ dane są posortowane, pierwszy napotkany wynik danego gracza jest jego najlepszym.
            if name not in unique_players:
                unique_players[name] = entry

        # Zamieniamy słownik z powrotem na listę i bierzemy pierwsze 10 elementów
        return list(unique_players.values())[:10]

    def get_player_rank(self, nickname, score):
        """Zwraca pozycję gracza w rankingu (1-10) lub -1 jeśli poza top 10"""
        temp_data = self.data + [{"nickname": nickname, "score": score, "date": ""}]
        temp_data.sort(key=lambda x: x["score"], reverse=True)

        for i, entry in enumerate(temp_data[:10], 1):
            if entry["nickname"] == nickname and entry["score"] == score:
                return i
        return -1

    def is_top_10(self, score):
        """Sprawdza czy wynik wchodzi do top 10"""
        if len(self.data) < 10:
            return True
        return score > self.data[-1]["score"]

    def is_first_place(self, nickname, score):
        """Sprawdza czy gracz zajął 1 miejsce"""
        if not self.data:
            return True
        if self.data[0]["score"] == score and self.data[0]["nickname"] == nickname:
            return True
        return False