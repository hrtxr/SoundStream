from app import app
from typing import *
from datetime import datetime
import sqlite3
from app.models.FileDAOInterface import FileDAOInterface
from app.models.File import File


class FileDAO(FileDAOInterface) :

    def __init__(self):
        self.databasename = app.static_folder + '/database/database.db'

    def _getDbConnection(self):
        """ Connect to the database. Returns the connection object """
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def findFileById(self,id_file :int) -> Optional[File]:
        """Return a file from the database using its unique identifier."""
        conn = self._getDbConnection()
        query = "SELECT * FROM file WHERE id_file = ?"

        file=conn.execute(query,(id_file,)).fetchone()

        conn.close()
        if file :
            return File(dict(file))
        else :
            return None
        

