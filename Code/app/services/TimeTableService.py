from datetime import datetime, timedelta
from app import app
from app.models.PlaylistDAO import PlaylistDAO
from app.models.FileDAO import FileDAO
import os

class TimeTableService:

    def __init__(self):
        self.pdao = PlaylistDAO()
        self.fdao = FileDAO() # car comme on doit accéder a la table file on utilise le FileDAO

    def getCompleteProg(self, datehour, id_orga):
        """ Get programmation of the day :"""
        ##### PITIÉ A REVOIR JE SUIS PAS SUR QUE CA FONCTIONNE QUOI... #####
        daybdd = datehour.strftime("%A")
        rawlist = self.pdao.get_raw_playlist(daybdd)

        cursor_time = datehour.replace(hour=8, minute=0, second=0, microsecond=0)
        playlist_finale = []

        for nom, strlength, path in rawlist:
            h, m, s = map(int, strlength.split(':'))
            length = timedelta(hours=h, minutes=m, seconds=s)
            
            endhour = cursor_time + length

            if endhour > datehour:
                if cursor_time <= datehour < endhour:
                    status = "playing"
                else:
                    status = "future"
                
                is_promo = ("PROMO" in nom) or ("ads" in path)

                playlist_finale.append({
                    "hour": cursor_time.strftime("%d/%m/%Y - %H:%M"),
                    "titre": nom,
                    "status": status,
                    "is_promo": is_promo
                })

            cursor_time = endhour

        return playlist_finale
    
    ####################
    ## EDIT PLAYLISTS ##
    ####################
    
    def getAllPlaylists(self):
        return self.pdao.findAll()
    
    def getPlaylistById(self, playlist_id):
        return self.pdao.findById(playlist_id)
    
    def addFileInPlaylist(self,playlist_id,id_file) -> bool: 
        return self.pdao.addFileToPlaylist(playlist_id,id_file)
    
    def deleteFileFromPlaylist(self,playlist_id,id_file) -> bool :
        return self.pdao.removeFileFromPlaylist(playlist_id,id_file)
    
    def getPlaylistDetails(self, playlist_id):
        playlist = self.pdao.findById(playlist_id)
        if not playlist:
            return None
        files = self.fdao.getFilesInPlaylist(playlist_id)
        
        title_count = sum(1 for f in files if f.type_file.lower() == 'mp3')
        ads_count = sum(1 for f in files if f.type_file.lower() == 'ad')
        
        return {
            'playlist': playlist,
            'files': files,
            'title_count': title_count,
            'ads_count': ads_count
        }

    ############################
    ## EDIT PLAYLIST FOR DAYS ##
    ############################

    def getAllDaysWithPlaylists(self):
        days = self.pdao.getAllDays()
        days_data = []

        for day in days:
            day_name = day['day_'] 
            playlists = self.pdao.getPlannedPlaylistsForDay(day_name)
            
            days_data.append({
                'day_name': day_name,
                'details': day,
                'playlists': playlists
            })
            
        return days_data
    
    def updateDaySchedule(self, day_name, playlist_id, start_time):
        self.pdao.removeAllPlaylistsFromDay(day_name)
        if playlist_id is not None and start_time:
            self.pdao.addPlaylistToDay(playlist_id, day_name, start_time)

    def getPlaylistNameById(self, playlist_id):
        playlist =self.pdao.findById(playlist_id)
        if playlist:
            return playlist.name
        return None

    def generateM3uContent(self, playlist_id: int) -> str:
        ''' Generate M3U content with all the references of the files contained in the playlist'''

        # we get all the details in the playlist
        details = self.getPlaylistDetails(playlist_id)

        files = details['files']

        m3u_lines = ['#EXTM3U']

        for file in files : 
            #parsage du format MM:SS en secondes pures
            time_in_seconds = 0
            split_time = file.time_length.split(':')
            time_in_seconds = int(split_time[0])*60 + int(split_time[1])

            #add the lines of each file to the m3u file
            m3u_lines.append(f"#EXTINF:{time_in_seconds},{file.name}")

            filename_only = os.path.basename(file.path)
            m3u_lines.append(filename_only)
            
        
        #join all the lines to create the string 
        # which represents the conntent of the m3u file 
        # and return it 
        m3u_content= "\n".join(m3u_lines)
        return m3u_content
    

    def updateM3uFile(self, playlist_id : int) -> bool :
        '''Generate the m3u file and crush the existant file when it's an update'''
        content = self.generateM3uContent(playlist_id)
        playlist = self.getPlaylistById(playlist_id)
        playlist_name = playlist.name
        if content == None :
            return False

        folder = os.path.join(app.static_folder, 'playlists')

        file_path = os.path.join(folder, f"playlist_{playlist_name}.m3u")

        with open(file_path, 'w', encoding='utf-8') as f :
            f.write(content)

        return True
    
    def autoCleanPlaylist(self):
        return self.pdao.removePlaylistObsolete()