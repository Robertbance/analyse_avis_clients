from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from database.db import get_db_connection
from config.config import SECRET_KEY, DEBUG

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return jsonify({"message": "Plateforme d'analyse des avis clients"})


# ==============================
# INSCRIPTION
# ==============================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    nom = data.get("nom")
    email = data.get("email")
    password = data.get("password")

    if not nom or not email or not password:
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Connexion base de données impossible"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Utilisateur (user_nom, user_email, user_date_inscription, mot_de_passe_user)
            VALUES (%s, %s, %s, %s)
            """,
            (nom, email, datetime.now(), hashed_password)
        )
        conn.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201

    except Exception as e:
        return jsonify({"error": "Email déjà utilisé"}), 400

    finally:
        cursor.close()
        conn.close()


# ==============================
# CONNEXION
# ==============================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Connexion base de données impossible"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Utilisateur WHERE user_email = %s",
        (email,)
    )

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["mot_de_passe_user"], password):
        return jsonify({
            "message": "Connexion réussie",
            "user_id": user["user_id"]
        })

    return jsonify({"error": "Identifiants incorrects"}), 401


# ==============================
# AJOUT D'UN AVIS
# ==============================
@app.route("/avis", methods=["POST"])
def ajouter_avis():
    data = request.get_json()

    texte = data.get("texte_avis")
    user_id = data.get("user_id")

    if not texte or not user_id:
        return jsonify({"error": "Texte ou utilisateur manquant"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Connexion base de données impossible"}), 500

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Avis (texte_avis, date_avis, user_id)
        VALUES (%s, %s, %s)
        """,
        (texte, datetime.now(), user_id)
    )

    avis_id = cursor.lastrowid
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Avis enregistré",
        "avis_id": avis_id
    }), 201


# ==============================
# ANALYSE IA (SIMULÉE)
# ==============================
@app.route("/analyse/<int:avis_id>", methods=["POST"])
def analyser_avis(avis_id):
    # Simulation IA (sera remplacée par SpaCy / TensorFlow)
    sentiment = "positif"
    theme = "service"
    mots_cles = "rapide,professionnel"

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Connexion base de données impossible"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Analyse (sentiment, theme, mot_cle, date_analyse, avis_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (sentiment, theme, mots_cles, datetime.now(), avis_id)
        )
        conn.commit()
        return jsonify({"message": "Analyse effectuée avec succès"})

    except Exception:
        return jsonify({"error": "Analyse déjà existante ou avis invalide"}), 400

    finally:
        cursor.close()
        conn.close()


# ==============================
# STATISTIQUES
# ==============================
@app.route("/stats/sentiments", methods=["GET"])
def stats_sentiments():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Connexion base de données impossible"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT sentiment, COUNT(*) AS total
        FROM Analyse
        GROUP BY sentiment
        """
    )

    stats = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(stats)


# ==============================
# LANCEMENT
# ==============================
if __name__ == "__main__":
    app.run(debug=DEBUG)
