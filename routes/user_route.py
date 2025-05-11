from flask import Blueprint, request, jsonify
from utils.authentifier_utils import token_required
import psycopg2
from config import connection_postgres

user_bp = Blueprint('user', __name__)

# Connexion PostgreSQL
def connectionPs():
    return psycopg2.connect(**connection_postgres)

# Route pour créer un prompt (rôle 'user' uniquement)
@user_bp.route('/user/prompts', methods=['POST'])
@token_required(role='user')
def creer_prompt_utilisateur():
    data = request.get_json()
    contenu = data.get('contenu')
    prix = data.get('prix', 1000)  # valeur par défaut

    if not contenu:
        return jsonify({'error': 'Le contenu du prompt est requis'}), 400

    try:
        conn = connectionPs()
        cur = conn.cursor()

        # Récupérer l'identité de l'utilisateur connecté via le token
        utilisateur_connecte = request.utilisateur  # injecté par @token_required
        utilisateur_id = utilisateur_connecte.get('id_utilisateur')  # à adapter selon ton décorateur

        cur.execute("""
            INSERT INTO prompt (contenu, statut, prix, utilisateur_id)
            VALUES (%s, %s, %s, %s)
        """, (contenu, 'en_attente', prix, utilisateur_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Prompt créé avec succès'}), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500
