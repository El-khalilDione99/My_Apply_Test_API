from flask import Blueprint, request, jsonify
import psycopg2
from config import connection_postgres

groupe_bp = Blueprint('groupe_bp', __name__)

# Connexion PostgreSQL
def connectionPs():
    return psycopg2.connect(**connection_postgres)

# Route pour créer un groupe
@groupe_bp.route('/groupes', methods=['POST'])
def creer_groupe():
    data = request.get_json()
    nom = data.get('nom')

    if not nom:
        return jsonify({'error': 'Le nom du groupe est obligatoire'}), 400

    try:
        conn = connectionPs()
        cur = conn.cursor()

        cur.execute("INSERT INTO groupe (nom) VALUES (%s) RETURNING id_groupe", (nom,))
        id_cree = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Groupe créé avec succès', 'id_groupe': id_cree}), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500
