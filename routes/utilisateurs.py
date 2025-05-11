from flask import Blueprint, request, jsonify
import psycopg2
from config import connection_postgres
from utils.authentifier_utils import token_required

# Création du Blueprint
utilisateur_bp = Blueprint('utilisateur_bp', __name__)

# Fonction de connexion
def connectionPs():
    return psycopg2.connect(**connection_postgres)

# Route pour créer un utilisateur
@utilisateur_bp.route('/utilisateurs', methods=['POST'])
def creer_utilisateur():
    data = request.get_json()
    
    nom = data.get('username')
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    role = data.get('role')
    groupe_id = data.get('groupe_id')
    
    if not nom or not email or not mot_de_passe or not role:
        return jsonify({'error': 'Les champs username, email, mot_de_passe et role sont obligatoires.'}), 400
    
    try:
        conn = connectionPs()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO utilisateur (username, email, mot_de_passe, role, groupe_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, email, mot_de_passe, role, groupe_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        error_message = str(e)
        if "unique" in error_message.lower():
            return jsonify({'error': 'Un utilisateur avec ce nom ou cet email existe déjà'}), 400
        elif "check" in error_message.lower():
            return jsonify({'error': 'Le rôle doit être "admin" ou "user"'}), 400
        else:
            return jsonify({'error': error_message}), 500


