import sqlite3

conn = sqlite3.connect('database.db')
with open ('schema.sql') as f:
    conn.executescript(f.read())


### DEBUG FUNCTION ###
# /!\ A SUPPRIMER APRES LA CONSTRUCTION DU SITE #
# NOUS TENONS À PRÉCISER ICI QUE LES DONNÉES ENTRÉES CI DESSOUS ONT ÉTÉS GÉRÉRÉS PAR GEMINI (INTELLIGENCE ARTIFICIELLE DE GOOGLE) A DES FINS DE BETA TESTING.

import bcrypt
from datetime import datetime, timedelta

def populate_database():
    print("--- Démarrage de l'insertion des données factices ---")
    
    # 1. UTILISATEURS & ORGANISATIONS (Ton code existant)
    password_clair = '12345'
    hashed_pw = bcrypt.hashpw(password_clair.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    users = [
        (1, "Romain", 'admin', hashed_pw),
        (2, "Tristan", 'communication', hashed_pw),
        (3, "Abou", 'commercial', hashed_pw)
    ]
    conn.executemany("INSERT INTO user_ (id_user, username, role, password) VALUES (?, ?, ?, ?)", users)

    orgas = [
        (111, 'JBL', 'Harman'),
        (112, 'Harman_Kardon', 'Harman'),
        (113, 'Samsung', 'Harman'),
        (114, 'AKG', 'Harman')
    ]
    conn.executemany("INSERT INTO organisation (id_orga, name_orga, subsidiary) VALUES (?, ?, ?)", orgas)

    links = [
        (1, 111), (1, 112),
        (2, 112), (2, 113),
        (3, 112), (3, 113)
    ]
    conn.executemany("INSERT INTO work_link (id_user, id_orga) VALUES (?, ?)", links)
    print("✅ Users, Orgas & Links insérés.")

    # 2. FILES (Fichiers Audio)
    # On simule des fichiers MP3
    now = datetime.now()
    files = [
        (1, 'Summer_Vibes_Intro.mp3', '/mnt/data/music/summer_intro.mp3', '00:03:45', now),
        (2, 'JBL_Promo_Spot.mp3', '/mnt/data/ads/jbl_promo.mp3', '00:00:30', now),
        (3, 'Ambient_Lounge.mp3', '/mnt/data/music/ambient.mp3', '00:05:20', now),
        (4, 'Samsung_Galaxy_Ad.mp3', '/mnt/data/ads/samsung_ad.mp3', '00:00:45', now)
    ]
    conn.executemany("INSERT INTO file (id_file, name, path, time_length, upload_date) VALUES (?, ?, ?, ?, ?)", files)
    print("✅ Files insérés.")

    # 3. PLANNING (Jours de la semaine)
    days = [('Monday',), ('Tuesday',), ('Wednesday',), ('Thursday',), ('Friday',), ('Saturday',), ('Sunday',)]
    conn.executemany("INSERT INTO Planning (day_) VALUES (?)", days)
    print("✅ Planning inséré.")

    # 4. PLAYLISTS
    # Playlist expire dans 30 jours
    expire = now + timedelta(days=30)
    playlists = [
        (10, 'Morning Mood', now, expire, now),
        (20, 'JBL Store Demo', now, expire, now),
        (30, 'Samsung Event', now, expire, now)
    ]
    conn.executemany("INSERT INTO playlist (id_playlist, name, creation_date, expiration_date, last_update_date) VALUES (?, ?, ?, ?, ?)", playlists)
    print("✅ Playlists insérées.")

    # 5. COMPOSITION (Lien Playlist <-> File)
    # Quelle musique va dans quelle playlist ?
    compositions = [
        (10, 1), (10, 3), # Morning Mood contient Summer Vibes et Ambient
        (20, 2), (20, 1), # JBL Store contient Promo et Summer Vibes
        (30, 4)           # Samsung Event contient Samsung Ad
    ]
    conn.executemany("INSERT INTO composition (id_playlist, id_file) VALUES (?, ?)", compositions)
    print("✅ Compositions insérées.")

    # 6. SONG_PLAYER (Les boitiers physiques)
    # Note: id_orga doit correspondre aux organisations existantes (111, 113, etc.)
    players = [
        (501, 'Showroom Paris', '192.168.1.10', 'PLAYING', now, '12 Rue de Rivoli, Paris', 111), # JBL
        (502, 'Boutique Lyon', '192.168.1.15', 'OFFLINE', now - timedelta(days=1), '5 Place Bellecour, Lyon', 113), # Samsung
        (503, 'Corner Fnac', '10.0.0.55', 'PLAYING', now, 'Centre Commercial, Lille', 112) # Harman
    ]
    conn.executemany("INSERT INTO song_player (id_player, name_place, IP_adress, state, last_synchronization, place_adress, id_orga) VALUES (?, ?, ?, ?, ?, ?, ?)", players)
    print("✅ Players insérés.")

    # 7. PLANNED (Quel jour joue quelle playlist ?)
    planned_data = [
       (10, 'Monday'), (10, 'Tuesday'),      # Morning Mood lun/mar
       (20, 'Saturday'), (20, 'Sunday'),     # JBL Demo le week-end
       (30, 'Friday')                        # Samsung Event le vendredi
    ]
    conn.executemany("INSERT INTO planned (id_playlist, day_) VALUES (?, ?)", planned_data)
    print("✅ Planning des playlists inséré.")

    # 8. LOGS (Historique)
    logs = [
        (1, 'INFO', 'Démarrage du player 501', now - timedelta(hours=2), 111),
        (2, 'ERROR', 'Échec de synchro player 502', now - timedelta(hours=1), 113),
        (3, 'WARNING', 'Mise à jour firmware requise', now, 112)
    ]
    conn.executemany("INSERT INTO log (id_log, type_log, text_log, date_log, id_orga) VALUES (?, ?, ?, ?, ?)", logs)
    print("✅ Logs insérés.")
    
    # 9. INTERACTION (Qui touche à quelle playlist ?)
    interactions = [
        (10, 1), # Romain a touché Morning Mood
        (20, 2), # Tristan a touché JBL Store Demo
        (30, 3)  # Abou a touché Samsung Event
    ]
    conn.executemany("INSERT INTO interaction (id_playlist, id_user) VALUES (?, ?)", interactions)
    print("✅ Interactions insérées.")

    conn.commit()
    print("--- Tout est bon, base prête ! ---")

# Exécution
populate_database()
conn.close()

###### 