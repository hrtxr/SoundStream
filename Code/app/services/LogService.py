from app.models.LogDAO import LogSqliteDAO as LogDAO
from typing import *

class LogService:
    ''' This class will manipulate the log to give 
    what the LogController wants.'''

    def __init__(self):
        self.ldao = LogDAO()

    def getLogs(self) -> dict:
        logs = self.ldao.findAll()
        list_logs = list()

        for log in logs:
            list_logs.append(log.toDict())

        return list_logs
    
    def getLogsByOrganisation(self, id_orga: int) -> list[dict]:
        logs = self.ldao.findAllByOrganization(id_orga)
        list_logs = list()
        for log in logs :
            list_logs.append(log.toDict())

        return list_logs
    
    def getTicketLogs(self) -> list[dict]:
        tickets = self.ldao.findAllTickets()  # New method to get ticket logs
        list_tickets = list()
        for ticket in tickets :
            list_tickets.append(ticket.toDict())

        return list_tickets