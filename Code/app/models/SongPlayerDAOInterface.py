class SongPlayerDAOinterface :
    
    def createSongPlayer(self, name_place, IP_adress, state, last_synchronization, place_address , name_orga) :
        """ Create a new song player in the data base"""
        pass
    
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