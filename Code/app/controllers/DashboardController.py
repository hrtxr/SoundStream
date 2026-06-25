from flask import render_template, session, redirect, url_for, request
from app import app
from app.controllers.LoginController import LoggedIn, reqrole
from app.services.UserService import UserService
from app.services.TimeTableService import TimeTableService
from app.services.SongPlayerService import SongPlayerService
from app.services.OrganisationService import OrganisationService
from app.services.LogService import LogService
from app.services.FileService import FileService
from app.services.AdvertisementService import AdvertisementService
import datetime
import subprocess


us = UserService()
tts = TimeTableService()
sps = SongPlayerService()
ogs = OrganisationService()
los = LogService()
file_service = FileService()
ads = AdvertisementService()


class DashboardController:

    @app.route('/dashboard/<nom_orga>', methods=['GET', 'POST'])
    @LoggedIn
    def dashboard(nom_orga):
        metadata = {'title': 'Dashboard'}
        session['organisation_name'] = nom_orga

        # Get organization ID once to optimize database queries
        id_orga = ogs.getIdByName(nom_orga)

        # Get all players for this organization as a list of dictionaries
        liste_song_player_dict = sps.findAllSongPlayerByOrganisation(id_orga)

        # Retrieve the count of online and offline players for this organization
        nb_on_and_nb_off = sps.countNumberOfSongPlayerOnlineAndOffline(id_orga)

        # Unpack counters from the result tuple
        nb_on = nb_on_and_nb_off[0]
        nb_off = nb_on_and_nb_off[1]

        tts.autoCleanPlaylists()

        # Consolidate variables into a single context dictionary
        context = {
            'metadata': metadata,
            'orga': nom_orga,
            'us': us,
            'tts': tts,
            'sps': sps,
            'ogs': ogs,
            'los': los,
            'nb_on': nb_on,
            'nb_off': nb_off,
            'liste_song_player': liste_song_player_dict
        }

        # Render the dashboard with the context dictionary
        return render_template('dashboard.html', context=context)

    @app.route('/emergencyMessage', methods=['POST'])
    @reqrole(['sales'])
    @LoggedIn
    def emergencyMessage():
        """Handle emergency message upload and broadcast to all devices."""
        metadata = {'title': 'Add Emergency Message'}

        nom_orga = session.get('organisation_name')

        # Validate file presence in request
        if 'uploadfile' not in request.files:
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        file_storage = request.files['uploadfile']
        if not file_storage or file_storage.filename == '':
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        # Save the uploaded file
        form = request.form.to_dict()
        form['file_type'] = 'mp3'
        file_id = file_service.createFileFromForm(form, file_storage)

        if file_id == -1:
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        # Retrieve the emergency file metadata from the database
        emergency_file = file_service.findFileById(file_id)
        filename = emergency_file.name

        # Parse duration string (e.g. "01:30" -> 90 seconds)
        duration_seconds = 30  # Default fallback
        try:
            if emergency_file.time_length:
                parts = emergency_file.time_length.split(':')
                if len(parts) == 2:
                    duration_seconds = int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except Exception as e:
            print(f"Error computing duration (defaulting to 30s): {e}")

        # Broadcast to all devices in the organization
        orga_id = ogs.getIdByName(nom_orga)
        devices = sps.findAllSongPlayerByOrganisation(orga_id)

        for device in devices:
            # Attempt broadcast even if marked OFFLINE (device may have reconnected)
            ip = device['IP_adress']
            # Retrieve the SSH username for this device (stored as device_name)
            user_vm = device['device_name']

            # Sync the file to device
            try:
                sps.sync_to_device(ip, user_vm)
            except Exception as e:
                print(f"Error syncing to {ip}: {e}")
                continue
            # Pause MPD, play the emergency file, then resume MPD
            cmd = f"export PATH=$PATH:/opt/homebrew/bin:/usr/local/bin && mpc pause ; mpg123 \"~/music/{filename}\" ; mpc play"

            # Execute asynchronously via SSH
            try:
                subprocess.Popen(
                    ["ssh", "-o", "StrictHostKeyChecking=no", f"{user_vm}@{ip}", cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Emergency sent to {ip} (schedule catch-up: +{duration_seconds}s)")
            except Exception as e:
                print(f"Error on {ip}: {e}")

        # Log the emergency broadcast
        username = session.get('username')
        los.createLog(
            "UPLOAD_EMERGENCY",
            f"User {username} broadcast emergency: {filename}",
            datetime.datetime.now(),
            orga_id
        )

        return redirect(url_for('dashboard', nom_orga=nom_orga))

    @app.route('/advertisement', methods=['POST'])
    @reqrole(['sales'])
    @LoggedIn
    def advertisement():
        """Handle advertisement message upload."""
        metadata = {'title': 'Upload Advertisement Message'}

        nom_orga = session.get('organisation_name')

        # Validate file presence in request
        if 'uploadfile' not in request.files:
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        file_storage = request.files['uploadfile']
        if not file_storage or file_storage.filename == '':
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        # Save the uploaded file
        form = request.form.to_dict()
        form['file_type'] = 'mp3'
        file_id = file_service.createFileFromForm(form, file_storage)

        if file_id == -1:
            return redirect(url_for('dashboard', nom_orga=nom_orga))

        # Schedule the advertisement
        play_time = request.form.get('heure_choisie')
        play_date = request.form.get('date_choisie')
        orga_id = ogs.getIdByName(nom_orga)
        
        if play_time and play_date:
            ads.scheduleAdvertisement(file_id, orga_id, play_date, play_time)

        # Log the advertisement upload
        username = session.get('username')
        los.createLog(
            "UPLOAD_ADVERTISEMENT",
            f"User {username} scheduled advertisement {file_storage.filename} for {play_date} at {play_time}",
            datetime.datetime.now(),
            orga_id
        )

        return redirect(url_for('dashboard', nom_orga=nom_orga))