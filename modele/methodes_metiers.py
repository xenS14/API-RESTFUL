import requests
import mysql.connector
import time
from modele.var_globale import *


def connexion_bdd(user: str, host: str, db: str):
    """Ouvre la connexion à la base de données"""
    conn = mysql.connector.connect(user=user, host=host, database=db)
    return conn


def connexion_ferme(conn):
    """Ferme la connexion à la base de données"""
    conn.close()


def recup_acc_api(conn) -> str:
    """Récupère la clé pour interagir avec le Webservice"""
    cursor = conn.cursor()
    cursor.execute("SELECT account_API FROM utilisateur WHERE idUtilisateur = 1")
    record = cursor.fetchone()[0]
    cursor.close()
    return record


def convert_hexa(hexa: str) -> int:
    """Convertit une chaîne hexadécimale en entier"""
    return int(hexa, 16)


def recup_cinq_releves_sonde(connexion, sonde):
    """Récupère les 5 derniers relevés pour une sonde donnée"""
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT sonde_has_releve.*, releve.Date_releve FROM `releve` "
        "INNER JOIN `sonde_has_releve` ON sonde_has_releve.Releve_idReleve = releve.idReleve "
        f"WHERE Sonde_idSonde = {sonde} ORDER BY Releve_idReleve DESC LIMIT 5"
    )
    records = cursor.fetchall()
    lesRelSonde = []
    for record in records:
        lesRelSonde.append(
            {
                "idSonde": record[0],
                "idReleve": record[1],
                "Temp": record[2],
                "Hum": record[3],
                "Batt": record[4],
                "RSSI": record[5],
                "Date": record[6],
            }
        )
    cursor.close()
    return lesRelSonde


def recup_cinq_releves(connexion):
    """Récupère les 5 derniers relevés"""
    cursor = connexion.cursor()
    cursor.execute(f"SELECT * FROM `releve` ORDER BY Date_releve DESC LIMIT 5")
    records = cursor.fetchall()
    lesRel = []
    for record in records:
        date = record[1].strftime("%Y-%m-%d %H:%M:%S")
        lesRel.append({"id": record[0], "date": date})
    cursor.close()
    return lesRel


def ajout_releve_sonde(connexion, datas: tuple[list, dict]):
    """Ajoute les relevés de sonde passés en paramètre dans la base de données"""
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO sonde_has_releve (`Sonde_idSonde`, `Releve_idReleve`, `Temperature`, `Humidite`, `Niveau_batterie`, `Signal_RSSI`) "
            f"VALUES ('{datas[i]['idSonde']}', {datas[i]['idReleve']}, {datas[i]['Temperature']}, '{datas[i]['Humidite']}', "
            f"{datas[i]['Niveau_batterie']}, {datas[i]['rssi']})")
        try:
            cursor.execute(req)
            connexion.commit()
        except:
            print("Le relevé de sonde n'a pas pu être ajouté")
    cursor.close()


def ajout_releve(connexion, datas: tuple[list, dict]):
    """Ajoute les relevés passés en paramètre dans la base de données"""
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO `releve` (`idReleve`, `Date_releve`) VALUES ({datas[i]['id']}, {datas[i]['date']})")
        try:
            cursor.execute(req)
            connexion.commit()
        except:
            print("Le relevé n'a pas pu être ajouté")
    cursor.close()


def upd_sonde(connexion, sonde: dict):
    """
    Modifie la sonde passée en paramètre
    """
    cursor = connexion.cursor()
    req = f"UPDATE `sonde` SET `Nom`='{sonde['nom']}', `Active`='{sonde['statut']}' WHERE idsonde = {sonde['id']}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


# def ajout_sonde(connexion, sonde: dict):
#     """ Ajoute les sondes passées en paramètre dans la base de données """
#     cursor = connexion.cursor()
#     req = f"INSERT INTO `sonde`(`idSonde`, `Nom`, `Active`) VALUES ('{sonde['id']}', '', {sonde['statut']})"
#     cursor.execute(req)
#     connexion.commit()
#     cursor.close()


def del_sonde(connexion, sonde: str):
    """Supprime la sonde passée en paramètre dans la base de données"""
    cursor = connexion.cursor()
    req = f"DELETE FROM `sonde` WHERE idSonde = {sonde}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def upd_statut_sonde(connexion, sonde: dict):
    """Modifie le statut de la sonde passée en paramètre dans la base de données"""
    cursor = connexion.cursor()
    req = f"UPDATE `sonde` SET `Inactif` = {sonde['statut']} WHERE idSonde = {sonde['id']}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def recup_anciens_rel(connexion) -> list:
    """Récupère la liste des relevés enregistrés dans la base de données"""
    cursor = connexion.cursor()
    cursor.execute("SELECT idReleve FROM releve")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    cursor.close()
    return lesId


def get_cinq_dernier_releve(connexion, sonde: str, type: str):
    """
    Récupère les 5 derniers relevés pour les retourner au format JSON à l'application Web
    parm connexion: Connexion à la BDD
    param sonde: Id de la sonde
    param type: Type d'info ("Temperature" ou "Humidite")
    return: 5 derniers relevés de la sonde au format JSON
    """
    tabReleves = []
    cursorRel = connexion.cursor()
    cursorRelS = connexion.cursor()
    cursorRelS.execute(f"SELECT {type}, Releve_idReleve FROM sonde_has_releve WHERE Sonde_idSonde = {sonde} ORDER BY Releve_idReleve DESC LIMIT 5")
    records = cursorRelS.fetchall()
    for record in records:
        cursorRel.execute(f"SELECT * FROM releve WHERE idReleve = {record[1]}")
        date = cursorRel.fetchone()[1]
        tabReleves.append({"id": record[1], "date": date.strftime("%Y-%m-%d %H:%M:%S"), "valeur": record[0]})
    cursorRel.close()
    cursorRelS.close()
    return tabReleves


def recup_liste_capteurs(connexion) -> list:
    """Récupère la liste des sondes enregistrées dans la base de données"""
    cursor = connexion.cursor()
    cursor.execute("SELECT idSonde FROM sonde WHERE Active = 1")
    records = cursor.fetchall()
    lesSondes = []
    for record in records:
        lesSondes.append(record[0])
    cursor.close()
    return lesSondes


def get_sondes(connexion) -> list:
    """
    Récupère la liste des sondes et la retourne au format JSON
    param connexion: Connexion à la BDD
    return: Liste des sondes au format JSON
    """
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM sonde")
    records = cursor.fetchall()
    lesSondes = []
    for record in records:
        lesSondes.append({"id": record[0], "nom": record[1], "etat": record[2]})
    cursor.close()
    return lesSondes


def get_cinq_alertes(connexion) -> list:
    """
    Récupère la liste des sondes et la retourne au format JSON
    param connexion: Connexion à la BDD
    return: Liste des sondes au format JSON
    """
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM alerte WHERE Utilisateur_idUtilisateur = 1 LIMIT 5")
    records = cursor.fetchall()
    lesAlertes = []
    for record in records:
        lesAlertes.append({"id": record[0], "seuil": record[1], "operateur": record[2], "type": record[3], "etat": record[4], "freq": record[6]})
    cursor.close()
    return lesAlertes


def convertit_date(chaine: str) -> str:
    """
    Convertit une date du format Ddd, DD MM YYYY HH:MM:SS au format YYYYMMDDHHMMSS
    return: Date convertie
    """
    tabDate = chaine.split(' ')
    tabHeure = tabDate[4].split(':')
    date = tabDate[3] + leMois[tabDate[2]] + tabDate[1] + tabHeure[0] + tabHeure[1] + tabHeure[2]
    return date


def recup_datas_ws(cle: str) -> tuple[list, list]:
    """
    Récupère les relevés auprès du WebService et les stocke dans un tableau de tableaux
    param cle: Clé de l'account pour se connecter au Webservice
    return: Liste des relevés
    """
    response = requests.get(f"http://app.objco.com:8099/?account={cle}&limit=3")
    if response.status_code != 200:
        print("Erreur de connexion")
    dico = response.json()
    # Stocke les relevés sous forme d'un tableau de tableaux à trois colonnes (0 = id, 1 = chaîne hexa, 2 = date)
    liste_releves = []
    for ligne in dico:
        liste_releves.append(ligne)
    return liste_releves


def cree_alerte(conn, dicoDonnees):
    """
    Enregistre l'alerte dans la base de données
    """
    cursor = conn.cursor()
    req = f"INSERT INTO alerte (Niv, Operateur, Type, Actif, Utilisateur_idUtilisateur, frequence_envoi_mail) VALUES({dicoDonnees[0]}, \">\", \"Humidité\", 1, 1, {dicoDonnees[1]})"
    cursor.execute(req)
    conn.commit()
    cursor.close()


def gestion_alerte(conn, lesReleves: list[dict]):
    """Gère l'envoi des alertes"""
    """ Ne fait pas encore le lien entre Sonde et Alerte """
    # Récupère la liste des alertes actives
    lesAlertes = recup_alertes(conn)
    # Parcourt la liste des releves et des alertes
    for releve in lesReleves:
        for alerte in lesAlertes:
            # Vérifie si le seuil est déclenché
            if verif_alerte(conn, alerte, releve):
                envoiMail(conn, alerte["idUser"])


def verif_alerte(conn, alerte: dict, rel: dict) -> bool:
    """ Vérifie si l'alerte doit être envoyée """
    seuilDep = False
    dateOk = False
    if alerte["ope"] == ">":
        if alerte["type"] == "Température" and rel["Temperature"] > alerte["niv"]:
                seuilDep = True
        elif alerte["type"] == "Humidité" and rel["Humidite"] > alerte["niv"]:
            seuilDep = True
    else:
        if alerte["type"] == "Température" and rel["Temperature"] < alerte["niv"]:
                seuilDep = True
        elif alerte["type"] == "Humidité" and rel["Humidite"] < alerte["niv"]:
            seuilDep = True
    # Si le seuil d'alerte a été dépassé
    if seuilDep:
        # Si la date de dernier envoi est vide
        if alerte["d_envoi"] == "":
            dateOk = True
        # Sinon, calcule si l'intervalle est dépassé
        else:
            dateOk = check_delai(conn, alerte["d_envoi"])
        # Si le seuil est dépassé ainsi que l'intervalle
        if dateOk == True:
            return True
    return False


def check_delai(conn, dernierEnvoi) -> bool:
    """
    Vérifie le délai entre le dernier envoi et la date/heure actuelle
    """
    """
    if alerte["freq"] + alerte["d_envoi"] > date/heure de maintenant:
        return True
    else:
        return False
    """


def envoiMail(conn, idUser: int):
    """
    Envoi le mail à l'utilisateur
    """


def recup_alertes(conn) -> list[dict]:
    """Récupère la liste des alertes actives"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Niv, Operateur, Type, frequence_envoi_mail, dernier_envoi, Utilisateur_idUtilisateur FROM alerte WHERE Actif = 1"
    )
    records = cursor.fetchall()
    lesAlertes = []
    for record in records:
        lesAlertes.append(
            {
                "niv": record[0],
                "ope": record[1],
                "type": record[2],
                "freq": record[3],
                "d_envoi": record[4],
                "idUser": record[5],
            }
        )
    cursor.close()
    return lesAlertes


def trt_chaine(conn, liste_releves: list) -> tuple[list, list]:
    """Traite les relevés reçus du Webservice en vue de les stocker dans la base de données"""
    # Récupère la liste des capteurs
    liste_capteurs = recup_liste_capteurs(conn)
    # Stocke les relevés à enregistrer dans la BDD
    les_releves = []
    # Stocke les releves_has_sonde à enregistrer dans la BDD
    les_rel_sonde = []
    # Récupère la liste des relevés déjà présents dans la BDD
    anciens_releves = recup_anciens_rel(conn)
    for releve in liste_releves:
        # Si le relevé n'est pas déjà présent dans la BDD, récupère ses infos
        if releve[0] not in anciens_releves:
            # Récupère la date dans un format adapté à la BDD
            date = convertit_date(releve[2])
            # Ajoute les données relatives au relevé dans la liste
            les_releves.append({"id": releve[0], "date": date})
            # Récupère les données du relevé pour chaque capteur présent dans ce relevé
            for capteur in liste_capteurs:
                chaine = releve[1]
                # Cherche si le capteur est présent dans le relevé
                pos = chaine.find(capteur)
                if pos != -1:
                    volt = convert_hexa(chaine[pos + 10 : pos + 14]) / 1000  # Voltage
                    temp = convert_hexa(chaine[pos + 16 : pos + 18]) / 10  # Température
                    signeTemp = chaine[pos + 14 : pos + 16]  # Signe de la température (+ ou -)
                    temp = float("-" + str(temp)) if signeTemp == "1" else float(temp)
                    humid = convert_hexa(chaine[pos + 18 : pos + 20])  # Taux d'humidité
                    humid = "" if humid == 255 else str(humid)
                    rssi = "-" + str(convert_hexa(chaine[pos + 20 : pos + 22]))  # RSSI
                    rssi = float(rssi)
                    # Ajoute les données relatives au relevé de sonde dans la liste
                    les_rel_sonde.append(
                        {
                            "idSonde": capteur,
                            "idReleve": releve[0],
                            "Temperature": temp,
                            "Humidite": humid,
                            "Niveau_batterie": volt,
                            "rssi": rssi,
                        }
                    )
                    # Affiche dans la console les relevés récupérés
                    print("Capteur n° " + str(chaine[pos : pos + 8]) + " || Relevé n° : " + str(releve[0]) + " || " + str(releve[2]))
                    print("Voltage : " + str(volt) + "V || Température : " + str(temp) + "°C || Humidité : " + humid + "% || RSSI : " + str(rssi) + "dBm\n")
    return les_releves, les_rel_sonde


def lance_procedure_recup(conn):
    """Boucle sur la récupération des données auprès du Webservice et l'envoi de ces données vers la BDD à intervalles réguliers"""
    # Récupère la clé pour se connecter au Webservice
    cle = recup_acc_api(conn)
    while True:
        # Récupère les données auprès du WebService à intervalle régulier
        datas = recup_datas_ws(cle)

        # Traite les données récupérées auprès du WebService
        rel, rel_sonde = trt_chaine(conn, datas)

        # Envoi les données vers la base de données
        ajout_releve(conn, rel)
        ajout_releve_sonde(conn, rel_sonde)

        rel = []
        rel_sonde = []

        # Gère l'envoi des alertes en cas de seuil dépassé
        # gestion_alerte(conn, rel_sonde)

        # Attend 5 minutes et 4 secondes
        time.sleep(61)
