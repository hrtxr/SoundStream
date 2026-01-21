from app.models.SongPlayerDAO import SongPlayerDAO
from app.services.TimeTableService import TimeTableService 
import subprocess
import time
import threading
import datetime
import platform
import os
from app import app

ts = TimeTableService()

class SongPlayerService:

    _current_playlist = None
    
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
            if platform.system() == 'Windows':
                command = ["ping", "-n", "1", "-w", "1000", ip] # Ping command for Windows with 1 echo request and 1 second timeout (in milliseconds)
                # Or use : command = ["Test-NetConnection","-ComputerName", ip] #Windows specific ping command (Default timeout is 1 second & 1 echo)

                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return result.returncode == 0

            else:  # For Unix/Linux/Mac
                command = ["ping","-c","1","-w","1",ip] # Ping command for Linux with 1 echo request and 1 second timeout (in seconds)

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
        

    def run_sync(self, ip, username):
            # Configuration des dossiers
            # On définit des couples (Source_Locale, Dossier_Destination_Distant)
            sync_tasks = [
                (os.path.join(app.static_folder, 'audio/'), "music/"),
                (os.path.join(app.static_folder, 'playlists/'), "playlists/")
            ]
            
            base_dest_path = f"/home/{username}/SoundStreamDevice/"

            for src, subfolder in sync_tasks:
                full_remote_path = os.path.join(base_dest_path, subfolder)
                
                # 1. Créer le sous-dossier spécifique sur la Debian
                subprocess.run(["ssh", f"{username}@{ip}", f"mkdir -p {full_remote_path}"])

                # 2. Synchroniser vers ce sous-dossier précis
                dest = f"{username}@{ip}:{full_remote_path}"
                cmd = [
                    "rsync", "-avz", "--delete",
                    "-e", "ssh",
                    src, dest
                ]
                
                try:
                    subprocess.run(cmd, check=True)
                except Exception as e:
                    print(f"Erreur synchro {subfolder} vers {ip} : {e}")
                    
    def sync_to_device(self, ip, username):
        """ Envoie les fichiers vers la vm Debian distante dans des dossiers séparés """

        threading.Thread(target=self.run_sync(ip, username)).start()


    def remote_play_playlist(self, ip, username, playlist_name):
        """ 
        Commande le MPD distant pour charger et lire une playlist précise 
        """
        # 1. On nettoie MPD
        # 2. On charge la nouvelle playlist (le fichier .m3u doit être dans le dossier playlist de MPD)
        # 3. On lance la lecture
        remote_cmd = f"mpc clear && mpc load {playlist_name} && mpc play"
        
        ssh_cmd = ["ssh", f"{username}@{ip}", remote_cmd]
        
        try:
            subprocess.run(ssh_cmd, check=True)
            print(f"▶️ Lecture de {playlist_name} lancée sur {ip}")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'ordre de lecture : {e}")

    def run_check(self):
        print("🚀 Scheduler démarré...")
        while True:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.strftime("%A")
            
            # Récupération de la playlist prévue (ex: "playlist_MaListe")
            scheduled_playlist = ts.getPlaylistForTime(current_day, current_time)
            
            # CONDITION CRUCIALE : 
            # On ne lance la musique QUE SI :
            # 1. Une playlist est prévue (scheduled_playlist n'est pas None)
            # 2. ET ce n'est pas celle qui tourne déjà
            if scheduled_playlist and scheduled_playlist != SongPlayerService._current_playlist:
                
                devices = self.spdao.findAllOnlineDevices()
                if devices:
                    print(f"🎵 Changement de playlist : {scheduled_playlist}")
                    for dev in devices:
                        self.remote_play_playlist(dev.IP_adress, 'tristan', scheduled_playlist)
                    
                    # On met à jour la mémoire pour ne pas relancer au prochain tour
                    SongPlayerService._current_playlist = scheduled_playlist
            
            # Si aucune playlist n'est prévue dans le planning (trou dans l'emploi du temps)
            elif not scheduled_playlist and SongPlayerService._current_playlist is not None:
                print("🛑 Fin de plage horaire : arrêt de la musique.")
                # Optionnel : envoyer un 'mpc stop' via SSH ici
                SongPlayerService._current_playlist = None

            time.sleep(30)

    def start_background_scheduler(self):

        threading.Thread(target=self.run_check, daemon=True).start()


####################################
## Calendar view & Timetable view ##
####################################

def trackStartingAt(self, day_name: str, hour: int, minute: int) -> list:
    """"""