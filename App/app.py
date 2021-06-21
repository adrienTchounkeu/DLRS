from flask import Flask
from flask_restful import Api
from neomodel import db, config
from Technipedia.App.config import protocolConnexion, usernameConnexion, passwordConnexion, hoteConnexion, portConnexion, hoteRunning, portRunning
from Technipedia.App.Routes import LoadServices

# Initialisation de l'api
api = Flask('__name__')
app = Api(api)

# Etablissement de la connection avec neo4j avec pour mot de
connexion = protocolConnexion+'://'+usernameConnexion+':'+passwordConnexion+'@'+hoteConnexion+':'+portConnexion
db.set_connection(connexion)

# Configuration between neo4j and neomodel
config.DATABASE_URL = connexion

# Chargement des ressources
LoadServices.loadApp(app)

# Lancement de l'api rest au port 5000 d'hôte 127.0.0.1 ou localhost (en local) avec le mode debug activé
if __name__ == '__main__':
    api.run(debug=True, host=hoteRunning, port=portRunning)