import sqlite3

conn = sqlite3.connect('database.db')
with open ('schema.sql') as f:
    conn.executescript(f.read())


### DEBUG FUNCTION ###
# /!\ A SUPPRIMER APRES LA CONSTRUCTION DU SITE #

import bcrypt

def create_admin_user(username, password_clair, role):

    # Hachage du mot de passe (encode -> hash -> decode en string pour stockage)
    hashed_pw = bcrypt.hashpw(password_clair.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insertion d'un utilisateur
    conn.execute("INSERT INTO user_ (id_user, username, role, password) VALUES (?, ?, ?, ?)", 
                 (1, username, role, hashed_pw))
    
    #insertion d'organisations
    conn.execute("INSERT INTO organisation (id_orga, name_orga, subsidiary) VALUES (?, ?, ?)", 
                 (111, 'JBL', 'Harman'))
    conn.execute("INSERT INTO organisation (id_orga, name_orga, subsidiary) VALUES (?, ?, ?)", 
                 (112, 'Harman_Kardon', 'Harman'))
    conn.execute("INSERT INTO organisation (id_orga, name_orga, subsidiary) VALUES (?, ?, ?)", 
                 (113, 'Samsung', 'Harman'))
    conn.execute("INSERT INTO organisation (id_orga, name_orga, subsidiary) VALUES (?, ?, ?)", 
                 (114, 'AKG', 'Harman'))

    # Insertion de liens
    conn.execute("INSERT INTO work_link (id_user, id_orga) VALUES (?, ?)", 
                 (1, 111))
    conn.execute("INSERT INTO work_link (id_user, id_orga) VALUES (?, ?)", 
                 (1, 112))
    
    print(conn.execute("SELECT * FROM work_link").fetchall())
    
    conn.commit()
    print(f"✅ Utilisateur '{username}' (mdp: {password_clair}) créé avec succès.")

# Exécution de la fonction
create_admin_user('Romain', '12345', 'admin')
conn.close()

###### 