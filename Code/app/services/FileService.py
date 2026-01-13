from app import app
from app.models.FileDAO import FileDAO
from werkzeug.utils import secure_filename #Pour la securiter important de zinzin
from werkzeug.datastructures import FileStorage #sa c juste un truc pour voir 
from typing import *
import os

class FileService :

    def __init__(self):

        self.fdao = FileDAO()
        #self.upload_folder = 

    def create_file_from_form(self, form_data: dict, file_storage: FileStorage) -> int:
        """
        Prend les données brutes du formulaire (dico) et le fichier,
        gère la sauvegarde physique, et remplit la méthode createFile du DAO.

        Args:
            form_data (dict): request.form (contient 'file_type', etc.)
            file_storage (FileStorage): request.files['uploadfile']

        Returns:
            int: L'ID du fichier créé, ou -1 en cas d'erreur.
        """
