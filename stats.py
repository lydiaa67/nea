import sqlite3

class Database_for_stats:
    def __init__(self, db_name="stats.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0
                )
            """)
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (1, 0, 0, 0)")
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (2, 0, 0, 0)")
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (3, 0, 0, 0)")
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (4, 0, 0, 0)")
            conn.commit()

    def update_stats(self, result, difficulty):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if difficulty == "easy":
                if result == "win":
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 1")
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 4")
                elif result == "loss":
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 1")
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 4")
                elif result == "draw":
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 1")
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 4")
            elif difficulty == "medium":
                if result == "win":
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 2")
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 4")
                elif result == "loss":
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 2")
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 4")
                elif result == "draw":
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 2")
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 4")
            else:  # hard
                if result == "win":
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 3")
                    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 4")
                elif result == "loss":
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 3")
                    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 4")
                elif result == "draw":
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 3")
                    cursor.execute("UPDATE stats SET draws = draws + 1 WHERE id = 4")
            conn.commit()

    def get_stats(self): 
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Fetch each row separately
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 1")
            stats1 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 2")
            stats2 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 3")
            stats3 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 4")
            stats4 = cursor.fetchone() or (0, 0, 0)
            return stats1, stats2, stats3, stats4  
    

    def reset_stats(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 1")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 2")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 3")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 4")
            conn.commit()

if __name__ == "__main__":
    stats = Database_for_stats()
    print("Current stats:", stats.get_stats())  
    stats.reset_stats() 
    print("Updated stats:", stats.get_stats()) 