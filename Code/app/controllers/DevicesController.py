from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.SongPlayerService import SongPlayerService
from app.services.OrganisationService import OrganisationService

sps=SongPlayerService()
ogs=OrganisationService()

class DevicesController :

    @app.route('/devices/<nom_orga>', methods =['GET'])
    @LoggedIn
    def devices(nom_orga):
        metadata= {'title': 'Devices'}

        return render_template('devices.html', metadata=metadata, sps=sps, ogs=ogs, orga=nom_orga)

    