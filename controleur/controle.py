from modele.methodes_metiers import *
from vue.affichage_donnees import *
import time

# Lance la connexion à la base de données
conn = connexion_bdd("manu", "localhost", "iot")

# Récupère les données auprès du WebService à intervalle régulier
while True :
    datas = recup_datas_ws()

    # Traite les données récupérées auprès du WebService
    rel, rel_sonde = trt_chaine(conn, datas)

    # Envoi les données vers la base de données
    ajout_releve(conn, rel)
    ajout_releve_sonde(conn, rel_sonde)

    # Récupère les 5 derniers relevés
    rel = recup_cinq_releves(conn)

    # Affiche les 5 derniers relevés dans la page web
    lancer_app(rel)

    # Attend 5 minutes et 4 secondes
    time.sleep(64)

# Ferme la connexion à la base de données
connexion_ferme(conn)
