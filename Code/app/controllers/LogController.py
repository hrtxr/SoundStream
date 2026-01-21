from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.OrganisationService import OrganisationService
from app.services.LogService import LogService

orga=OrganisationService()
log=LogService()


class LogController :

    @app.route('/logs/<nom_orga>', methods =['GET'])
    @LoggedIn
    @reqrole(['admin'])
    def logs(nom_orga):
        metadata = {'title' : 'log'}
        log_list = log.getLogsByOrganisation(orga.getIdByName(nom_orga))
        return render_template('logs.html', log_list = log_list, metadata = metadata, orga=nom_orga)

    @app.route('/tickets', methods =['GET'])
    @LoggedIn
    @reqrole(['admin'])
    def tickets():
        metadata = {'title' : 'Tickets'}
        nom_orga = session.get('organisation_name')
        ticket_list = log.getTicketLogs()
        return render_template('tickets.html', ticket_list = ticket_list, metadata = metadata, orga=nom_orga)

    @app.route('/messages_diffused/<nom_orga>', methods =['GET'])
    @LoggedIn
    @reqrole(['marketing'])
    def messages_diffused(nom_orga):
        metadata = {'title' : 'Messages Diffused'}
        message_list = log.getMessageDiffusedLogs()
        return render_template('messages_diffused.html', message_list = message_list, metadata = metadata, orga=nom_orga)