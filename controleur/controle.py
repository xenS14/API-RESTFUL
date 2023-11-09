from modele.methodes_metiers import *
from modele.var_globale import *
from vue.affichage_donnees import *
import threading

# Lance la connexion à la base de données
conn = connexion_bdd(user, host, db)

# Création d'un Thread pour la procédure de récupération et stockage des données
threading.Thread(target=lance_procedure_recup, args=(conn,)).start()

# Lance l'API
lancer_app()

# Ferme la connexion à la base de données
connexion_ferme(conn)
