import sqlite3
from app import app
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface

import bcrypt

class UserDAO(UserDAOInterface) :
    
    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'
    
    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _generatePWDHash(self, password) :
        """ Generate password hash from plain text password """
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        password_hashed = hashed_bytes.decode('utf-8')
        return password_hashed
    
    def createUser(self, username, password, role):
        """ Create a new user """
        pass

    def findByUsername(self, username):
        """ Get user by username """
        conn = self._getDbConnection()
        # Use a parameterized query to prevent SQL injection
        res = conn.execute('SELECT * FROM user_ WHERE username = ?', (username,)).fetchone()
        conn.close()

        if res:
            return User(dict(res))
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
        
    def  findAll(self):
        """ Get all users """
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM user_ ;').fetchall()
        userList = list()
        for user in users : 
            userList.append(User(dict(user)))
        conn.close()
        return userList