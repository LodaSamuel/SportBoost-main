-- SQLite
CREATE TABLE  IF NOT EXISTS utente(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password  VARCHAR(50) NOT NULL,
    indirizzo VARCHAR(50) NOT NULL,
    preferenza VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS acquisto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    costo FLOAT NOT NULL,
    id_utente INTEGER NOT NULL,
    FOREIGN KEY(id_utente) REFERENCES utente(id)
);

CREATE TABLE IF NOT EXISTS articolo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    prezzo FLOAT NOT NULL,
    sport VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ArticoloAcquisto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_acquisto INTEGER NOT NULL,
    id_articolo INTEGER NOT NULL,
    FOREIGN KEY(id_acquisto) REFERENCES acquisto(id),
    FOREIGN KEY(id_articolo) REFERENCES articolo(id)
);

CREATE TABLE IF NOT EXISTS negozio(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    luogo VARCHAR(50) NOT NULL,
    latitudine FLOAT NOT NULL,
    longitudine FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS negozioArticolo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_articolo INTEGER NOT NULL,
    id_negozio INTEGER NOT NULL,
    FOREIGN KEY(id_articolo) REFERENCES articolo(id),
    FOREIGN KEY(id_negozio) REFERENCES negozio(id)
);



INSERT INTO articolo (nome, prezzo, sport) VALUES
    ('Pallone', 12.00, 'Calcio'),
    ('Scarpe', 120.00, 'Calcio'),
    ('Canestro', 70.00, 'Basket'),
    ('Occhialini', 7.50, 'Nuoto'),
    ('Palla', 10.00, 'Pallavolo'),
    ('Palla', 16.00, 'Basket'),
    ('Mazza', 35.00, 'Baseball'),
    ('Racchetta', 28.00, 'Tennis'),
    ('Pallina', 4.00, 'Tennis'),
    ('Canna da pesca', 63.00, 'Pesca'),
    ('Guantoni', 13.80, 'Box'),
    ('Tavolo', 180.00, 'Ping pong'),
    ('Manubrio 10kg', 20.00, 'Palestra'),
    ('Scarpe', 70.00, 'Atletica');

INSERT INTO negozio (nome, luogo, latitudine, longitudine) VALUES
    ('Sport Revolution', 'Mairano', 45.449873, 10.079485),
    ('Sports Country', 'Pontegatello', 45.467309, 10.113810),
    ('GymTools', 'Brescia', 45.525305, 10.197748),
    ('Nautical Escapes', 'Brescia', 45.557166, 10.218363),
    ('Winning Whistle', 'Borgosatollo', 45.476533, 10.247395),
    ('Supreme Sprint', 'Ospitaletto', 45.560866, 10.077988),
    ('River Rascals', 'Sirmione', 45.467726, 10.594987),
    ('Street Soles', 'Rezzato', 45.514120, 10.320090),
    ('SportFuel', 'Brescia', 45.568353, 10.238387),
    ('FightFusion', 'Gussago', 45.587672, 10.159384);

INSERT INTO negozioArticolo (id_articolo, id_negozio) VALUES
    (1, 1),
    (1, 2),
    (1, 5),
    (1, 9),
    (2, 1),
    (2, 2),
    (2, 5),
    (2, 8),
    (2, 9),
    (3, 1),
    (3, 2),
    (3, 9),
    (4, 1),
    (4, 4),
    (4, 9),
    (5, 1),
    (5, 2),
    (5, 9),
    (6, 1),
    (6, 9),
    (7, 1),
    (8, 1),
    (8, 2),
    (8, 9),
    (9, 1),
    (9, 2),
    (9, 9),
    (10, 1),
    (10, 4),
    (10, 7),
    (11, 1),
    (11, 3),
    (11, 9),
    (11, 10),
    (12, 9),
    (13, 1),
    (13, 2),
    (13, 3),
    (13, 9),
    (14, 1),
    (14, 6),
    (14, 8),
    (14, 9);