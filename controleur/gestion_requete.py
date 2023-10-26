import modele
import vue

# Gère le traitement des requêtes client
"""
Si réception d'une requête concernant une Sonde
    Création d'un objet Sonde
    Si requête = "GET"
        Appel de la méthode get_sonde sur l'objet de la classe Sonde créé avec passage de l'id renseigné dans la requête en paramètre
        Envoi le contenu de la requête à la BDD
        Reçoit la réponse de la BDD
        Envoi les données reçues de la BDD à la vue (qui se met à jour)
Sinon si réception d'une requête concernant un Relevé
    post --> appel de la méthode 
"""