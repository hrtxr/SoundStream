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
    
    def addSongPlayerInDb(self, data_form_to_form):
        '''
            data = tuples (name_place, ip_address, state, last_synchronization, place_address, id_orga)

        '''
        conn = self._getDbConnection()
        try:
            query = '''
            INSERT INTO song_player
            (name_place, ip_address, state, last_synchronization, place_address, id_orga)
            VALUES (?, ?, ?, ?, ?, ?);
            '''
            conn.execute(query, data_form_to_form)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def updateDbSongPlayer(self, form_data, id_player):

        # Get a database connection
        conn = self._getDbConnection()
        
        #Get all key from the form
        updated_columns=list(form_data.keys())

        # Get all values from the form
        values = list(form_data.values())

        # Create the SQL update query
        # Each column uses "column = ?" to protect against SQL injection
        set_clause = ', '.join([f'{col} = ?' for col in updated_columns])
        requete = f"UPDATE song_player SET {set_clause} WHERE id_player = ?"
        # Execute the query with parameters
        # Using "?" protects the query from SQL injection
        conn.execute(requete, tuple(values) + (id_player,))

        # Save changes to the database
        conn.commit()

        
    def deleteSongPlayerInDb(self,id_song_player):
        conn = self._getDbConnection()

        requete = '''DELETE FROM song_player WHERE id_player = ?'''
        conn.execute(requete,(id_song_player,))

        conn.commit()

        
    def findByID(self, id_player):
        conn = self._getDbConnection()
        # Use a parameterized query to prevent SQL injection
        res = conn.execute('SELECT * FROM song_player WHERE id_player = ?;', (id_player,)).fetchone()
        conn.close()

        if res:
            return SongPlayer(dict(res))
        return  []
    
    def findByOrganisation(self, name_orga) :
        conn = self._getDbConnection()
        songplayers = conn.execute('SELECT * FROM song_player JOIN organisation USING(id_orga) WHERE name_orga = ?;', (name_orga,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList:
            return songplayerList
        return []
    
    def findByState(self, state) :
        """ Get song player by state """
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
        conn = self._getDbConnection()
        songplayers = conn.execute("""SELECT * FROM song_player WHERE id_orga = ?;""", (id_orga,)).fetchall()
        songplayerList = list()
        for songplayer in songplayers : 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList :
            return songplayerList
        return []

    def findAllByOrganisationAndStatus(self, id_orga, status):
        conn = self._getDbConnection()

        sql = "SELECT * FROM song_player WHERE id_orga = ? AND state = ?;"

        songplayers = conn.execute(sql, (id_orga, status)).fetchall()

        songplayerList = list()
        for songplayer in songplayers: 
            songplayerList.append(SongPlayer(dict(songplayer)))
        conn.close()

        if songplayerList:
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
        return []
    
    def UpdateState(self, state, id_player) :
        '''
            Update the state of a song player.
            This method is different from updateSongPlayer.
            The state is not chosen by the user.
            It is set by the system.
        '''        
        conn = self._getDbConnection()
        conn.execute('UPDATE song_player SET state = ? WHERE id_player =  ?;', (state,id_player))
        conn.commit() 
        conn.close()
