from flask import Flask, render_template
from modele.methodes_metiers import *
from modele.var_globale import *


def creer_app():
    app = Flask(__name__, template_folder="")
    return app


def lancer_app():
    app = Flask(__name__, template_folder="")

    @app.route("/")
    def accueil():
        connexion = connexion_bdd(user, host, db)
        data = recup_cinq_releves_sonde(connexion, 62190434)
        connexion_ferme(connexion)
        return render_template("accueil.html", title="Accueil", data=data)

    @app.route("/container")
    def historique():
        connexion = connexion_bdd(user, host, db)
        data = recup_cinq_releves_sonde(connexion, 62190434)
        connexion_ferme(connexion)
        return render_template("container/template.html", title="Container", data=data)

    if __name__ == "vue.affichage_donnees":
        app.run(debug=True)
