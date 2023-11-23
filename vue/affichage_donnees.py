from flask import Flask, render_template, request, url_for, redirect, session
from modele.methodes_metiers import *
from modele.var_globale import *


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
<<<<<<< HEAD
        return render_template('historique.html', title='Historique des relevés', data=data)
    
    @app.route('/alertes')
    def alertes():
        connexion = connexion_bdd(user, host, db)
        data = recup_alertes(connexion)
        connexion_ferme(connexion)
        return render_template('alertes.html', title='Liste des alertes', data=data)
    
    @app.route('/param_alertes', methods = ['GET', 'POST'])
    def param_alertes():
        if request.method == "GET":
            return render_template('param_alertes.html', title='Définition d\'une alerte')
        elif request.method == "POST":
            tabDonnees = [request.form["hum"], request.form["freq"]]
            connexion = connexion_bdd(user, host, db)
            cree_alerte(connexion, tabDonnees)
            data = recup_cinq_releves_sonde(connexion, 62190434)
            connexion_ferme(connexion)
            return redirect(url_for('accueil', data=data))
            
=======
        return render_template("container/template.html", title="Container", data=data)

>>>>>>> f46cf362407b198abba6b0ace41676a2b1c1de88
    if __name__ == "vue.affichage_donnees":
        app.run(debug=True)
