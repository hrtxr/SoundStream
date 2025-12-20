class SongPlayerDAOInterface :
    
    def addSongPlayerInDb(self, name_place, IP_adress, state, last_synchronization, place_address , name_orga) :
        """ add a new song player in the data base"""
        pass
    
    def updateDbSongPlayer(self,form_datat):
        """Update the song player data (name_place place_adress ect)"""
    
    def deleteSongPlayerInDb(self,id_song_player) :
        """Deletes the song player from the data base"""
    
    def findByIpAdress(self, ip) :
        """ Get song player by IP adress """
        pass
    
    def findByOrganisation(self, name_orga) :
        """ Get song player by name of organisation """
        pass
    
    def findByState(self, state) :
        """ Get song player by state """
        pass

    def findAll(self) :
        """ Get all song players """
        pass
    
    def UpdateState(self, state, id_player) :
        """ Update the state of a song player """
        pass