import sqlite3
from app import app
from app.models.Playlist import Playlist
from app.models.PlaylistDAOInterface import PlaylistDAOInterface

class PlaylistDAO(PlaylistDAOInterface):

    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def getTracksForDay(self, day_name):
        """ Get : Title, Lenght (in seconds)
        Order by : track position in playlist """
        conn = self._getDbConnection()
        query = """
            SELECT f.name, f.time_length, f.path
            FROM file f
            JOIN composition c ON f.id_file = c.id_file
            JOIN playlist p ON c.id_playlist = p.id_playlist
            JOIN planned pl ON p.id_playlist = pl.id_playlist
            WHERE pl.day_ = ?
        """
        return conn.execute(query, (day_name,)).fetchall()
    
    def findAll(self):
        conn = self._getDbConnection()
        playlists = conn.execute('SELECT * FROM playlist;').fetchall()
        playlistList = list()
        for playlist in playlists : 
            playlistList.append(Playlist(dict(playlist)))
        conn.close()

        if playlistList :
            return playlistList
        return None