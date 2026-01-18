#!/bin/bash

# Configuration à modifier
username_distant_raspberry="synapse"
IP_distant_raspberry="192.168.56.101"
Dossier_source_flask="./app/static/audio/"
Dossier_destination_raspberry="/home/synapse/music"

# Retirer la connexion (Arrêter le service de musique à distance)
echo "Arrêt du lecteur distant..."
# Ajout de -o StrictHostKeyChecking=no pour eviter les blocages ssh
ssh -o StrictHostKeyChecking=no $username_distant_raspberry@$IP_distant_raspberry "sudo systemctl stop mpd"
echo "Lecteur distant arrêté"

# Synchronisation avec rsync
echo "Synchronisation des fichiers en cours..."
rsync -avr --delete --progress --include='*.mp3' --exclude='*' -e "ssh -o StrictHostKeyChecking=no" "$Dossier_source_flask" "$username_distant_raspberry@$IP_distant_raspberry:$Dossier_destination_raspberry"
echo "Synchronisation des fichiers terminée"

# Relancer le lecteur à distance
echo "Redémarrage du lecteur distant..."
ssh -o StrictHostKeyChecking=no $username_distant_raspberry@$IP_distant_raspberry "sudo systemctl restart mpd && mpc update"
echo "Lecteur distant redémarré"