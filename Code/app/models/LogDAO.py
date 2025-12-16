from app import app
import sqlite3
from app.models.LogDAOInterface import LogDAOInterface

class LogDAO(LogDAOInterface):

    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def findAllByOrganisation(self, id_orga):
        conn = self._getDbConnection()
        query = "SELECT * FROM log WHERE id_orga = ?"

        cursor = conn.execute(query, (id_orga,))
        rows = cursor.fetchall()

        result = [dict(row) for row in rows]

        conn.close()

        return result