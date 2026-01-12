from datetime import datetime, timedelta
from app.models.PlaylistDAO import PlaylistDAO

class TimeTableService:

    def __init__(self):
        self.dao = PlaylistDAO()

    def getCompleteProg(self, datehour, id_orga):
        """ Get programmation of the day :"""
        ##### PITIÉ A REVOIR JE SUIS PAS SUR QUE CA FONCTIONNE QUOI... #####
        daybdd = datehour.strftime("%A")
        rawlist = self.dao.get_raw_playlist(daybdd)

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
        return self.dao.findAll()
    
    def getPlaylistById(self, playlist_id):
        return self.dao.findById(playlist_id)
    
    def getPlaylistDetails(self, playlist_id):
        playlist = self.dao.findById(playlist_id)
        if not playlist:
            return None
        files = self.dao.getFilesInPlaylist(playlist_id)
        
        title_count = sum(1 for f in files if f['type'] == 'mp3')
        ads_count = sum(1 for f in files if f['type'] == 'ad')
        
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
        days = self.dao.getAllDays()
        days_data = []

        for day in days:
            day_name = day['day_'] 
            playlists = self.dao.getPlannedPlaylistsForDay(day_name)
            
            days_data.append({
                'day_name': day_name,
                'details': day,
                'playlists': playlists
            })
            
        return days_data
    
    def updateDaySchedule(self, day_name, playlist_id, start_time):
        self.dao.removeAllPlaylistsFromDay(day_name)
        if playlist_id is not None and start_time:
            self.dao.addPlaylistToDay(playlist_id, day_name, start_time)