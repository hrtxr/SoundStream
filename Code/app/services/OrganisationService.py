from app.models.OrganisationDAO import OrganisationDAO
import os

class OrganisationService:

    def __init__(self) :
        self.odao = OrganisationDAO()

    def getIdByName(self, orga_name):
        return self.odao.getIdByName(orga_name)
