DROP TABLE IF EXISTS composition;
DROP TABLE IF EXISTS interaction;
DROP TABLE IF EXISTS planned;
DROP TABLE IF EXISTS work_link;
DROP TABLE IF EXISTS song_player;
DROP TABLE IF EXISTS log;

DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS user_;
DROP TABLE IF EXISTS Planning;
DROP TABLE IF EXISTS organisation;
CREATE TABLE playlist(
   id_playlist INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   creation_date DATETIME NOT NULL,
   expiration_date DATETIME NOT NULL,
   last_update_date DATETIME NOT NULL,
   UNIQUE(name)
);

CREATE TABLE user_(
   id_user INTEGER PRIMARY KEY,
   username VARCHAR(25) NOT NULL,
   role VARCHAR(50) NOT NULL,
   password TEXT NOT NULL,
   UNIQUE(username)
);

CREATE TABLE organisation(
   id_orga INTEGER PRIMARY KEY,
   name_orga TEXT NOT NULL,
   subsidiary TEXT NOT NULL,
   UNIQUE(name_orga, subsidiary)
);

CREATE TABLE file(
   id_file INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   path TEXT NOT NULL,
   time_length TIME NOT NULL,
   upload_date DATETIME NOT NULL,
   UNIQUE(name)
);

CREATE TABLE song_player(
   id_player INTEGER PRIMARY KEY,
   name_place TEXT UNIQUE NOT NULL,
   IP_adress TEXT NOT NULL,
   state VARCHAR(50) NOT NULL,
   last_synchronization DATETIME,
   place_adress TEXT NOT NULL,
   id_orga INT NOT NULL,
   UNIQUE(IP_adress),
   FOREIGN KEY(id_orga) REFERENCES organisation(id_orga)
);

CREATE TABLE Planning(
   day_ VARCHAR(50),
   PRIMARY KEY(day_)
);

CREATE TABLE log(
   id_log INTEGER PRIMARY KEY,
   type_log TEXT NOT NULL,
   text_log TEXT NOT NULL,
   date_log DATETIME NOT NULL,
   id_orga INT NOT NULL,
   FOREIGN KEY(id_orga) REFERENCES organisation(id_orga)
);

CREATE TABLE work_link(
   id_user INT,
   id_orga INT,
   PRIMARY KEY(id_user, id_orga),
   FOREIGN KEY(id_user) REFERENCES user_(id_user),
   FOREIGN KEY(id_orga) REFERENCES organisation(id_orga)
);

CREATE TABLE composition(
   id_playlist INT,
   id_file INT,
   PRIMARY KEY(id_playlist, id_file),
   FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist),
   FOREIGN KEY(id_file) REFERENCES file(id_file)
);

CREATE TABLE interaction(
   id_playlist INT,
   id_user INT,
   PRIMARY KEY(id_playlist, id_user),
   FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist),
   FOREIGN KEY(id_user) REFERENCES user_(id_user)
);

CREATE TABLE planned(
   id_playlist INT,
   day_ VARCHAR(50),
   PRIMARY KEY(id_playlist, day_),
   FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist),
   FOREIGN KEY(day_) REFERENCES Planning(day_)
);
