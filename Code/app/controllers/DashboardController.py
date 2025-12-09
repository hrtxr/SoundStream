from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.controllers.LoginController import LoggedIn, reqrole

class DashboardController:

    @app.route('/dashboard', methods=['GET'])
    @LoggedIn
    def index():
        metadata= {'title': 'Dashboard'}
        
        return render_template('dashboard.html', metadata=metadata)