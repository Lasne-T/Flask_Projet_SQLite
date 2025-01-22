import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('database.db')

# Exécution du script SQL pour créer les tables
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des utilisateurs
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('DUPONT', 'Emilie', 'emilie.dupont@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('LEROUX', 'Lucas', 'lucas.leroux@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('MARTIN', 'Amandine', 'amandine.martin@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('TREMBLAY', 'Antoine', 'antoine.tremblay@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('LAMBERT', 'Sarah', 'sarah.lambert@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('GAGNON', 'Nicolas', 'nicolas.gagnon@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('DUBOIS', 'Charlotte', 'charlotte.dubois@example.com', '0123456789', 'Utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, prenom, email, telephone, role) VALUES (?, ?, ?, ?, ?)", ('LEFEVRE', 'Thomas', 'thomas.lefevre@example.com', '0123456789', 'Utilisateur'))

# Insertion des livres
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction', '1943-04-06', 1))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)", ('1984', 'George Orwell', 'Dystopie', '1949-06-08', 1))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)", ('Les Misérables', 'Victor Hugo', 'Classique', '1862-01-01', 1))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)", ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantasy', '1997-06-26', 1))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)", ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 'Fantasy', '1954-07-29', 1))

# Insertion des stocks
cur.execute("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", (1, 5))
cur.execute("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", (2, 3))
cur.execute("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", (3, 2))
cur.execute("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", (4, 4))
cur.execute("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", (5, 1))

# Validation des transactions et fermeture de la connexion
connection.commit()
connection.close()
