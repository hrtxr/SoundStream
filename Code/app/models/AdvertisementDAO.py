import sqlite3
from typing import List, Dict, Optional

class AdvertisementDAO:
    def __init__(self, db_path="app/static/database/database.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def createAdvertisement(self, id_file: int, id_orga: int, play_date: str, play_time: str) -> int:
        query = """
            INSERT INTO advertisement (id_file, id_orga, play_date, play_time, played)
            VALUES (?, ?, ?, ?, 0)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_file, id_orga, play_date, play_time))
            conn.commit()
            return cursor.lastrowid

    def getPendingAdvertisements(self, current_date: str, current_time: str) -> List[Dict]:
        query = """
            SELECT a.id_ad, a.id_file, a.id_orga, f.name, f.path
            FROM advertisement a
            JOIN file f ON a.id_file = f.id_file
            WHERE a.played = 0 
              AND (a.play_date < ? OR (a.play_date = ? AND a.play_time <= ?))
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (current_date, current_date, current_time))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def markAsPlayed(self, id_ad: int) -> bool:
        query = "UPDATE advertisement SET played = 1 WHERE id_ad = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_ad,))
            conn.commit()
            return cursor.rowcount > 0
