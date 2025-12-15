from app.models.LogDAO import LogDAO

class LogService:

    def __init__(self):
        self.dao = LogDAO()

    def getLogsByOrganisation(self, id_orga):
        return self.dao.findAllByOrganisation(id_orga)