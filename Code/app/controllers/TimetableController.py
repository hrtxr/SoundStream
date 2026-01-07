from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app


class TimetableController:

    @app.route('/timetable/<nom_orga>', methods =['GET'])
    def timetable(nom_orga):
        metadata= {'title': 'Timetable'}
        return render_template('timetable.html', metadata=metadata, orga=nom_orga)

    @app.route('/editTables/<nom_orga>', methods = ['GET', 'POST'])
    def editTables(nom_orga):
        metadata= {'title': 'Edit Tables'}
        plst={  'playlist_name' : 'Plst1',
                'title_count' : 115,
                'ads_count' : 13,
                'last_updated' : '12/12/2025'
        }
        return render_template('edit_tables.html', metadata=metadata, orga=nom_orga, plst=plst)