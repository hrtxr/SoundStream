from datetime import datetime
import sqlite3
from app import app
from app.models.Playlist import Playlist
from app.models.PlaylistDAOInterface import PlaylistDAOInterface

class PlaylistDAO(PlaylistDAOInterface):

    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def getTracksForDay(self, day_name):
        """ JE PENSE QUE CA SERT A RIEN CA NON PLUS A REVOIR PLUS TARD """
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

    def findById(self, playlist_id):
        conn = self._getDbConnection()
        playlist = conn.execute(
            'SELECT * FROM playlist WHERE id_playlist = ?',
            (playlist_id,)
        ).fetchone()
        conn.close()
        
        if playlist:
            return Playlist(dict(playlist))
        return None
    
    ####################
    ## EDIT PLAYLISTS ##
    ####################

    def getFilesInPlaylist(self, playlist_id):
        conn = self._getDbConnection()
        files = conn.execute('''
            SELECT f.*
            FROM file f
            JOIN composition c ON f.id_file = c.id_file
            WHERE c.id_playlist = ?
            ORDER BY f.name
        ''', (playlist_id,)).fetchall()
        conn.close()
        return files
    
    def addFileToPlaylist(self, playlist_id, filename, file_type='mp3', lengt='00:03:00'):
        conn = self._getDbConnection()
        
        file = conn.execute(
            'SELECT id_file FROM file WHERE name = ?',
            (filename,)
        ).fetchone()
        
        if file:
            file_id = file['id_file']
        else:
            cursor = conn.execute('''
                INSERT INTO file (name, path, time_length, upload_date, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, f'/mnt/data/music/{filename}', lengt, datetime.now(), file_type))
            file_id = cursor.lastrowid
        
        exists = conn.execute('''
            SELECT * FROM composition 
            WHERE id_playlist = ? AND id_file = ?
        ''', (playlist_id, file_id)).fetchone()
        
        if not exists:
            conn.execute('''
                INSERT INTO composition (id_playlist, id_file)
                VALUES (?, ?)
            ''', (playlist_id, file_id))
            
            conn.commit()
        
        conn.close()
        print(file_id)
        return file_id
    
    def removeFileFromPlaylist(self, playlist_id, file_id):
        conn = self._getDbConnection()
        conn.execute('''
            DELETE FROM composition 
            WHERE id_playlist = ? AND id_file = ?
        ''', (playlist_id, file_id))
        
        conn.execute('''
            UPDATE playlist 
            SET last_update_date = ? 
            WHERE id_playlist = ?
        ''', (datetime.now(), playlist_id))
        
        conn.commit()
        conn.close()

    ############################
    ## EDIT PLAYLIST FOR DAYS ##
    ############################

    def getAllDays(self):
        conn = self._getDbConnection()
        days = conn.execute('SELECT * FROM Planning ORDER BY day_').fetchall()
        conn.close()
        return days
    
    def getPlannedPlaylistsForDay(self, day_name):
        conn = self._getDbConnection()
        playlists = conn.execute('''
            SELECT p.*, pl.start_time
            FROM playlist p
            JOIN planned pl ON p.id_playlist = pl.id_playlist
            WHERE pl.day_ = ?
            ORDER BY pl.start_time
        ''', (day_name,)).fetchall()
        conn.close()
        return playlists
    
    def addPlaylistToDay(self, playlist_id, day_name, start_time):
        conn = self._getDbConnection()
        
        exists = conn.execute('''
            SELECT * FROM planned 
            WHERE id_playlist = ? AND day_ = ?
        ''', (playlist_id, day_name)).fetchone()
        
        if exists:
            conn.execute('''
                UPDATE planned 
                SET start_time = ? 
                WHERE id_playlist = ? AND day_ = ?
            ''', (start_time, playlist_id, day_name))
        else:
            conn.execute('''
                INSERT INTO planned (id_playlist, day_, start_time)
                VALUES (?, ?, ?)
            ''', (playlist_id, day_name, start_time))
        
        conn.commit()
        conn.close()

    def removeAllPlaylistsFromDay(self, day_name):
        conn = self._getDbConnection()
        conn.execute('DELETE FROM planned WHERE day_ = ?', (day_name,))
        conn.commit()
        conn.close()