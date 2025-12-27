class SongPlayerDAOInterface :
    
    def addSongPlayerInDb(self, name_place, IP_adress, state, last_synchronization, place_address , name_orga) :
        """
        Adds a new song player to the database.

            Args:
                name_place (str): The name of the location
                IP_address (str): The IP address of the player (e.g., '192.168.1.1')
                state (str): The current state ('ONLINE' or 'OFFLINE')
                last_synchronization (str | None): Timestamp of the last sync or None
                place_address (str): The physical address of the place
                name_orga (str): The name of the organization
            Returns:
                None
        """
        pass

    
    def deleteSongPlayerInDb(self,id_song_player):
        """
        Delete a song player to the database 

            Args:
                id_song_player(int): The ID of the song player to be deleted
            Returns:
                None
        """


    def findByID(self, id_song_player):
        """ 
        Get song player by the id of the song player

            Args:
                id_player(int): The ID of the song player to fetch
            Returns:
                SongPlayer: An instance of the SongPlayer object
        """
        pass


    def findAllByOrganisationInBd(self, id_orga):
        """
        Get all song players belonging to the same organization.

            Args:
                id_orga(int): The organization ID
            Returns:
                List[SongPlayer] : A list of SongPlayer instances
        """
        pass


    def findByState(self, state) :
        """
        Get all song players with a specific state.

            Args:
                state (str): The state to filter by ( 'ONLINE' or 'OFFLINE').
            Returns:
                List[SongPlayer]: A list of SongPlayer instances.
        """
        pass


    def findAll(self) :
        """
        Get all song players from the database.

            Returns:
                List[SongPlayer]: A list of all SongPlayer instances found in the database.
        """
        pass

    
    def UpdateState(self, state, id_song_player) :
        """
        Update the state of a specific song player.

            Args:
                state (str): The new state to set (e.g., 'ONLINE', 'OFFLINE').
                id_song_player (int): The unique ID of the song player to update.
        """
        pass