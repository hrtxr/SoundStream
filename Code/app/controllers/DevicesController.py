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
        #c'est en fr pour l'instant pour expliquer mes choix
        metadata= {'title': 'Devices'}
        # On récupère l'ID de l'organisation une seule fois pour optimiser
        orga = ogs.getIdByName(nom_orga)
    
        # On initialise nos compteurs et notre liste
        nb_on = 0
        nb_off = 0
        liste_song_player_dict = []

        # On récupère les objets depuis le service
        liste_song_player_object = sps.findAllSongPlayerByOrganisation(orga)
    
        # On centralise la logique ici : on transforme en dict ET on compte les états
        # en un seul passage (boucle unique) pour de meilleures performances.
        for p in liste_song_player_object:
            # Transformation en dictionnaire pour faciliter l'accès dans la template Jinja
            liste_song_player_dict.append(vars(p))

            # Calcul des compteurs en Python plutôt qu'en SQL ou dans la template
            # Cela garantit que les chiffres affichés correspondent exactement à la liste
            if p.state == 'ONLINE':
                nb_on += 1
            elif p.state == 'OFFLINE':
                nb_off += 1
        return render_template('devices.html', metadata=metadata, liste_song_player=liste_song_player_dict, nb_on=nb_on, nb_off=nb_off)
        

    @app.route('/update/<int:id_player>', methods=['POST','GET'])
    @LoggedIn
    def update(id_player):
    
        # Run the ping test and save the new status (PLAYING/OFFLINE) in the database
        sps.changeState(id_player)

        # Redirect the user back to the previous page to see the updated status
        return redirect(request.referrer)


    @app.route('/delete/<int:id_player>',methods=['POST','GET'])
    @LoggedIn
    def delete(id_player):
        # Permanently remove the player from the database using the service layer
        sps.deleteSongPlayer(id_player)

        # Stay on the current page to confirm the player is gone from the list
        return redirect(request.referrer)



# ici y manque juste la logique pour ajouter un device est cette page seras fini  
