from flask import Flask
from routes.utilisateurs import utilisateur_bp
from routes.g_Utilisateur import groupe_bp
from utils.login import auth_bp
from routes.admin_rotes import admin_bp
from routes.user_route import user_bp




app = Flask(__name__)
app.register_blueprint(utilisateur_bp)
app.register_blueprint(groupe_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)



@app.route('/')
def accueil():
    return "Bienvenue dans notre API"

if __name__ == '__main__':
    app.run(debug=True)
