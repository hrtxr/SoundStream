from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app

class LoginController:

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        metadata= {'title': 'Login'}
        
        return render_template('login.html', metadata=metadata)
    
