from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.TimeTableService import TimetableService
from app.services.SongPlayerService import SongPlayerService
from app.services.OrganisationService import OrganisationService
from app.services.LogService import LogService


us=UserService()
tts=TimetableService()
sps=SongPlayerService()
ogs=OrganisationService()
los=LogService()


class DashboardController:
    
    @app.route('/dashboard/<nom_orga>', methods=['GET', 'POST'])
    @LoggedIn
    def dashboard(nom_orga):
        metadata= {'title': 'Dashboard'}

        print(sps.findAllByOrganisation(ogs.getIdByName(nom_orga)))
    
        return render_template('dashboard.html', metadata=metadata, orga=nom_orga, us=us, tts=tts, sps=sps, ogs=ogs, los=los)