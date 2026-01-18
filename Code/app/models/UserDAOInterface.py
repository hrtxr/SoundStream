class UserDAOInterface :
    def createUser(self, username, password, role) :
        pass

    def createLinkUserOrganisation(self, username, organisation):
        pass

    def findByUsername(self, username):
        pass

    def findUsersInOrganisation(self, organisation):
        pass
    
    def verifyUser(self, username, password) :
        pass

    def changePassword(self, username, password) :
        pass
    
    def deleteByUsername(self, username):
        pass

    def updateUserRole(self, username, new_role):
        pass

    def getOrganisationByUsername(self, username):
        pass
    
    def getAllRoles(self):
        pass

    def findAll(self) :
        pass
