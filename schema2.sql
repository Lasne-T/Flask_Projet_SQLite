
DROP TABLE IF EXISTS livres;
DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS emprunts;


CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    genre TEXT,
    date_publication DATE,
    disponible BOOLEAN NOT NULL DEFAULT 1
);


CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telephone TEXT NOT NULL,
    role TEXT CHECK(role IN ('administrateur', 'utilisateur')) NOT NULL DEFAULT 'utilisateur',
    date_inscription TEXT DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt TEXT DEFAULT CURRENT_TIMESTAMP,
    date_retour TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
    FOREIGN KEY (livre_id) REFERENCES livres (id)
);



CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    FOREIGN KEY (livre_id) REFERENCES livres(id)
);
