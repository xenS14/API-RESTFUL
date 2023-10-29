from modele.classes_metiers import *
import time

# Lance la connexion à la base de données
conn = connexion_bdd("manu", "localhost", "iot")

# Récupère les données auprès du WebService à intervalle régulier
while True :
    datas = recup_datas_ws()

    # Traite les données récupérées auprès du WebService
    rel, rel_sonde = trait_datas(conn, datas)

    # Envoi les données vers la base de données
    ajout_releve(conn, rel)
    ajout_releve_sonde(conn, rel_sonde)

    # Affiche les données vers la page web
    

    # Attend 5 minutes et 4 secondes
    time.sleep(64)

# Ferme la connexion à la base de données
connexion_ferme(conn)
