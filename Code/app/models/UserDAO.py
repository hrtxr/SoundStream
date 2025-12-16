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
        conn  = self._getDbConnection()
        """ Hash the password before storing """
        hashed_password = self._generatePWDHash(password)
        """ Insert the new user """
        query = 'INSERT INTO user_(username, password, role) VALUES (?,?,?)'
        conn.execute(query, (username,hashed_password,role))
        conn.commit()
        conn.close()
        

    def findByUsername(self, username):
        """ Get user by username """
        conn = self._getDbConnection()
        # Use a parameterized query to prevent SQL injection
        res = conn.execute('SELECT * FROM user_ WHERE username = ?', (username,)).fetchone()
        conn.close()

        if res:
            return User(dict(res))
        return None
    
    def findUsersInOrganisation(self, organisation):
        """ Get all the users of an organisation """
        conn = self._getDbConnection()
        query = """
            SELECT u.username
            FROM user_ u
            JOIN work_link w ON u.id_user = w.id_user
            JOIN organisation o ON w.id_orga = o.id_orga
            WHERE o.name_orga = ?
        """
        res = conn.execute(query, (organisation,)).fetchall()
        conn.close()
        return [row[0] for row in res]
    

    def verifyUser(self,username, password):
        """Verify if username and password are correct"""
        user = self.findByUsername(username)

        if user is None:
            return False
        
        #Check password using bcrypt 
        hashed_pw = user.password.encode('utf-8')
        input_pw = password.encode('utf-8')

        return bcrypt.checkpw(input_pw, hashed_pw)
    
    def changePassword(self, username, password):
        """Change the password of the user"""
        conn = self._getDbConnection()

        #Hash the new password
        hashed_password = self._generatePWDHash(password)

        #update the password
        query = 'UPDATE user_ SET password = ? WHERE username = ?'
        conn.execute(query, (hashed_password, username))
        conn.commit()
        conn.close()

    def deleteByUsername(self,username):
        """ Delete a user by username""" 
        conn = self._getDbConnection()

        # Delete the user 
        query = 'DELETE FROM user_ WHERE username = ?'
        conn.execute(query,(username,))
        conn.commit()
        conn.close()


    def findAll(self):
        """ Get all users """
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM user_ ;').fetchall()
        userList = list()
        for user in users : 
            userList.append(User(dict(user)))
        conn.close()
        return userList