#!/bin/bash

# Configuration à modifier
<<<<<<< HEAD
username_distant_raspberry="tristan"
IP_distant_raspberry="192.168.1.23"
Dossier_source_flask="/app/static/audio"
Dossier_destination_raspberry="/home/SoundStreamDevice"
Playlist="playlist_Romain" # Nom de la playlist à jouer

# Retirer la connexion (Arrêter le service de musique à distance)
echo "Arrêt du lecteur distant..."
ssh $username_distant_raspberry@$IP_distant_raspberry sudo -S sytemctl stop mpd
=======
username_distant_raspberry="synapse"
IP_distant_raspberry="192.168.56.101"
Dossier_source_flask="./app/static/audio/"
Dossier_destination_raspberry="/home/synapse/music"

# Retirer la connexion (Arrêter le service de musique à distance)
echo "Arrêt du lecteur distant..."
# Ajout de -o StrictHostKeyChecking=no pour eviter les blocages ssh
ssh -o StrictHostKeyChecking=no $username_distant_raspberry@$IP_distant_raspberry "sudo systemctl stop mpd"
>>>>>>> 00f02c4faec1855d63a55bc97c63c2be1caf8e98
echo "Lecteur distant arrêté"

# Synchronisation avec rsync
echo "Synchronisation des fichiers en cours..."
<<<<<<< HEAD
rsync -avz --progress --include '*.mp3' -e ssh $Dossier_source_flask $username_distant_raspberry@$IP_distant_raspberry:"$Dossier_destination_raspberry"
=======
rsync -avr --delete --progress --include='*.mp3' --exclude='*' -e "ssh -o StrictHostKeyChecking=no" "$Dossier_source_flask" "$username_distant_raspberry@$IP_distant_raspberry:$Dossier_destination_raspberry"
>>>>>>> 00f02c4faec1855d63a55bc97c63c2be1caf8e98
echo "Synchronisation des fichiers terminée"

# Relancer le lecteur à distance
echo "Redémarrage du lecteur distant..."
<<<<<<< HEAD
ssh $username_distant_raspberry@$IP_distant_raspberry sudo -S systemctl restart mpd
echo "Lecteur distant redémarré"

# Lancer le lecteur à distance
echo "Lancement de la lecture musicale distante..."
ssh $username_distant_raspberry@$IP_distant_raspberry sudo -S systemctl start mpd
echo "Lecture musicale distante lancée"

# Lancer la musique
ssh $username_distant_raspberry@$IP_distant_raspberry "mpc update && mpc clear && mpc load $Playlist.m3u && mpc play"
=======
ssh -o StrictHostKeyChecking=no $username_distant_raspberry@$IP_distant_raspberry "sudo systemctl restart mpd && mpc update"
echo "Lecteur distant redémarré"
>>>>>>> 00f02c4faec1855d63a55bc97c63c2be1caf8e98
