from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.OrganisationService import OrganisationService

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
    def deleteUsn(username):
        us.deleteByUsername(username)
        return redirect(request.referrer)
    
    @app.route('/editUsn/<username>', methods=['GET', 'POST'])
    @LoggedIn
    @reqrole(['admin'])
    def editUsn(username):
        
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
            
            # Mise à jour du rôle
            us.udao.updateUserRole(username, new_role)
            
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