from app.models.SongPlayerDAO import SongPlayerDAO
import os

class SongPlayerService:
    
    def __init__(self) :
        self.spdao = SongPlayerDAO()
    
    """
    WoRK IN PROGRESS mais en gros c'est la methode qui fait le ping 
    def ping(self,ip) :
        return os.system(f"ping -c 1 -W 1 {ip}") == 
    
    ICI c la methode qui va utiliser spdao.UpdateState pour modifier dans la BD
    def changeState(self,ip) :
        
        soung_player = self.spdao.findByIpAdress(ip)
    """
        
    
    def findAllByOrganisation(self, id_orga):
        return self.spdao.findAllByOrganisation(str(id_orga))

        
        