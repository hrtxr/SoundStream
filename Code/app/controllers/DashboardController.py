from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app

class DashboardController:

    @app.route('/Dashboard', methods=['GET'])
    def index():
        metadata= {'title': 'Dashboard'}
        
        return render_template('dashboard.html', metadata=metadata)