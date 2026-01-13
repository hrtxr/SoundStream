from datetime import datetime
import sqlite3
from app import app
from app.models.Playlist import Playlist
from app.models.PlaylistDAOInterface import PlaylistDAOInterface
import os

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
    
    def addFileToPlaylist(self, id_playlist: int, id_file: int) -> bool:
        """
        Links an existing file to a playlist in the database.
        It checks for duplicates before inserting into the 'composition' table.

        Args:
            id_file (int): The unique ID of the file to add.
            id_playlist (int): The unique ID of the target playlist.

        Returns:
            bool: True if the file was successfully added.
                  False if the file was already in the playlist or if an error occurred.
        """
        conn = self._getDbConnection()

        try:
            #  Check if the link already exists to prevent duplicates
            query_check = "SELECT * FROM composition WHERE id_playlist = ? AND id_file = ?;"
            exists = conn.execute(query_check, (id_playlist, id_file)).fetchone()

            if not exists:
                #  Create the link in the association table
                query = "INSERT INTO composition (id_playlist, id_file) VALUES (?, ?);"
                conn.execute(query, (id_playlist, id_file))
                conn.commit()
                return True
            
            # The file is already in the playlist
            return False

        except Exception as e:
            print(f"Error linking file to playlist: {e}")
            return False    
        finally:
            # Always close the connection to avoid memory leaks
            conn.close()  
    
    
    def removeFileFromPlaylist(self, playlist_id: int, file_id: int) -> bool:
        """
        Removes a file from a playlist (deletes the link) and updates the modification date.

        Args:
            playlist_id (int): The ID of the playlist.
            file_id (int): The ID of the file to remove.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        conn = self._getDbConnection()
        
        try:
            # 1. Remove the link in the join table
            query_remove ="DELETE FROM composition WHERE id_playlist = ? AND id_file = ?"
            conn.execute(query_remove, (playlist_id, file_id))
            
            # 2. Update the playlist timestamp
            query_update ="UPDATE playlist SET last_update_date = ? WHERE id_playlist = ?"
            conn.execute(query_update, (datetime.now(), playlist_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error removing file from playlist: {e}")
            conn.rollback() # Cancel changes if an error occurs
            return False
            
        finally:
            # CRITICAL: Always close the connection, even if it crashes
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