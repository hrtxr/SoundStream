from flask import render_template, session, redirect, url_for, request
from app import app
from app.services.ServiceSongPlayer import SongPlayerService
from app.controllers.LoginController import LoggedIn, reqrole

sps = SongPlayerService()

class SongPlayerController :


    @app.route('/alldevices', methods =['GET'])
    @LoggedIn
    def alldevices ():

        metadata= {'title': 'All Devices'}

        all_devices = sps.allSongPlayer()

        return render_template('devices.html', metadata=metadata)


    @app.route('/alldevices/delete/<int:id_player>', methods=['POST'])
    @LoggedIn
    def delete(id_player):
        # Appel au service pour supprimer
        sps.deleteSongPlayer(id_player)
    
        # Redirection vers la fonction 'alldevices' qui affiche la liste
        return redirect(url_for('alldevices'))




    # ici c'est la route qui va
    '''
    @app.route('/get-player', methods=['POST'])
    @LoggedIn

    explication de se que je veux faire :
    Interroge un lecteur distant (SongPlayer) via son IP pour auto-découvrir ses informations.
    
    Cette méthode implémente la logique d'auto-détection pour éviter la saisie manuelle 
    par l'utilisateur. Elle fait le pont entre la saisie de l'IP dans le formulaire 
    et l'enregistrement complet en base de données.

    Logique attendue :
    -----------------
    1. Établir une connexion HTTP vers l'IP fournie (ex: http://<ip_address>/info).
    2. Récupérer le payload JSON contenant les métadonnées de la machine :
       - hostname (sera mappé sur name_place)
       - location (sera mappé sur place_adress)
       - current_status (sera mappé sur state)
    3. Gérer les cas d'erreur réseau (Timeout, ConnectionRefused) pour éviter de 
       bloquer le thread principal du contrôleur.
    4. Retourner un dictionnaire formaté pour être transformé en tuple par le 
       contrôleur ou None si la machine ne répond pas.

    vous inquiter pas le texte il générer par ia mais l'idée elle vien de moi 
    Signer saif
    '''
    




