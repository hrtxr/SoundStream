from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService


us=UserService()
class DashboardController:

    @app.route('/organisation', methods=['GET'])
    @LoggedIn
    def organisation():
        metadata= {'title': 'Organisation Choice'}
        
        userorga = us.findUserOrganisation(session['username'])

        return render_template('organisation.html', metadata=metadata, userorga=userorga)