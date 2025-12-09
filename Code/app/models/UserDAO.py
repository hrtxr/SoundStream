import sqlite3
from app import app
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface

import bcrypt

class UserDAO(UserDAOInterface) :
    
    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'
    
    def _getDbConnection(self):
        """ connection à la base de données. Retourne l'objet connection """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _generatePWDHash(self, password) :
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        password_hashed = hashed_bytes.decode('utf-8')
        return password_hashed
    
    def createUser(self, username, password, role):
        pass

    def findByUsername(self, username):
        """ Récupère un utilisateur par son username """
        conn = self._getDbConnection()
        # On utilise une requête paramétrée pour éviter les injections SQL
        res = conn.execute('SELECT * FROM user_ WHERE username = ?', (username,)).fetchone()
        conn.close()

        if res:
            return User(dict(res))
        return None
    
    def findAll(self):
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM user_ ;').fetchall()
        userList = list()
        for user in users : 
            userList.append(User(dict(user)))
        conn.close()
        return userList