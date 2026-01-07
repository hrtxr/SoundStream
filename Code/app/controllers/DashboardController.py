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
        session['organisation_name'] = nom_orga

        print(sps.findAllSongPlayerByOrganisation(ogs.getIdByName(nom_orga)))

        # Get organization ID once to optimize database queries
        id_orga = ogs.getIdByName(nom_orga)

        # Get all players for this organization as a list of dictionaries
        liste_song_player_dict = sps.findAllSongPlayerByOrganisation(id_orga)

        # Retrieve the count of online and offline players for this organization
        nb_on_and_nb_off = sps.countNumberOfSongPlayerOnlineAndOffline(id_orga)
        
        # Unpack counters from the result list/tuple
        nb_on = nb_on_and_nb_off[0]
        nb_off = nb_on_and_nb_off[1]


        # Render the dashboard with all collected metrics and player data
        return render_template('dashboard.html', 
                                metadata=metadata, 
                                orga=nom_orga, 
                                us=us, 
                                tts=tts, 
                                sps=sps, 
                                ogs=ogs, 
                                los=los,
                                nb_on=nb_on,
                                nb_off=nb_off, 
                                liste_song_player=liste_song_player_dict)