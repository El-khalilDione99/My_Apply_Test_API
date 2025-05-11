from functools import wraps
from flask import request, jsonify
import jwt
from config import connection_postgres

SECRET_KEY = "votre_clé_secrète"  # Assure-toi que c’est bien la même utilisée dans login()

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'error': 'Token manquant'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_id = data.get('id_utilisateur')
                user_role = data.get('role')

                if role and user_role != role:
                    return jsonify({'error': 'Accès refusé pour ce rôle'}), 403

                #  Injecte les infos utilisateur dans la requête
                request.utilisateur = {
                    'id_utilisateur': user_id,
                    'username': data.get('username'),
                    'role': user_role
                }

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expiré'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token invalide'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
