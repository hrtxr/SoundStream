# 🔉 SoundStream

### Livrable pour les évaluations des Compétences :
## Compétence 4 :
[livrable compétences 4](00-Documents/Compte_rendu_compétence_4.pdf)

### Qu'est ce que SoundStream
SoundStream est un projet que nous sommes en train de réaliser dans le cadre de la SAÉ S301 (SAÉ = projet évalué qui regroupe un ensemble de compétances afin de pouvoir appliquer les principes théoriques vus en cours). Elle est réalisée en groupe et consiste en le développement d'une application web complète.
<br>
> Rendu du projet le **19 Janvier** & Soutenance la **semaine du 20 Janvier**

### 🧑‍💻 Développeurs
| Participants      | Mail de contact                       | Discord               |
| ----------------- | ------------------------------------- | -----------           |
| HEURTAUX Romain   | heurtaux.romain@gmail.com             | romain_hrtx           |
| SY Aboubakry      | aboubakry.sy@edu.univ-paris13.fr      | -                     |
| CASSEL Kadir      | kadir.cassel06@gmail.com              | -                     |
| COLLEN Tristan    | tristan.collen@edu.univ-paris13.fr    | -                     |
| ALJANE Saif-Eddine| saifeddinealjane@gmail.com            | -                     |
- Groupe Neptune A
### 🖊️ Descriptif du projet

Dans beaucoup d’organisations (entreprises, collectivités, gares, campus…), il faut assurer une diffusion musicale continue, avec insertion de messages publicitaires et possibilité de lancer des messages urgents. L’enjeu est de garantir la continuité de service : même en cas de coupure réseau, il doit toujours y avoir de la musique qui joue. La supervision permet en plus de vérifier que chaque lecteur est bien en fonctionnement et que ses playlists de secours sont correctement synchronisées.

L’idée serait de mettre en place un système de supervision qui permette :
- de suivre l’état des lecteurs
- de mettre à jour en central la playlist locale et de la synchroniser automatiquement sur les lecteurs
- de vérifier que la playlist locale de secours est bien à jour
- de consigner les messages diffusés (musique, publicité, urgent)
- et de déclencher des alertes en cas de problème (lecteur KO, playlist obsolète,absence de diffusion).

Les étudiants développeraient la solution pour un pilote :
1. Deux lecteurs test (site principal + 2 sites distants)
2. Tableau de bord simple (état, synchro, “now playing”)
3. Stocker l’historique.
4. Scénarios de test : coupure réseau, coupure électrique, diffusion d’un message urgent, respect du planning des publicités.

### 📷 Photos du projet 

#### Maquette:
![Login](00-documents/Screenshots-Maquette/V1/Login.png "Login")

![Dashboard Admin](00-documents/Screenshots-Maquette/V1/Dashboard%20Admin.png "Dashboard Admin")

![Dashboard CM](00-documents/Screenshots-Maquette/V1/Dashboard%20CM.png "Dashboard Admin")

![Device view 1](00-documents/Screenshots-Maquette/V1/Device%20view%201.png "Device view 1")

![timetable view 1](00-documents/Screenshots-Maquette/V1/Timetable%20view%201.png "timetable view 1")

![Timetable view 2 - Calendar](00-documents/Screenshots-Maquette/V1/Timetable%20view%202%20-%20Calendar.png "Timetable view 2 - Calendar")

![Player Web](00-documents/Screenshots-Maquette/V1/Player%20web.png "Player Web")

### Produit final
*-> En cours git push origin main
Username for 'https://github.com': de création ;)*

### 🌲 Arborescence 
```
/
├── 00-Documents
│   ├── Screenshots-Maquette
│   │   └── V1
│   │       ├── Dashboard Admin.png
│   │       ├── Dashboard CM.png
│   │       ├── Device view 1.png
│   │       ├── Login.png
│   │       ├── Player web.png
│   │       ├── Timetable view 1.png
│   │       └── Timetable view 2 - Calendar.png
│   ├── Besoin_Utilisateurs.pdf
│   ├── Cahier_des_chargesV1.0.pdf
│   ├── indications.txt
│   ├── Ignore-latex-userstories.txt
│   └── Synthèse des questions à poser à Mr.pdf
├── Code
│   └── indications.txt
├── .gitignore
└── README.md
```

### 🧋 Autres Sources
- [🐈‍⬛ Le Github](https://github.com/hrtxr/SoundStream)
- [🔗 Le Moodle](https://moodle.univ-spn.fr/course/view.php?id=7746)
