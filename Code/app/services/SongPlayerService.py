from app.models.SongPlayerDAO import SongPlayerDAO
import subprocess
import threading

class SongPlayerService:
    
    def __init__(self) :
        self.spdao = SongPlayerDAO()
    
   
    def ping(self,ip: str) ->bool :
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
        

    def changeState(self, id_player):
        # Define the two possible states: "PLAYING" and "OFFLINE"
        state_playing = "ONLINE"
        state_offline = "OFFLINE"
    
        # Retrieve the song player associated with the given id from the database
        song_player = self.spdao.findByID(id_player)
        if song_player:
            # Get the Ip adress of the song player
            ip=song_player.IP_adress
    
            # Check if the IP is reachable (ping the IP)
            if self.ping(ip) == False:
                # If the IP is not reachable, update the player's state to "OFFLINE"
                self.spdao.UpdateState(state_offline, id_player)
            else:
                # If the IP is reachable, update the player's state to "PLAYING"
                self.spdao.UpdateState(state_playing, id_player)
        else :
            return


    def deleteSongPlayer(self,id_song_player):

        self.spdao.deleteSongPlayerInDb(id_song_player)

    def allSongPlayer(self):
        return  self.findAll()
 
    def findAllByOrganisationAndStatus(self, id_orga, status):
        return self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status))
    
    def CountAllByOrganisationAndStatus(self, id_orga, status):
        return len(self.spdao.findAllByOrganisationAndStatus(str(id_orga), str(status)))
                                            
    def findAllSongPlayerByOrganisation(self, id_orga):
        # Fetch initial list of players from the database
        players = self.spdao.findAllByOrganisationInBd(id_orga)

        # Update each player's status by pinging their IP address
        for p in players:
            self.changeState(p.id_player)
    
        # Return the refreshed list with updated statuses
        return self.spdao.findAllByOrganisationInBd(id_orga)
    
    def findAllOffline(self):
        return self.spdao.findAllOffline()

    #Je veux que on indique seulement l'ip du player puis que les info du player soit ajouter automatique dans la bd 
    #def addSongPlayer(self,form):
        