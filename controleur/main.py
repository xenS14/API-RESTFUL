import mysql.connector


# Lance la connexion à la base de données
conn = mysql.connector.connect(user="manu", host="localhost", database="cubes1")


# Retrouve les températures des capteurs dans une chaîne
def recup_capteurs():
    req = "SELECT idSonde FROM sonde"
    listecapteurs = req_select(req)
    print(listecapteurs)
    chaine = "00101001CP20021XXCP10020XXETC"
    for capteur in listecapteurs:
        pos = chaine.find(capteur)
        # print("Température capteur", capteur, ":", str(chaine[pos + 5:pos + 7]) +"°C")


# Exécute une requête pour récupérer la liste des capteurs
def req_select(req):
    listecapteur = []
    result = conn.cursor()
    result.execute(req)
    resultat = result.fetchall()
    for ligne in resultat:
        listecapteur.append(ligne["id"])
    return listecapteur


recup_capteurs()
