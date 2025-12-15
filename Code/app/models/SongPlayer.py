class SongPlayer : 
    def __init__(self, dico) :
        self.id_player = dico['id_player']
        self.name_place = dico['name_place']
        self.IP_adress = dico['IP_adress']
        self.state = dico['state']
        self.last_synchronization = dico['last_synchronization']
        self.place_adress = dico['place_adress']
        self.name_orga = dico['id_orga']