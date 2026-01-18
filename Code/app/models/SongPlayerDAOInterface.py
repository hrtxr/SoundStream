class SongPlayerDAOInterface :

    def createDevice(self, name_place, ip_address, place_address, place_city, place_postcode, place_building_name, orga_id):
        """
        Create a new song player in the database.

            Args:
                name_place (str): The name of the place
                ip_address (str): The IP address of the song player
                place_city (str): The city of the place
                place_postcode (str): The postcode of the place
                place_building_name (str): The building name of the place
                orga_id (int): The ID of the organization
            Returns:
                None
        """
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

    def findAllBuildingNames(self):
        """
        Get all distinct building names from the song players.

            Returns:
                List[str]: A list of distinct building names.
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