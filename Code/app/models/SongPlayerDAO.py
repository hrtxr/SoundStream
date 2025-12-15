import sqlite3
from app import app
from app.models.SongPlayer import SongPlayer
from app.models.SongPlayerDAOInterface import SongPlayerDAOInterface

class SongPlayerDAO(SongPlayerDAOInterface) :
    
    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'
    
    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn
    
    def createSongPlayer(self, name_place, IP_adress, state, last_synchronization, place_adress, id_orga) :
        
        conn = self._getDbConnection()
        
        query = '''INSERT INTO song_player (name_place , Ip_adress, state ,last_synchronization , place_address , id_orga)
                      VALUES (?,?,?,?,?,?) ;'''
        conn.execute(query,(name_place, IP_adress, state, last_synchronization, place_adress, id_orga))
        conn.commit()
        conn.close()
            

    def findByIpAdress(self, ip):
        conn = self._getDbConnection()
        # Use a parameterized query to prevent SQL injection
        res = conn.execute('SELECT * FROM song_player WHERE IP_adress = ?;', (ip,)).fetchone()
        conn.close()

        if res:
            return SongPlayer(dict(res))
        return None
    
    def findByOrganisation(self, name_orga) :
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player JOIN organization USING(id_orga) WHERE name_orga = ?;', (name_orga,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList:
            return songplayerList
        return None
    
    def findByState(self, state) :
        """ Get song player by state """
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player WHERE state = ?;', (state,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers :
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList:
            return songplayerList
        return None
    
    def findAllByOrganisation(self, id_orga):
        conn = self._getDbConnection()
        songplayers = conn.execute("""SELECT * FROM song_player WHERE id_orga = ?;""", (id_orga,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList :
            return songplayerList
        return []
    
    def findAll(self):
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player;').fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList :
            return songplayerList
        return None
    
    def UpdateState(self, state, id_player) :
        ''' Update the state of a song player '''
        conn = self._getDbConnection()
        conn.execute('UPDATE song_player SET state = ? WHERE id_player =  ?;', (state,id_player))
        conn.commit() 
        conn.close()
