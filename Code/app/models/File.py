class File :
    def __init__(self,dico):
        self.id_file = dico['id_file']
        self.name = dico['name']
        self.path = dico['path']
        self.time_length = dico['time_length']
        self.upload_date = dico['upload_date']
        self.type_file = dico['type_file']