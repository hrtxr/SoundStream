class Playlist : 
    def __init__(self, dico) :
        self.id_playlist = dico['id_playlist']
        self.name = dico['name']
        self.creation_date = dico['creation_date']
        self.expiration_date = dico['expiration_date']
        self.last_update_date = dico['last_update_date']