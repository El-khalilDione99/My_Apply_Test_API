from flask import Flask, request, jsonify
import random


app = Flask(__name__)


@app.route('/')
def accueil():
    print('bonjour')
    
    


if __name__ == '__main__':
    app.run(debug=True)
