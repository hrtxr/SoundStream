from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.OrganisationService import OrganisationService
from app.services.LogService import LogService

ogs=OrganisationService()
los=LogService()


class LogController :

    @app.route('/logs/<nom_orga>', methods =['GET'])
    @LoggedIn
    @reqrole(['admin'])
    def logs(nom_orga):
        metadata= {'title': 'Logs'}

        return render_template('logs.html', metadata=metadata, ogs=ogs, los=los, orga=nom_orga)

    