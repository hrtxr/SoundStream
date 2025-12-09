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

    # Insertion dans la table 'user_' via la connexion 'conn' déjà ouverte plus haut
    conn.execute("INSERT INTO user_ (id_user, username, role, password) VALUES (?, ?, ?, ?)", 
                 (1, username, role, hashed_pw))
    conn.commit()
    print(f"✅ Utilisateur '{username}' (mdp: {password_clair}) créé avec succès.")

# Exécution de la fonction
create_admin_user('Romain', '12345', 'admin')
conn.close()

###### 