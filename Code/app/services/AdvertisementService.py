import datetime
from typing import List, Dict

from app.models.AdvertisementDAO import AdvertisementDAO

class AdvertisementService:
    def __init__(self):
        self.adao = AdvertisementDAO()

    def scheduleAdvertisement(self, id_file: int, id_orga: int, play_date: str, play_time: str) -> int:
        """
        Schedules an advertisement to be played at a specific date and time.
        Args:
            id_file (int): The ID of the audio file in the database.
            id_orga (int): The ID of the organisation.
            play_date (str): The date in YYYY-MM-DD format.
            play_time (str): The time in HH:MM format.
        Returns:
            int: The ID of the new advertisement record.
        """
        # Ensure time is zero-padded properly HH:MM
        if len(play_time.split(':')) == 2:
            h, m = play_time.split(':')
            play_time = f"{h.zfill(2)}:{m.zfill(2)}"
            
        return self.adao.createAdvertisement(id_file, id_orga, play_date, play_time)

    def getAndMarkPendingAdvertisements(self) -> List[Dict]:
        """
        Gets all pending advertisements that should be played now,
        and marks them as played to prevent double playback.
        Returns:
            List[Dict]: List of advertisement dictionaries containing file details.
        """
        now = datetime.datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M')

        pending_ads = self.adao.getPendingAdvertisements(current_date, current_time)
        
        # Mark them as played immediately so another loop tick doesn't pick them up
        for ad in pending_ads:
            self.adao.markAsPlayed(ad['id_ad'])
            
        return pending_ads
