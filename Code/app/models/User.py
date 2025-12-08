class User : 
    def __init__(self, dico) :
        self.id_user = dico['id_user']
        self.username = dico['username']
        self.password = dico['password']
        self.role = dico['role']
