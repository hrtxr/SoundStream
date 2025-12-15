from app import app
import sqlite3
from app.models.OrganisationDAOInterface import OrganisationDAOInterface

class OrganisationDAO(OrganisationDAOInterface):
    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def getIdByName(self, orga_name):
        conn = self._getDbConnection()
        query = """ SELECT id_orga FROM organisation WHERE name_orga = ? """

        cursor = conn.execute(query, (orga_name,))
        result = cursor.fetchone()
        
        conn.close()
        
        # Si un résultat est trouvé, result est un tuple comme (112,)
        if result:
            return result[0] # On retourne juste le chiffre 112
        
        return None