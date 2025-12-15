from datetime import datetime, timedelta
from app.models.PlaylistDAO import PlaylistDAO

class TimetableService:

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