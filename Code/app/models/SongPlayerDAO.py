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

    
    def addSongPlayerInDb(self, data):
        '''
            docstring in SongPlayerDAOInterface
        '''
        conn = self._getDbConnection()
        
        query = '''
            INSERT INTO song_player
            (name_place, ip_address, state, last_synchronization, place_address, id_orga)
            VALUES (?, ?, ?, ?, ?, ?);
        '''
        conn.execute(query, data)
        conn.commit()
        conn.close()

    
    def deleteSongPlayerInDb(self,id_song_player):
        '''
            docstring in SongPlayerDAOInterface
        '''
        conn = self._getDbConnection()

        requete = '''DELETE FROM song_player WHERE id_player = ?'''
        conn.execute(requete,(id_song_player,))

        conn.commit()

     
    def findByID(self, id_song_player):
        '''
            docstring in SongPlayerDAOInterface
        '''
        conn = self._getDbConnection()
        # Use a parameterized query to prevent SQL injection
        res = conn.execute('SELECT * FROM song_player WHERE id_player = ?;', (id_song_player,)).fetchone()
        conn.close()

        if res:
            return SongPlayer(dict(res))
        return  []

  
    def findByState(self, state) :
        '''
            docstring in SongPlayerDAOInterface
        '''
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player WHERE state = ;', (state,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers :
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList:
            return songplayerList
        return []
    

    def findAllByOrganisationInBd(self, id_orga):
        '''
            docstring in SongPlayerDAOInterface
        '''
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
        '''
            docstring in SongPlayerDAOInterface
        '''
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player;').fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList :
            return songplayerList
        return []

    
    def UpdateState(self, state, id_song_player) :
        '''
            docstring in SongPlayerDAOInterface
        '''      
        conn = self._getDbConnection()
        conn.execute('UPDATE song_player SET state = ? WHERE id_player =  ?;', (state,id_song_player))
        conn.commit() 
        conn.close()
