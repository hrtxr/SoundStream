from app.models.UserDAO import UserDAO

class UserService():

    def __init__(self):
		# cette ligne utilise le Data Access Object (DAO) dédié aux fichier JSON
        self.udao = UserDAO()
    
    def findUserOrganisation(self, username):
        """ Get the organisation of a user by username and return the list of organisations """
        return  self.udao.findUserOrganisation(username)