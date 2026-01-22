import sqlite3
import os

# Récupère le dossier où se trouve le fichier initdb.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construit les chemins complets
DB_PATH = os.path.join(BASE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

# Connexion
conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH) as f:
    conn.executescript(f.read())


### DEBUG FUNCTION ###
# /!\ A SUPPRIMER APRES LA CONSTRUCTION DU SITE #
# NOUS TENONS À PRÉCISER ICI QUE LES DONNÉES ENTRÉES CI DESSOUS ONT ÉTÉS GÉRÉRÉS PAR GEMINI (INTELLIGENCE ARTIFICIELLE DE GOOGLE) A DES FINS DE BETA TESTING.

import bcrypt
from datetime import datetime, timedelta

def populate_database():
    print("--- Démarrage de l'insertion des données factices ---")

    #initialization of roles and type tables insertions

    roles = [
        ('admin', 'Administrator of the web app'),
        ('marketing', 'they create the base of the playlists and fix it to week days'),
        ('sales', 'they manage the song player and the messages to insert in the playlists')
    ]

    conn.executemany("INSERT INTO role (role, description) VALUES (?, ?)", roles)
    print("✅ Roles insérés.")

    type = [
        ('mp3',)
    ]

    conn.executemany("INSERT INTO type_file (type_file) VALUES (?)", type)
    print("✅ Types insérés.")

    # 1. UTILISATEURS & ORGANISATIONS (Ton code existant)
    password_clair = '12345'
    hashed_pw = bcrypt.hashpw(password_clair.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    users = [
        ( "Romain", 'admin', hashed_pw),
        ( "Tristan", 'marketing', hashed_pw),
        ( "Abou", 'sales', hashed_pw)
    ]
    conn.executemany("INSERT INTO user_ (username, role, password) VALUES (?, ?, ?)", users)

    orgas = [
        ('Orga1',),
        ('Orga2',),
        ('Orga3',),
    ]
    conn.executemany("INSERT INTO organisation (name_orga) VALUES (?)", orgas)

    links = [
        (1, 1), (1, 2),
        (2, 2), (2, 3),
        (3, 2), (3, 3)
    ]
    conn.executemany("INSERT INTO work_link (id_user, id_orga) VALUES (?, ?)", links)
    print("✅ Users, Orgas & Links insérés.")

    now = datetime.now()

    # 3. PLANNING (Jours de la semaine)
    days = [('Monday',), ('Tuesday',), ('Wednesday',), ('Thursday',), ('Friday',), ('Saturday',), ('Sunday',)]
    conn.executemany("INSERT INTO Planning (day_) VALUES (?)", days)
    print("✅ Planning inséré.")

    # 6. SONG_PLAYER (Les boitiers physiques)
    # Note: id_orga doit correspondre aux organisations existantes (111, 113, etc.)
    players = [
        ('Abou', '10.100.27.134', 'OFFLINE', now, '12 Rue de Rivoli','75000', 'Paris', 'centre commercial', 'aboubakry', 2), # JBL
    ]
    conn.executemany("INSERT INTO song_player (name_place, IP_adress, state, last_synchronization, place_adress, place_postcode, place_city, place_building_name, device_name, id_orga) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", players)
    print("✅ Players insérés.")

    conn.commit()
    print("--- Tout est bon, base prête ! ---")

# Exécution
populate_database()
conn.close()

###### 