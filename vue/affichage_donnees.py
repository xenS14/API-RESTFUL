from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from modele.methodes_metiers import *
from modele.var_globale import *
import json


def lancer_app():
    app = Flask(__name__, template_folder="")

    @app.route("/", methods = ['GET'])
    def accueil():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            data = dernier_releve_par_sonde(connexion)
            alertes = get_alertes(connexion)
            connexion_ferme(connexion)
            return render_template("templates/homepage.html", title="Accueil", data=data, lesalertes=alertes)

    @app.route("/<idsonde>")
    def histo(idsonde):
        connexion = connexion_bdd(user, host, db)
        data = recup_cinq_releves_sondev2(connexion, idsonde)
        connexion_ferme(connexion)
        return json.dumps(data)
    
    @app.route("/<idsonde>/<nbreleve>")
    def graphe(idsonde, nbreleve):
        connexion = connexion_bdd(user, host, db)
        data = recup_des_releves_de_sonde(connexion, idsonde, nbreleve)
        connexion_ferme(connexion)
        return json.dumps(data)
    
    @app.route('/gestion_sondes', methods=['GET', 'POST'])
    def gesSonde():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            sondes = get_sondes(connexion)
            connexion_ferme(connexion)
            return render_template('templates/gestion_sondes.html', title='Gestion des sondes', sondes=sondes)
        elif request.method == "POST":
            datas = {"id": request.form["idsonde"], "nom": request.form[f"name" + request.form["idsonde"]], "statut": request.form[request.form["idsonde"]]}
            connexion = connexion_bdd(user, host, db)
            if datas["nom"] == "":
                upd_statut_sonde(connexion, datas)
            else:
                upd_sonde(connexion, datas)
            sondes = get_sondes(connexion)
            connexion_ferme(connexion)
            return redirect(url_for("accueil"))
            # return render_template('templates/gestion_sondes.html', title='Gestion des sondes', sondes=sondes)
    
    @app.route('/param_alertes', methods = ['GET', 'POST'])
    def param_alertes():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            sondes = get_sondes(connexion)
            connexion_ferme(connexion)
            return render_template('templates/param_alertes.html', title='Définition d\'une alerte', sondes=sondes, message='')
        elif request.method == "POST":
            tabDonnees = [request.form["seuil"], request.form["freq"], request.form["type"], request.form["sens"], request.form["sonde"]]
            if tabDonnees[0] == '' or tabDonnees[1] == '':
                connexion = connexion_bdd(user, host, db)
                sondes = get_sondes(connexion)
                connexion_ferme(connexion)
                return render_template('templates/param_alertes.html', title='Définition d\'une alerte', sondes=sondes, message="Veuillez renseignez tous les champs.")
            connexion = connexion_bdd(user, host, db)
            cree_alerte(connexion, tabDonnees)
            data = recup_cinq_releves_sonde(connexion, 62190434)
            connexion_ferme(connexion)
            return redirect(url_for('accueil', data=data))
            
    if __name__ == "vue.affichage_donnees":
        app.run(debug=True)
