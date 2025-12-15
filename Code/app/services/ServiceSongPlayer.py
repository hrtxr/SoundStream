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

    def findAllByOrganisationAndStatus(self, id_orga, status):
        return self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status))
    
    def CountAllByOrganisationAndStatus(self, id_orga, status):
        return len(self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status)))
                                            
    def findAllByOrganisation(self, id_orga):
        return self.spdao.findAllByOrganisation(id_orga)
    
    def findAllOffline(self):
        return self.spdao.findAllOffline()

        
        