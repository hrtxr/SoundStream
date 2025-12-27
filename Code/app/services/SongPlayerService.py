from app.models.SongPlayerDAO import SongPlayerDAO
import subprocess
import threading

class SongPlayerService:
    
    def __init__(self) :
        self.spdao = SongPlayerDAO()
    
   
    def ping(self,ip):
        """
        Checks if a song player is reachable on the network.

            Args:
                ip (str): The IP address of the song player to ping.

            Returns:
                bool: True if the player responds, False otherwise.
        """
        try :
            command = ["ping","-c","1","-w","1",ip]

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0

        except subprocess.CalledProcessError:
            # If subprocess fails, return False
            return False
        except Exception:
            # In case of any other exception, return False
            return False
        

    def changeState(self, id_song_player):
        """
        Checks the network status of a player and updates its state in the database.

            Args:
                id_song_player (int): The unique ID of the song player to check.
        """
        # Define the two possible states: "ONLINE" and "OFFLINE"
        state_online = "ONLINE"
        state_offline = "OFFLINE"
    
        # Retrieve the song player associated with the given id from the database
        song_player = self.spdao.findByID(id_song_player)
        if song_player:
            # Get the Ip adress of the song player
            ip=song_player.IP_adress
    
            # Check if the IP is reachable (ping the IP)
            if self.ping(ip) == False:
                # If the IP is not reachable, update the player's state to "OFFLINE"
                self.spdao.UpdateState(state_offline, id_song_player)
            else:
                # If the IP is reachable, update the player's state to "ONLINE"
                self.spdao.UpdateState(state_online, id_song_player)
        else :
            return


    def deleteSongPlayer(self,id_song_player):
        """
        Deletes a song player from the system and the database.

            Args:
                id_song_player (int): The unique identifier of the player to be removed.
        """

        self.spdao.deleteSongPlayerInDb(id_song_player)


    def allSongPlayer(self):
        """
        Retrieves all song players available in the system.

            Returns:
                List[SongPlayer]: A list containing all song player instances.
        """
        return  self.findAll()
 
                                            
    def findAllSongPlayerByOrganisation(self, id_orga):
        """
        Retrieves and synchronizes the status of all players within an organization.

            Args:
                id_orga (int): The unique ID of the organization.

            Returns:
                list[dict]: A list of song players as dictionaries with refreshed network statuses.
        """
        # Fetch initial list of players to identify who needs to be checked
        players = self.spdao.findAllByOrganisationInBd(id_orga)

        # Update each player's status by pinging their IP address
        for player in players:
            self.changeState(player.id_player)

        # Retrieve the updated objects from the database after synchronization
        updated_players = self.spdao.findAllByOrganisationInBd(id_orga)

        # Convert objects to dictionaries for compatibility with Jinja2 templates
        player_list_dict = []
        for player in updated_players:
            player_list_dict.append(vars(player))
    
        return player_list_dict
    
    
    #def addSongPlayer(self,form):


    def countNumberOfSongPlayerOnlineAndOffline(self,id_orga) :
        """
        Counts the number of online and offline song players for a specific organization.

            Args:
                id_orga (int): The unique ID of the organization.

            Returns:
                tuple: A tuple containing (nb_on, nb_off).
        """
        # Initialize counters for online and offline states
        nb_on = 0
        nb_off = 0

        # Retrieve the list of players as dictionaries from the service
        liste_song_player = self.spdao.findAllByOrganisationInBd(id_orga)

        # Convert objects to dictionaries for compatibility with Jinja2 templates
        liste_song_player_dict = [vars(p) for p in liste_song_player]
        
        # Iterate through the list to count states
        for p in liste_song_player_dict:
            if p['state'] == 'ONLINE':
                nb_on += 1
            elif p['state'] == 'OFFLINE':
                nb_off += 1

        return (nb_on, nb_off)
        