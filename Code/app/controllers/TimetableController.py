from importlib import metadata
from flask import render_template, session, redirect, url_for, request
from functools import wraps
from app import app
from app.services.TimeTableService import TimeTableService
from app.services.LogService import LogService
from app.services.OrganisationService import OrganisationService
import datetime

orga = OrganisationService()
log = LogService()
ts = TimeTableService()
class TimetableController:

    @app.route('/timetable/<nom_orga>', methods =['GET'])
    def timetable(nom_orga):
        metadata= {'title': 'Timetable'}
        return render_template('timetable.html', metadata=metadata, orga=nom_orga)

    
    ####################
    ## EDIT PLAYLISTS ##
    ####################

    @app.route('/editPlaylist/<nom_orga>', methods=['GET'])
    def editPlaylist(nom_orga):
        metadata = {'title': 'Edit Playlist'}
        
        playlists = ts.getAllPlaylists()
        
        selected_playlist_id = request.args.get('playlist_id')
        selected_playlist = None
        files = []
        title_count = 0
        ads_count = 0
        
        if selected_playlist_id:
            details = ts.getPlaylistDetails(int(selected_playlist_id))
            if details:
                selected_playlist = details['playlist']
                files = details['files']
                title_count = details['title_count']
                ads_count = details['ads_count']
        
        return render_template('edit_playlist.html', 
                             metadata=metadata, 
                             orga=nom_orga, 
                             playlists=playlists if playlists else [],
                             selected_playlist=selected_playlist,
                             files=files,
                             title_count=title_count,
                             ads_count=ads_count)

    @app.route('/choosePlaylist/<nom_orga>', methods=['POST'])
    def choosePlaylist(nom_orga):
        playlist_id = request.form.get('playlist_id')
        return redirect(url_for('editPlaylist', nom_orga=nom_orga, playlist_id=playlist_id))

    @app.route('/addFileToPlaylist/<nom_orga>/<int:playlist_id>', methods=['POST'])
    def addFileToPlaylist(nom_orga, playlist_id):
        filename = request.form.get('filename')
        file_type = request.form.get('file_type', 'mp3')
        if filename:
            ts.addFileToPlaylist(playlist_id, filename, file_type)

        username = session.get('username')
        orga_id = orga.getIdByName(session.get('organisation_name'))
        playlist_name = ts.getPlaylistNameById(playlist_id)

        log.ldao.createLog("ADD_FILE",
                            f"l'utilisateur {username} a ajouté le fichier {filename} dans la playlist {playlist_name}.",
                           datetime.datetime.now(),
                             orga_id)
        
        return redirect(url_for('editPlaylist', nom_orga=nom_orga, playlist_id=playlist_id))

    @app.route('/deleteFileFromPlaylist/<nom_orga>/<int:playlist_id>/<int:file_id>', methods=['GET'])
    def deleteFileFromPlaylist(nom_orga, playlist_id, file_id):
        username = session.get('username')
        orga_id = orga.getIdByName(session.get('organisation_name'))
        playlist_name = ts.getPlaylistNameById(playlist_id)

        log.ldao.createLog("REMOVE_FILE",
                            f"l'utilisateur {username} a enlevé le fichier {file_id} de la playlist {playlist_name}.",
                           datetime.datetime.now(),
                             orga_id)
        
        ts.dao.removeFileFromPlaylist(playlist_id, file_id)
        return redirect(url_for('editPlaylist', nom_orga=nom_orga, playlist_id=playlist_id))
    

    ############################
    ## EDIT PLAYLIST FOR DAYS ##
    ############################

    @app.route('/editTables/<nom_orga>', methods=['GET'])
    def editTables(nom_orga):
        metadata = {'title': 'Edit Tables'}
        days_with_playlists = ts.getAllDaysWithPlaylists()
        all_playlists = ts.getAllPlaylists()
        
        return render_template('edit_tables.html',
                             metadata=metadata,
                             orga=nom_orga,
                             days_with_playlists=days_with_playlists,
                             all_playlists=all_playlists if all_playlists else [])

    @app.route('/updateDay/<nom_orga>', methods=['POST'])
    def updateDay(nom_orga):
        day_name = request.form.get('day_name')
        playlist_id = request.form.get('playlist_id')
        start_time = request.form.get('start_time')
        if playlist_id:
            playlist_id = int(playlist_id)
        else:
            playlist_id = None 
        ts.updateDaySchedule(day_name, playlist_id, start_time)

        username = session.get('username')
        orga_id = orga.getIdByName(session.get('organisation_name'))
        log.ldao.createLog("SCHEDULE_UPDATE",
                            f"l'utilisateur {username} a mis à jour la plannificationde de la playlist {playlist_id}.",
                           datetime.datetime.now(),
                             orga_id)
        
        return redirect(url_for('editTables', nom_orga=nom_orga))