from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app


class TimetableController:

    @app.route('/timetable/<nom_orga>', methods =['GET'])
    def timetable(nom_orga):
        metadata= {'title': 'Timetable'}
        return render_template('timetable.html', metadata=metadata)
