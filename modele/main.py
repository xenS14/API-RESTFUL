import requests
import mysql.connector
import time


def convert_hexa(hexa):
    return int(hexa, 16)


def convert_date(hexa):
    result = "20"
    for i in range(0, len(hexa), 2):
        if convert_hexa(hexa[i:i + 2]) < 10:
            result += hexa[i: i +2]
        else:
            result += str(int(hexa[i:i + 2], 16))
    return result


def ajout_releve_sonde(connexion, datas):
    req = (f"INSERT INTO sonde_has_releve (`Sonde_idSonde`, `Releve_idReleve`, `Temperature`, `Humidite`, "
           f"`Niveau_batterie`, `Signal_RSSI`) "
           f"VALUES ('{datas['idSonde']}', {datas['idReleve']}, {datas['Temperature']}, '{datas['Humidite']}', "
           f"{datas['Niveau_batterie']}, {datas['rssi']})")
    cursor = connexion.cursor()
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def ajout_releve(connexion, datas):
    cursor = connexion.cursor()
    req = (f"INSERT INTO `releve` (`idReleve`, `Date_releve`) VALUES ({datas['id']}, {datas['date']})")
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def ajout_capteur(connexion, liste):
    cursor = connexion.cursor()
    for capteur in liste:
        req = f"INSERT INTO `sonde`(`idSonde`, `Nom`, `Inactif`) VALUES ('{capteur}', '', 0)"
        cursor.execute(req)
        connexion.commit()
    cursor.close()


def recup_anciens_rel(connexion):
    cursor = connexion.cursor()
    cursor.execute("SELECT idReleve FROM releve")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    return lesId


def recup_liste_capteurs(connexion):
    cursor = connexion.cursor()
    cursor.execute("SELECT idSonde FROM sonde")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    cursor.close()
    return lesId


def convertit_date(chaine):
    tabDate = chaine.split(' ')
    tabHeure = tabDate[4].split(':')
    date = tabDate[3] + leMois[tabDate[2]] + tabDate[1] + tabHeure[0] + tabHeure[1] + tabHeure[2]
    return date


# Liste capteurs
ls_capt = ["06190485", "62190434", "62182233"]

# Dico des mois
leMois = {"Jan": "01","Feb": "02", "Mar": "03", "Apr": "04", "May" : "05", "Jun": "06", "Jul" : "07",
          "Aug" : "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

i = 1
while True:
    # Ouvre la connexion à la base de données
    conn = mysql.connector.connect(user= "manu", host= "localhost", database= "iot")

    # Récupère les données du Webservice
    response = requests.get("http://app.objco.com:8099/?account=16L1SPQZS3&limit=3")
    if response.status_code != 200:
        print("Erreur de connexion")
    dico = response.json()

    # Stocke les relevés sous forme d'un tableau de tableaux à trois colonnes
    # 0 = id    1 = chaîne héxa     2 = date
    liste_releves = []
    for ligne in dico:
        liste_releves.append(ligne)

    # Récupère la liste des capteurs
    liste_capteurs = recup_liste_capteurs(conn)

    # Récupère la liste des relevés déjà présents dans la BDD
    anciens_releves = recup_anciens_rel(conn)
    for releve in liste_releves:
        # Si le relevé n'est pas présent dans la BDD
        if releve[0] not in anciens_releves:
            # Récupère la date dans un format adapté à la BDD
            # Date extraite de la chaine
            date = convert_date(releve[1][40:52])
            # Date extraite du relevé
            date = convertit_date(releve[2])
            # Stocke les données et les intègre dans la table Releve
            dataReleve = {"id": releve[0], "date": date}
            ajout_releve(conn, dataReleve)
            # Récupère les données du relevé pour chaque capteur présent dans ce relevé
            for capteur in liste_capteurs:
                chaine = releve[1]
                pos = chaine.find(capteur)
                if pos != -1:
                    print("Capteur n° " + str(chaine[pos:pos + 8]) + " || Relevé n° : " + str(releve[0]) +
                        " || " + str(releve[2]))
                    volt = convert_hexa(chaine[pos + 10: pos + 14]) / 1000
                    temp = convert_hexa(chaine[pos + 16: pos + 18]) / 10
                    signeTemp = convert_hexa(chaine[pos + 15 : pos + 16])
                    signe = ""
                    if signeTemp == "1":
                        temp = "-" + str(temp)
                    temp = float(temp)
                    humid = convert_hexa(chaine[pos + 18: pos + 20])
                    if humid == 255:
                        humid = ''
                    else:
                        humid = str(humid)
                    rssi = "-" + str(convert_hexa(chaine[pos + 20: pos +22]))
                    rssi = float(rssi)
                    # Stocke les données et les insére dans la table Sonde_has_releve
                    datas = {"idSonde": capteur, "idReleve": releve[0], "Temperature": temp, "Humidite": humid,
                            "Niveau_batterie": volt, "rssi": rssi}
                    ajout_releve_sonde(conn, datas)
                    # Affiche les relevés
                    print("Voltage : " + str(volt) + "V || Température : " + signe + str(temp) + "°C || Humidité : " +
                        str(humid) + "% || RSSI : " + str(rssi) + "dBm\n")

    # Ferme la connexion à la BDD
    conn.close()
    # Met le programme en pause pendant 304 secondes (temps entre chaque relevé)
    print("Nb de tours :", i)
    i += 1
    time.sleep(304)


"""
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello world!"
if __name__ == '__main__':
    app.run(debug=True)
"""

