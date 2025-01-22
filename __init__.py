from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

@app.route('/management_livre', methods=['GET', 'POST'])
def management_livre():
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        if 'add' in request.form:
            titre = request.form['titre']
            auteur = request.form['auteur']
            genre = request.form['genre']
            date_publication = request.form['date_publication']
            conn.execute('INSERT INTO livres (titre, auteur, genre, date_publication, disponible) VALUES (?, ?, ?, ?, ?)',
                         (titre, auteur, genre, date_publication, 1))
            conn.commit()
        elif 'delete' in request.form:
            livre_id = request.form['livre_id']
            conn.execute('DELETE FROM livres WHERE id = ?', (livre_id,))
            conn.commit()
        conn.close()

    conn = sqlite3.connect('database.db')
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('management_livre.html', livres=livres)

@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        conn = sqlite3.connect('database.db')
        livre = conn.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',)).fetchall()
        conn.close()
        return render_template('recherche_livre.html', livres=livre, titre=titre)
    return render_template('recherche_livre.html')

@app.route('/emprunt_livre', methods=['GET', 'POST'])
def emprunt_livre():
    if request.method == 'POST':
        utilisateur_id = request.form['utilisateur_id']
        livre_id = request.form['livre_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, retour_effectue) VALUES (?, ?, CURRENT_TIMESTAMP, 0)',
                     (utilisateur_id, livre_id))
        conn.execute('UPDATE livres SET disponible = 0 WHERE id = ?', (livre_id,))
        conn.commit()
        conn.close()
        return render_template('emprunt_livre.html', success=True)
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres WHERE disponible = 1').fetchall()
    utilisateurs = conn.execute('SELECT * FROM utilisateurs').fetchall()
    conn.close()
    return render_template('emprunt_livre.html', livres=livres, utilisateurs=utilisateurs)

if __name__ == "__main__":
  app.run(debug=True)
