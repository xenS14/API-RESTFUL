from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from modele.methodes_metiers import *
from modele.var_globale import *
import json


def lancer_app():
    app = Flask(__name__, template_folder="")

    # Page d'accueil de l'interface
    @app.route("/", methods = ['GET'])
    def accueil():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            data = dernier_releve_par_sonde(connexion)
            alertes = recup_liste_alertes(connexion)
            util = recup_user(connexion)
            ip = recup_adresse_ip()
            connexion.close()
            return render_template("templates/homepage.html", data=data, lesalertes=alertes, util=util, ip=ip)
    
    # Récupère un nombre déterminé de relevés pour la sonde passée en paramètre
    @app.route("/releve/<idsonde>/<nbreleve>")
    def recup_releve_par_sonde(idsonde, nbreleve):
        connexion = connexion_bdd(user, host, db)
        data = recup_des_releves_sonde(connexion, idsonde, nbreleve)
        connexion.close()
        return json.dumps(data)
    
    # Récupère le nombre de relevé pour la sonde passée en paramètre
    @app.route("/nbreleve/<idsonde>")
    def recup_nb_de_releve(idsonde):
        connexion = connexion_bdd(user, host, db)
        nbreleve = recup_nb_releve_sonde(connexion, idsonde)
        data = recup_des_releves_sonde(connexion, idsonde, nbreleve)
        connexion.close()
        return json.dumps(data)
    
    # Récupère la liste des sondes
    @app.route("/sondes")
    def recup_les_sondes():
        connexion = connexion_bdd(user, host, db)
        data = recup_sondes(connexion)
        connexion.close()
        return json.dumps(data)
    
    # Récupère la sonde passé en paramètre
    @app.route("/sonde/<idsonde>")
    def recup_une_sonde(idsonde):
        connexion = connexion_bdd(user, host, db)
        data = recup_sondes(connexion, idsonde)
        connexion.close()
        return json.dumps(data)
    
    # Affiche la page de gestion des sondes et crée les routes pour les ajouts et mise à jour des sondes
    @app.route('/gestion_sondes', methods=['GET', 'POST'])
    def gesSonde():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            sondes = recup_sondes(connexion)
            connexion.close()
            return render_template('templates/gestion_sondes.html', title='Gestion des sondes', sondes=sondes)
        elif request.method == "POST":
            connexion = connexion_bdd(user, host, db)
            donneesAction = {"action": request.form["action"][:6], "id":request.form["action"][6:]}
            if donneesAction["action"] == "delete":
                suppr_sonde(connexion, donneesAction["id"])
            elif donneesAction["action"] == "ajoute":
                datas = {"id": request.form["cree-id-sonde"], "nom": request.form["cree-nom-sonde"]}
                ajout_sonde(connexion, datas)
            elif donneesAction["action"] == "update":
                datas = {"id": donneesAction["id"], "nom": request.form[f"name" + donneesAction["id"]], "statut": request.form[donneesAction["id"]]}
                if datas["nom"] == "":
                    maj_statut_sonde(connexion, datas)
                else:
                    maj_sonde(connexion, datas)
            connexion.close()
            return redirect(url_for("accueil"))
    
    # Affiche la page de gestion des alertes et crée la route pour la création d'alertes
    @app.route('/param_alertes', methods = ['GET', 'POST'])
    def param_alertes():
        if request.method == "GET":
            connexion = connexion_bdd(user, host, db)
            sondes = recup_sondes(connexion)
            connexion.close()
            return render_template('templates/param_alertes.html', sondes=sondes, message='')
        elif request.method == "POST":
            tabDonnees = [request.form["seuil"], request.form["freq"], request.form["type"], request.form["sens"], request.form["sonde"]]
            if tabDonnees[0] == '' or tabDonnees[1] == '':
                connexion = connexion_bdd(user, host, db)
                sondes = recup_sondes(connexion)
                connexion.close()
                return render_template('templates/param_alertes.html', title='Définition d\'une alerte', sondes=sondes, message="Veuillez renseignez les champs seuil ET fréquence.")
            connexion = connexion_bdd(user, host, db)
            cree_alerte(connexion, tabDonnees)
            data = recup_des_releves_sonde(connexion, 62190434)
            connexion.close()
            return redirect(url_for('accueil', data=data))
            
    if __name__ == "vue.affichage_donnees":
        app.run(debug=True)
