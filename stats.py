import sqlite3

class Database_for_stats:
    def __init__(self, db_name="stats.db"):
        self.db_name = db_name
        self._create_table() #creates the table if it does not exist

    def _create_table(self): #there needs to actually be a table to store the stats
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
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (1, 0, 0, 0)") # Default stats for each difficulty
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (2, 0, 0, 0)")
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (3, 0, 0, 0)")
            cursor.execute("INSERT OR IGNORE INTO stats (id, wins, losses, draws) VALUES (4, 0, 0, 0)")
            conn.commit()

    def update_stats(self, result, difficulty): #stats need to be updated to reflect the outcome of the game played
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            #selection statement to determine which stats to update- based on the game outcome and difficulty level
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

    def get_stats(self): #gets the stats so that they can be displayed to the player
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Fetch each row separately so that win rate can be calculated separately for each difficulty
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 1")
            stats1 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 2")
            stats2 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 3")
            stats3 = cursor.fetchone() or (0, 0, 0)
            cursor.execute("SELECT wins, losses, draws FROM stats WHERE id = 4")
            stats4 = cursor.fetchone() or (0, 0, 0)
            return stats1, stats2, stats3, stats4  

    def reset_stats(self): #resets the stats so that the player can start afresh. for when the player manually presses the button to do this.
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 1")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 2")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 3")
            cursor.execute("UPDATE stats SET wins = 0, losses = 0, draws = 0 WHERE id = 4")
            conn.commit()
    