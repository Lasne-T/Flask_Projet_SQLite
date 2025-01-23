from flask import Flask, render_template_string, render_template, request, jsonify, render_template, redirect, url_for, session
import sqlite3
from sqlite3 import Error
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def create_connection():
    """Créer une connexion à la base de données SQLite."""
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except Error as e:
        print(e)
    return None

def init_db():
    """Initialiser la base de données."""
    with app.app_context():
        conn = create_connection()
        with open('schema2.sql') as f:
            conn.executescript(f.read())
        conn.close()
        
@app.route('/')
def hello_world():
    return render_template('hello.html')
    
@app.route('/api/livres', methods=['GET'])
def get_livres():
    """Récupérer tous les livres."""
    conn = create_connection()
    livres = conn.execute("SELECT * FROM livres").fetchall()
    conn.close()
    return jsonify([{
        'id': livre[0],
        'titre': livre[1],
        'auteur': livre[2],
        'genre': livre[3],
        'date_publication': livre[4],
        'disponible': bool(livre[5])
    } for livre in livres])

@app.route('/api/livres/<int:livre_id>', methods=['GET'])
def get_livre(livre_id):
    """Récupérer un livre par son ID."""
    conn = create_connection()
    livre = conn.execute("SELECT * FROM livres WHERE id = ?", (livre_id,)).fetchone()
    conn.close()
    if livre:
        return jsonify({
            'id': livre[0],
            'titre': livre[1],
            'auteur': livre[2],
            'genre': livre[3],
            'date_publication': livre[4],
            'disponible': bool(livre[5])
        })
    return jsonify({'error': 'Livre non trouvé'}), 404

@app.route('/api/livres', methods=['POST'])
def create_livre():
    """Créer un nouveau livre."""
    data = request.get_json()
    titre = data.get('titre')
    auteur = data.get('auteur')
    genre = data.get('genre')
    date_publication = data.get('date_publication')

    if not all([titre, auteur, genre, date_publication]):
        return jsonify({'error': 'Données invalides'}), 400

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)",
        (titre, auteur, genre, date_publication, 1)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Livre créé avec succès', 'id': new_id}), 201

@app.route('/api/livres/<int:livre_id>', methods=['PUT'])
def update_livre(livre_id):
    """Mettre à jour les informations d'un livre."""
    data = request.get_json()
    titre = data.get('titre')
    auteur = data.get('auteur')
    genre = data.get('genre')
    date_publication = data.get('date_publication')
    disponible = data.get('disponible')

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE livres
        SET titre = ?, auteur = ?, genre = ?, date_publication = ?, disponible = ?
        WHERE id = ?
        """,
        (titre, auteur, genre, date_publication, disponible, livre_id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Livre non trouvé'}), 404

    return jsonify({'message': 'Livre mis à jour avec succès'})

@app.route('/api/livres/<int:livre_id>', methods=['DELETE'])
def delete_livre(livre_id):
    """Supprimer un livre."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livres WHERE id = ?", (livre_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Livre non trouvé'}), 404

    return jsonify({'message': 'Livre supprimé avec succès'})

@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    """Rechercher un livre par titre."""
    if request.method == 'POST':
        titre = request.form['titre']
        conn = create_connection()
        livres = conn.execute("SELECT * FROM livres WHERE titre LIKE ?", (f'%{titre}%',)).fetchall()
        conn.close()
        return render_template('recherche_livre.html', livres=livres, titre=titre)

    return render_template('recherche_livre.html')

@app.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    """Ajouter un livre."""
    titre = request.form['titre']
    auteur = request.form['auteur']
    genre = request.form['genre']
    date_publication = request.form['date_publication']

    if not all([titre, auteur, genre, date_publication]):
        return redirect(url_for('gestion_livres'))

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)",
        (titre, auteur, genre, date_publication, 1)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_livres'))

@app.route('/supprimer_livre', methods=['POST'])
def supprimer_livre():
    """Supprimer un livre."""
    livre_id = request.form['id']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livres WHERE id = ?", (livre_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_livres'))

@app.route('/gestion_livres')
def gestion_livres():
    """Afficher la page de gestion des livres."""
    conn = create_connection()
    livres = conn.execute("SELECT * FROM livres").fetchall()
    conn.close()
    return render_template('gestion_livres.html', livres=livres)
    
    @app.route('/gestion_stocks', methods=['GET'])
def gestion_stocks():
    """Afficher les stocks de livres avec un tableau et des graphiques."""
    conn = create_connection()
    stocks = conn.execute("""
        SELECT s.id, l.titre, l.auteur, s.quantite
        FROM stocks s
        JOIN livres l ON s.livre_id = l.id
    """).fetchall()
    conn.close()

    # Préparer les données pour les graphiques
    labels = [stock[1] for stock in stocks]
    quantities = [stock[3] for stock in stocks]
    stock_data = {
        'labels': labels,
        'quantities': quantities
    }

    return render_template('gestion_stocks.html', stocks=stocks, stock_data=stock_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
