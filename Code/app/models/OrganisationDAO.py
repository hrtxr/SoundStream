from app import app
import sqlite3
from app.models.OrganisationDAOInterface import OrganisationDAOInterface

class OrganisationDAO(OrganisationDAOInterface):
    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def createOrganisation(self, name_orga, subsidiary) :
        conn = self._getDbConnection()
        try:
            query = "INSERT INTO organisation (name_orga, subsidiary) VALUES (?, ?);"
            conn.execute(query, (name_orga,subsidiary))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception("Error creating organisation : " + str(e)) # On signale l'erreur s'il y a un problème de création (= Exception levée)
        finally:
            conn.close()
            
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
    
    def findUserOrganisation(self, username):
        """ Get the organisation of a user by username """
        conn = self._getDbConnection()
        query = """
            SELECT o.name_orga 
            FROM user_ u
            JOIN work_link w ON u.id_user = w.id_user
            JOIN organisation o ON w.id_orga = o.id_orga
            WHERE u.username = ?
        """
        res = conn.execute(query, (username,)).fetchall()
        conn.close()
        return [row[0] for row in res]
    
    def getAllOrganisations(self):
        conn = self._getDbConnection()
        query = "SELECT * FROM organisation"

        cursor = conn.execute(query)
        results = cursor.fetchall()
        
        conn.close()
        
        return results