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

    