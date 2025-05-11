from flask import Blueprint, request, jsonify
import psycopg2
from config import connection_postgres
from utils.authentifier_utils import token_required

admin_bp = Blueprint('admin', __name__)

# Fonction pour connecter à PostgreSQL
def connectionPs():
    return psycopg2.connect(**connection_postgres)



# ----------------------------------par les admins pour créer un utilisateur-------------------------------------
@admin_bp.route('/admin/utilisateurs', methods=['POST'])
@token_required(role='admin')
def creer_utilisateur_admin():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    role = data.get('role', 'user')
    groupe_id = data.get('groupe_id')

    if not username or not email or not mot_de_passe or not role:
        return jsonify({'error': 'Champs requis: username, email, mot_de_passe, role'}), 400

    try:
        conn = connectionPs()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO utilisateur (username, email, mot_de_passe, role, groupe_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, mot_de_passe, role, groupe_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Utilisateur créé avec succès par l\'admin'}), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


# --------------------------------pour supprimer un utilisateur-----------------------------------------------
@admin_bp.route('/admin/utilisateurs/<int:id_utilisateur>', methods=['DELETE'])
@token_required(role='admin')
def supprimer_utilisateur(id_utilisateur):
    try:
        conn = connectionPs()
        cur = conn.cursor()

        cur.execute("DELETE FROM utilisateur WHERE id_utilisateur = %s", (id_utilisateur,))
        if cur.rowcount == 0:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


# -------------------------qui pemmetre à l'admin ed créer un groupe----------------------------------------
@admin_bp.route('/admin/groupes', methods=['POST'])
@token_required(role='admin')
def creer_groupe():
    data = request.get_json()
    nom = data.get('nom')

    if not nom:
        return jsonify({'error': 'Le champ "nom" est obligatoire'}), 400

    try:
        conn = connectionPs()
        cur = conn.cursor()

        # Insère uniquement le nom, l'id_groupe sera généré automatiquement
        cur.execute("""
            INSERT INTO groupe (nom)
            VALUES (%s)
        """, (nom,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Groupe créé avec succès'}), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


# --------------------------qui lui permet de supprimer d'un groupe---------------------------
@admin_bp.route('/admin/groupes/<int:id_groupe>', methods=['DELETE'])
@token_required(role='admin')
def supprimer_groupe(id_groupe):
    try:
        conn = connectionPs()
        cur = conn.cursor()

        # Vérifier d’abord s’il y a des utilisateurs dans le groupe
        cur.execute("SELECT COUNT(*) FROM utilisateur WHERE groupe_id = %s", (id_groupe,))
        count = cur.fetchone()[0]

        if count > 0:
            return jsonify({'error': 'Impossible de supprimer un groupe contenant des utilisateurs'}), 400

        cur.execute("DELETE FROM groupe WHERE id_groupe = %s", (id_groupe,))
        if cur.rowcount == 0:
            return jsonify({'error': 'Groupe non trouvé'}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Groupe supprimé avec succès'}), 200

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500

