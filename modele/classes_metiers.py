import requests
import mysql.connector
from flask import Flask


# Liste des capteurs
ls_capt = ["06190485", "62190434", "62182233"]


# Correspondance mois:numéro
leMois = {"Jan": "01","Feb": "02", "Mar": "03", "Apr": "04", "May" : "05", "Jun": "06", "Jul" : "07",
          "Aug" : "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}


def convert_hexa(hexa: str) -> int:
    """ Convertit une chaîne hexadécimale en entier """
    return int(hexa, 16)


"""def convert_date(hexa):
    result = "20"
    for i in range(0, len(hexa), 2):
        if convert_hexa(hexa[i:i + 2]) < 10:
            result += hexa[i: i +2]
        else:
            result += str(int(hexa[i:i + 2], 16))
    return result"""


def ajout_releve_sonde(connexion, datas):
    """ Ajoute les relevés de sonde passés en paramètre dans la base de données """
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO sonde_has_releve (`Sonde_idSonde`, `Releve_idReleve`, `Temperature`, `Humidite`, "
            f"`Niveau_batterie`, `Signal_RSSI`) "
            f"VALUES ('{datas[i]['idSonde']}', {datas[i]['idReleve']}, {datas[i]['Temperature']}, '{datas[i]['Humidite']}', "
            f"{datas[i]['Niveau_batterie']}, {datas[i]['rssi']})")
        cursor.execute(req)
        connexion.commit()
    cursor.close()


def ajout_releve(connexion, datas):
    """ Ajoute les relevés passés en paramètre dans la base de données """
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO `releve` (`idReleve`, `Date_releve`) VALUES ({datas[i]['id']}, {datas[i]['date']})")
        cursor.execute(req)
        connexion.commit()
    cursor.close()


def ajout_capteur(connexion, liste):
    """ Ajoute les sondes passées en paramètre dans la base de données """
    cursor = connexion.cursor()
    for capteur in liste:
        req = f"INSERT INTO `sonde`(`idSonde`, `Nom`, `Inactif`) VALUES ('{capteur}', '', 0)"
        cursor.execute(req)
        connexion.commit()
    cursor.close()


def recup_anciens_rel(connexion) -> list:
    """ Récupère la liste des relevés enregistrés dans la base de données """
    cursor = connexion.cursor()
    cursor.execute("SELECT idReleve FROM releve")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    return lesId


def recup_liste_capteurs(connexion) -> list:
    """ Récupère la liste des sondes enregistrées dans la base de données """
    cursor = connexion.cursor()
    cursor.execute("SELECT idSonde FROM sonde")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    cursor.close()
    return lesId


def convertit_date(chaine: str) -> str:
    """ Convertit une date au format Ddd, DD MM YYYY HH:MM:SS en date au format YYYYMMDDHHMMSS """
    tabDate = chaine.split(' ')
    tabHeure = tabDate[4].split(':')
    date = tabDate[3] + leMois[tabDate[2]] + tabDate[1] + tabHeure[0] + tabHeure[1] + tabHeure[2]
    return date


def connexion_bdd(user: str, host: str, db: str):
    """ Ouvre la connexion à la base de données """
    conn = mysql.connector.connect(user=user, host=host, database=db)
    return conn


def connexion_ferme(conn):
    """ Ferme la connexion à la base de données """
    conn.close()


def recup_datas_ws() -> list:
    """ Récupère les relevés auprès du WebService et les stocke dans un tableau de tableaux """
    response = requests.get("http://app.objco.com:8099/?account=16L1SPQZS3&limit=3")
    if response.status_code != 200:
        print("Erreur de connexion")
    dico = response.json()
    # Stocke les relevés sous forme d'un tableau de tableaux à trois colonnes (0 = id, 1 = chaîne hexa, 2 = date)
    liste_releves = []
    for ligne in dico:
        liste_releves.append(ligne)
    return liste_releves


def trait_datas(conn, liste_releves: list):
    """ Traite les relevés reçus du Webservice en vue de les stocker dans la base de données """
    # Récupère la liste des capteurs
    liste_capteurs = recup_liste_capteurs(conn)
    # Stocke les relevés à enregistrer dans la BDD
    les_releves = []
    # Stocker les releves_has_sonde à enregistrer dans la BDD
    les_rel_sonde = []
    # Récupère la liste des relevés déjà présents dans la BDD
    anciens_releves = recup_anciens_rel(conn)
    for releve in liste_releves:
        # Si le relevé n'est pas déjà présent dans la BDD, récupère ses infos
        if releve[0] not in anciens_releves:
            # Récupère la date dans un format adapté à la BDD
            date = convertit_date(releve[2])
            # Ajoute les données relative au relevé dans la liste
            les_releves.append({"id": releve[0], "date": date})
            # Récupère les données du relevé pour chaque capteur présent dans ce relevé
            for capteur in liste_capteurs:
                chaine = releve[1]
                pos = chaine.find(capteur)
                if pos != -1:
                    print("Capteur n° " + str(chaine[pos:pos + 8]) + " || Relevé n° : " + str(releve[0]) +
                        " || " + str(releve[2]))
                    volt = convert_hexa(chaine[pos + 10: pos + 14]) / 1000      # Voltage
                    temp = convert_hexa(chaine[pos + 16: pos + 18]) / 10        # Température
                    signeTemp = convert_hexa(chaine[pos + 15 : pos + 16])       # Signe de la température (+ ou -)
                    temp = float("-" + str(temp)) if signeTemp == "1" else float(temp)
                    """if signeTemp == "1":
                        temp = "-" + str(temp)
                    temp = float(temp)"""
                    humid = convert_hexa(chaine[pos + 18: pos + 20])            # Taux d'humidité
                    humid = '' if humid == 255 else str(humid)
                    """humid = ''
                    else:
                        humid = str(humid)"""
                    rssi = "-" + str(convert_hexa(chaine[pos + 20: pos +22]))   # RSSI
                    rssi = float(rssi)
                    # Ajoute les données relatives au relevé de sonde dans la liste
                    datas = {"idSonde": capteur, "idReleve": releve[0], "Temperature": temp, "Humidite": humid,
                            "Niveau_batterie": volt, "rssi": rssi}
                    les_rel_sonde.append(datas)
                    # Affiche les relevés récupérés
                    print("Voltage : " + str(volt) + "V || Température : " + str(temp) + "°C || Humidité : " +
                        str(humid) + "% || RSSI : " + str(rssi) + "dBm\n")
    return les_releves, les_rel_sonde


"""
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello world!"
if __name__ == '__main__':
    app.run(debug=True)
"""

