from flask import Blueprint, request, jsonify
import jwt
import datetime
import psycopg2
from config import connection_postgres
from utils.authentifier_utils import SECRET_KEY

auth_bp = Blueprint('auth', __name__)

def connectionPs():
    return psycopg2.connect(**connection_postgres)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    role = data.get('role')

    if not username or not role:
        return jsonify({'error': 'Username et rôle requis'}), 400

    try:
        conn = connectionPs()
        cur = conn.cursor()

        # Cherche d'abord l'utilisateur par username
        cur.execute("SELECT id_utilisateur, role FROM utilisateur WHERE username = %s", (username,))
        user = cur.fetchone()

        if not user:
            return jsonify({'error': 'Utilisateur introuvable avec ce nom'}), 404

        id_utilisateur, role_en_base = user

        # Vérifie si le rôle correspond
        if role_en_base != role:
            return jsonify({'error': f"Rôle invalide. Le rôle réel de cet utilisateur est : {role_en_base}"}), 403

        # Génère le token
        token = jwt.encode({
            'username': username,
            'role': role,
            'id_utilisateur': id_utilisateur,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        cur.close()
        conn.close()

        return jsonify({'token': token}), 200

    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({'error': str(e)}), 500
