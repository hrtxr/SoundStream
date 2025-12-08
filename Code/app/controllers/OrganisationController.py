from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app

class DashboardController:

    @app.route('/Organisation', methods=['GET'])
    def organisation():
        metadata= {'title': 'Organisation Choice'}
        
        return render_template('organisation.html', metadata=metadata)