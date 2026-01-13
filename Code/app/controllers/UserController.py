from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.OrganisationService import OrganisationService
from app.services.LogService import LogService
import datetime

log = LogService()
ogs=OrganisationService()
us=UserService()


class UserController :

    @app.route('/users/<nom_orga>', methods =['GET'])
    @LoggedIn
    @reqrole(['admin'])
    def users(nom_orga):
        metadata= {'title': 'Users'}

        return render_template('users.html', metadata=metadata, ogs=ogs, us=us, orga=nom_orga)

    @app.route('/deleteUsn/<username>',methods=['POST','GET'])
    @LoggedIn
    @reqrole(['admin'])
    def deleteUser(username):

        # Create the log before and insert it in the database before delete the user
        user_orga = us.udao.getOrganisationByUsername(username)
        orga_id = ogs.getIdByName(user_orga)
        log.ldao.createLog("DELETE", f"l'utilisateur {username} a été supprimé de la base de données.",
                           datetime.datetime.now(), orga_id)
        

        us.deleteByUsername(username)
        return redirect(request.referrer)
    
    @app.route('/editUsn/<username>', methods=['GET', 'POST'])
    @LoggedIn
    @reqrole(['admin'])
    def editUser(username):
        
        if request.method == 'POST':
            # Récupération des données du formulaire
            new_password = request.form.get('password')
            new_role = request.form.get('role')
            
            # Récupérer tous les rôles disponibles pour validation
            available_roles = us.udao.getAllRoles()
            
            # Vérification du rôle
            if not new_role or new_role not in available_roles:
                return "Erreur : Rôle invalide", 400
            
            # Mise à jour du mot de passe si fourni
            if new_password and new_password.strip():
                us.udao.changePassword(username, new_password)
            
            user_name_session = session.get('username')
            orga_id = session.get('organisation_name')
            log.ldao.createLog("EDIT_USER",
                               f"Le mot de passe de l'utilisateur {username} a été changé par {user_name_session}",
                               datetime.datetime.now(),
                               orga_id
                            )
            # Mise à jour du rôle
            us.udao.updateUserRole(username, new_role)
            log.ldao.createLog("EDIT_USER",
                               f"Le rôle de l'utilisateur {username} a été changé en {new_role} par {user_name_session}",
                               datetime.datetime.now(),
                               orga_id
                            )
            # Récupérer l'organisation pour redirection
            orga_name = us.udao.getOrganisationByUsername(username)
            
            if not orga_name:
                orga_name = 'default'
            
            return redirect(url_for('users', nom_orga=orga_name))
        
        else:
            # AFFICHAGE DU FORMULAIRE (GET)
            user = us.findByUsername(username)
            
            if not user:
                return "Utilisateur non trouvé", 404
            
            # Récupérer l'organisation de l'utilisateur
            orga_name = us.udao.getOrganisationByUsername(username)
            
            if not orga_name:
                orga_name = 'Harman_Kardon'
            
            # Récupérer tous les rôles disponibles
            available_roles = us.udao.getAllRoles()
            
            # Affichage du formulaire pré-rempli
            metadata = {'title': 'Modifier Utilisateur'}
            return render_template('edit_user.html', 
                                 metadata=metadata, 
                                 user=user,
                                 orga=orga_name,
                                 roles=available_roles)  # <- Passage des rôles au template
        

    @app.route('/addUser', methods=['GET', 'POST'])
    @LoggedIn
    @reqrole(['admin'])
    def addUser():
        
        if request.method == 'POST':
            # Récupération des données du formulaire
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')


            # Récupérer l'organisation pour redirection et association au nouvel utilisateur
            orga_name = session.get('organisation_name')
            
            # Récupérer tous les rôles disponibles pour validation
            available_roles = us.udao.getAllRoles()
            
            # Vérification du rôle
            if not role or role not in available_roles:
                return "Erreur : Rôle invalide", 400
            
            
            # Création de l'utilisateur
            us.udao.createUser(username, password, role, orga_name)
            # Create the log and insert it in the database
            orga_id = ogs.getIdByName(orga_name)
            log.ldao.createLog("ADD", f"l'utilisateur {username} a été implémenté dans la base de données.",
                           datetime.datetime.now(), orga_id)
            
            return redirect(url_for('users', nom_orga=orga_name))
        
        else:
            # AFFICHAGE DU FORMULAIRE (GET)
            
            # Récupérer l'organisation de où se situe
            orga_name = session.get('organisation_name')
            
            if not orga_name:
                orga_name = 'Harman_Kardon'
            
            # Récupérer tous les rôles disponibles
            available_roles = us.udao.getAllRoles()
            
            # Affichage du formulaire pré-rempli
            metadata = {'title': 'Ajouter Utilisateur'}
            return render_template('add_user.html', 
                                 metadata=metadata, 
                                 orga=orga_name,
                                 roles=available_roles)  # <- Passage des rôles au template