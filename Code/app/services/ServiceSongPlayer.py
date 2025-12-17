from app.models.SongPlayerDAO import SongPlayerDAO
import subprocess

class SongPlayerService:
    
    def __init__(self) :
        self.spdao = SongPlayerDAO()
    
   
    def ping(ip: str) ->bool :
        # ici le try except est obliger 
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
        

    def changeState(self, ip):
        # Define the two possible states: "PLAYING" and "OFFLINE"
        state_playing = "PLAYING"
        state_offline = "OFFLINE"
    
        # Retrieve the song player associated with the given IP address from the database
        song_player = self.spdao.findByIpAdress(ip)
    
        # Get the ID of the song player
        id_song_player = song_player.id_player 
    
        # Check if the IP is reachable (ping the IP)
        if self.ping(ip) == False:
            # If the IP is not reachable, update the player's state to "OFFLINE"
            song_player.UpdateState(state_offline, id_song_player)
        else:
            # If the IP is reachable, update the player's state to "PLAYING"
            song_player.UpdateState(state_playing, id_song_player)

    def updateSongPlayer(self, form_data):
        """
        Service to update a song player in the database.
        Only updates fields with values.
        The player id is never modified.
        """

        # Get the player id from the form
        song_player_id = form_data['id_player']

        # Create empty lists for columns and values to update
        updated_columns = list()
        values = list()

        # Loop through all items in the form data
        for key, value in form_data.items():

            # Skip the player id because we do not want to modify it
            if key == 'id_player':
                continue

            # Only include fields that have a value
            if value:
                # Add the column with placeholder to protect against SQL injection
                updated_columns.append(f"{key} = ?")
                # Add the corresponding value
                values.append(value)

        # If there is nothing to update, exit the function
        if not updated_columns:
            return

        # Create a dictionary from columns and values
        # Keys are like "column = ?", values are the actual data
        updated_form = dict(zip(updated_columns, values))

        # Call the DAO update method to modify the song player in the database
        # Using placeholders "?" ensures protection against SQL injection
        self.spdao.update(updated_form, song_player_id)

    
    def findAllByOrganisationAndStatus(self, id_orga, status):
        return self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status))
    
    def CountAllByOrganisationAndStatus(self, id_orga, status):
        return len(self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status)))
                                            
    def findAllByOrganisation(self, id_orga):
        return self.spdao.findAllByOrganisation(id_orga)
    
    def findAllOffline(self):
        return self.spdao.findAllOffline()