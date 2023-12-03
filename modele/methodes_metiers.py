import requests, json, socket
import mysql.connector
import time
from datetime import datetime, timedelta
from modele.var_globale import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def connexion_bdd(user: str, host: str, db: str):
    """
    Ouvre la connexion à la base de données
    
    param user: Identifiant de l'utilisateur de la base de données
    param host: Adresse de la base de données
    param db: Nom de la base de données
    return: Connexion à la base de données
    """
    conn = mysql.connector.connect(user=user, host=host, database=db)
    return conn


def recup_user(conn, idUser = 1) -> str:
    """
    Récupère la clé pour interagir avec le Webservice
    
    param conn: Connexion à la base de données
    param idUser: Identifiant de l'utilisateur dans la base de données
    return: Clef account du Webservice
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM utilisateur WHERE idUtilisateur = {idUser}")
    record = cursor.fetchone()
    cursor.close()
    utilisateur = {
        "id": record[0],
        "prenom": record[1],
        "nom": record[2],
        "num_tel": record[3],
        "email": record[4],
        "id_site": record[5],
        "mdp_site": record[6],
        "acc_api": record[7],
        "mdp_appli": record[8]
    }
    return utilisateur


def recup_adresse_ip():
    """
    Récupère l'adresse ip de l'utilisateur

    return: Adresse ip de l'utilisateur
    """
    nom_hote = socket.gethostname()

    # Obtenez l'adresse IP associée au nom d'hôte
    adresse_ip = socket.gethostbyname(nom_hote)

    return adresse_ip


def convert_hexa(hexa: str) -> int:
    """
    Convertit une chaîne hexadécimale en entier
    
    param hexa: Chaîne hexadécimale à convertir
    return: Valeur entière de la chaîne convertie
    """
    return int(hexa, 16)


def recup_des_releves_sonde(connexion, sonde, nbdereleves = 5) -> list[dict]:
    """
    Récupère les 5 derniers relevés pour une sonde donnée
    
    param connexion: Connexion à la base de données
    param sonde: Identifiant de la sonde pour laquelle on veut les relevés
    param nbdereleves: Nombre de relevés souhaités pour cette sonde
    return: Liste des relevés de la sonde concernée
    """
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT sr.*, releve.Date_releve, sonde.Nom FROM sonde_has_releve AS sr "
        "INNER JOIN sonde ON sonde.idSonde = sr.Sonde_idSonde "
        "INNER JOIN releve ON releve.idReleve = sr.Releve_idReleve "
        f"WHERE Sonde_idSonde = \'{sonde}\' ORDER BY Releve_idReleve DESC LIMIT {nbdereleves}"
    )
    records = cursor.fetchall()
    lesRelSonde = []
    for record in records:
        lesRelSonde.append({"idSonde": record[0], "idReleve": record[1], "temp": record[2], "hum": record[3], "batt": record[4],
                            "rssi": record[5], "date": record[6].strftime("%d-%m-%Y %H:%M:%S"), "nom":record[7]})
    cursor.close()
    return lesRelSonde


def ajout_releve_sonde(connexion, datas: tuple[list, dict]):
    """
    Ajoute les relevés de sonde passés en paramètre dans la base de données
    
    param connexion: Connexion à la base de données
    param datas: Liste des relevés de sonde à ajouter à la table sonde_has_releve
    """
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO sonde_has_releve (`Sonde_idSonde`, `Releve_idReleve`, `Temperature`, `Humidite`, `Niveau_batterie`, `Signal_RSSI`) "
            f"VALUES ('{datas[i]['idSonde']}', {datas[i]['idReleve']}, {datas[i]['Temperature']}, '{datas[i]['Humidite']}', "
            f"{datas[i]['Niveau_batterie']}, {datas[i]['rssi']})")
        try:
            cursor.execute(req)
            connexion.commit()
        except:
            print(f"Le relevé {datas[i]['idReleve']} de la sonde {datas[i]['idSonde']} n'a pas pu être ajouté")
    cursor.close()


def ajout_releve(connexion, datas: tuple[list, dict]):
    """
    Ajoute les relevés passés en paramètre dans la base de données
    
    param connexion: Connexion à la base de données
    param datas: Liste des relevés à ajouter à la table releve
    """
    cursor = connexion.cursor()
    for i in range(len(datas)):
        req = (f"INSERT INTO `releve` (`idReleve`, `Date_releve`) VALUES ({datas[i]['id']}, {datas[i]['date']})")
        try:
            cursor.execute(req)
            connexion.commit()
        except:
            print(f"Le relevé {datas[i]['id']} n'a pas pu être ajouté")
    cursor.close()


def maj_sonde(connexion, sonde: dict):
    """
    Modifie la sonde passée en paramètre

    param connexion: Connexion à la base de données
    param sonde: Données de sonde à modifier
    """
    cursor = connexion.cursor()
    req = f"UPDATE `sonde` SET `Nom`='{sonde['nom']}', `Active`='{sonde['statut']}' WHERE idsonde = {sonde['id']}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def maj_statut_sonde(connexion, sonde: dict):
    """
    Modifie le statut de la sonde passée en paramètre

    param connexion: Connexion à la base de données
    param sonde: Sonde avec son nouveau statut à mettre à jour
    """
    cursor = connexion.cursor()
    req = f"UPDATE `sonde` SET `Active`='{sonde['statut']}' WHERE idsonde = {sonde['id']}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def ajout_sonde(connexion, sonde: dict):
    """
    Ajoute la sonde passée en paramètre dans la base de données
    
    param connexion: Connexion à la base de données
    param sonde: Sonde à ajouter
    """
    cursor = connexion.cursor()
    req = f"INSERT INTO `sonde`(`idSonde`, `Nom`, `Active`) VALUES ('{sonde["id"]}', '{sonde["nom"]}', 1)"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def suppr_sonde(connexion, sonde: str):
    """
    Supprime la sonde passée en paramètre dans la base de données
    
    param connexion: Connexion à la base de données
    param sonde: Sonde à supprimer
    """
    cursor = connexion.cursor()
    req = f"DELETE FROM `sonde` WHERE idSonde = {sonde}"
    cursor.execute(req)
    connexion.commit()
    cursor.close()


def recup_anciens_releves(connexion) -> list:
    """
    Récupère la liste des relevés enregistrés dans la base de données
    
    param connexion: Connexion à la base de données
    return: Liste des id de tous les relevés enregistrés dans la base de données
    """
    cursor = connexion.cursor()
    cursor.execute(f"SELECT idReleve FROM releve ORDER BY idReleve DESC LIMIT {nbReleveWs}")
    records = cursor.fetchall()
    lesId = []
    for record in records:
        lesId.append(record[0])
    cursor.close()
    return lesId


def recup_sondes(connexion, idSonde = '') -> list:
    """
    Récupère la liste des sondes enregistrées dans la base de données
    
    param connexion: Connexion à la base de données
    param idSonde: Identifiant de la sonde dont on veut récupérer les données
    return: Liste des sondes
    """
    where = ''
    if idSonde != '':
        where = f' WHERE idSonde = {idSonde}'
    cursor = connexion.cursor()
    cursor.execute(f"SELECT * FROM sonde{where}")
    records = cursor.fetchall()
    lesSondes = []
    for record in records:
        lesSondes.append({"id": record[0], "nom": record[1], "statut": record[2]})
    cursor.close()
    return lesSondes


def dernier_releve_par_sonde(connexion) -> list[dict]:
    """
    Récupère le dernier relevé pour chaque sonde

    param connexion: Connexion à la base de données
    return: Liste du dernier relevé de chaque sonde
    """
    lesSondes = recup_sondes(connexion)
    lesReleves = []
    for sonde in lesSondes:
        req = (
            "SELECT sonde.idSonde, sonde.Nom, sr.Temperature, sr.Humidite, releve.Date_releve "
            "FROM sonde_has_releve AS sr "
            "INNER JOIN sonde ON sonde.idSonde = sr.Sonde_idSonde "
            "INNER JOIN releve ON releve.idReleve = sr.Releve_idReleve "
            f"WHERE sonde.idSonde = {sonde["id"]} "
            "ORDER BY sr.Releve_idReleve DESC "
            "LIMIT 1"
        )
        cursor = connexion.cursor()
        cursor.execute(req)
        record = cursor.fetchone()
        if record != None:
            lesReleves.append({"idSonde": record[0], "nom":record[1], "temp":record[2], "hum":record[3], "date": record[4].strftime("%d-%m-%Y %H:%M:%S")})
        cursor.close()
    return lesReleves


def recup_nb_releve_sonde(conn, idsonde):
    """
    Récupère le nombre de relevés enregistrés pour une sonde donnée

    param conn: Connexion à la base de donnée
    param idsonde: Identifiant de la sonde
    return: Nombre de relevés pour la sonde passée en paramètre
    """
    req = f"SELECT COUNT(*) FROM sonde_has_releve WHERE Sonde_idSonde = {idsonde}"
    cursor = conn.cursor()
    cursor.execute(req)
    record = cursor.fetchone()[0]
    cursor.close()
    return record


def convertit_date(chaine: str) -> str:
    """
    Convertit une date du format Ddd, DD MM YYYY HH:MM:SS au format YYYYMMDDHHMMSS

    param chaine: Chaîne à convertir
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
    return: Liste des relevés provenant du Webservice
    """
    response = requests.get(f"http://app.objco.com:8099/?account={cle}&limit={nbReleveWs}")
    if response.status_code != 200:
        print("Erreur de connexion au Webservice")
    dico = response.json()
    # Stocke les relevés sous forme d'un tableau de tableaux à trois colonnes (0 = id, 1 = chaîne hexa, 2 = date)
    liste_releves = []
    for ligne in dico:
        liste_releves.append(ligne)
    return liste_releves


def cree_alerte(conn, datas: list):
    """
    Enregistre l'alerte dans la base de données

    param conn: Connexion à la base de données
    param datas: Données de l'alerte devant être créée
    """
    cursor = conn.cursor()
    req = f"INSERT INTO alerte (Niv, Operateur, Type, Active, Utilisateur_idUtilisateur, frequence_envoi_mail, Sonde_idSonde) VALUES({datas[0]}, \"{datas[3]}\", \"{datas[2]}\", 1, 1, {datas[1]}, \"{datas[4]}\")"
    cursor.execute(req)
    conn.commit()
    cursor.close()


def gestion_alerte(conn):
    """
    Gère l'envoi des alertes
    
    param conn: Connexion à la base de données
    """
    # Récupère le dernier relevé de chaque sonde
    lesReleves = dernier_releve_par_sonde(conn)
    # Parcourt la liste des relevés de sonde
    for releve in lesReleves:
        # Récupère la liste des alertes sur la sonde en cours
        lesAlertes = recup_alertes_sonde(conn, releve["idSonde"])
        # Parcourt la liste des alertes
        for alerte in lesAlertes:
            # Vérifie si le seuil et le délai d'envoi sont dépassés 
            if verif_alerte(conn, alerte, releve):
                if envoiMail(conn, alerte, releve):
                    maj_Alerte(conn, alerte)        


def verif_alerte(conn, alerte: dict, rel: dict) -> bool:
    """
    Vérifie si l'alerte doit être envoyée

    param conn: Connexion à la base de données
    param alerte: Alerte qui doit être vérifiée
    param rel: Relevé avec lequel l'alerte est vérifiée
    return: True si l'alerte doit être déclenchée, False dans le cas contraire
    """
    seuilDep = False
    dateOk = False
    if rel["hum"] != "":
        if alerte["ope"] == ">":
            if alerte["type"] == "Température" and rel["temp"] > alerte["niv"]:
                seuilDep = True
            elif alerte["type"] == "Humidité" and float(rel["hum"]) > alerte["niv"]:
                seuilDep = True
        else:
            if alerte["type"] == "Température" and rel["temp"] < alerte["niv"]:
                seuilDep = True
            elif alerte["type"] == "Humidité" and float(rel["hum"]) < alerte["niv"]:
                seuilDep = True
        # Si le seuil d'alerte a été dépassé
        if seuilDep:
            # Si la date de dernier envoi est vide
            if alerte["d_envoi"] == None:
                dateOk = True
            # Sinon, calcule si l'intervalle est dépassé
            else:
                dateOk = verif_delai(conn, alerte)
            # Si le seuil est dépassé ainsi que l'intervalle
            if dateOk == True:
                return True
    # Sinon
    return False


def verif_delai(conn, alerte: dict) -> bool:
    """
    Vérifie le délai entre le dernier envoi et la date/heure actuelle

    param conn: Connexion à la base de données
    param alerte: Alerte pour laquelle il faut vérifier si le délai d'attente est dépassé
    return: True si le délai d'attente est dépassé, False dans le cas contraire
    """
    d_envoi = alerte["d_envoi"]
    date = d_envoi + timedelta(hours=int(alerte["freq"]))
    maintenant = datetime.now()
    if maintenant > date:
        return True
    else:
        return False


def envoiMail(conn, alerte: dict, releve: dict) -> bool:
    """
    Envoi le mail à l'utilisateur

    param conn: Connexion à la base de données
    param alerte: Alerte qui a été déclenchée
    param releve: Relevé ayant levé l'alerte
    return: True si l'email a été envoyé, False dans le cas contraire 
    """
    # Récupère les infos de l'utilisateur
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM utilisateur WHERE idUtilisateur = {alerte["idUser"]}")
    util = cursor.fetchone()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT Nom FROM sonde WHERE idSonde = {releve["idSonde"]}")
    nomSonde = cursor.fetchone()[0]
    cursor.close()
    # Création du message
    if alerte["ope"] == ">":
        operateur = "supérieure"
    elif alerte["ope"] == "<":
        operateur = "inférieure"
    if alerte["type"] == "Température":
        unite = "°C"
        valeur = releve["temp"]
    else:
        unite = "%"
        valeur = releve["hum"]
    date = releve["date"].split(' ')
    message = (
        f"Bonjour {util[1]} {util[2]},\n\n"
        f"La sonde n°{releve["idSonde"]} ({nomSonde}) a détecté une {alerte["type"].lower()} {operateur} à {alerte["niv"]}{unite} ({valeur}{unite}) "
        f"le {date[0]} à {date[1]}.\n\n"
        f"Votre service alerte."
               )
    # Création de la session SMTP
    # Informations du compte Gmail
    sender_email = util[4]
    sender_password = util[8]

    # Adresse e-mail du destinataire
    recipient_email = util[4]

    # Création du message
    subject = f"Alerte de {alerte["type"].lower()} sur la sonde n°{releve["idSonde"]}"
    body = message

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connexion au serveur SMTP de Gmail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            # Authentification
            server.login(sender_email, sender_password)

            # Envoi de l'e-mail
            server.sendmail(sender_email, recipient_email, message.as_string())

        print("E-mail envoyé avec succès.")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Échec de l'authentification. Assurez-vous que l'accès aux applications moins sécurisées est activé.")
        return False
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False


def maj_Alerte(conn, alerte: dict):
    """
    Met à jour la date de dernier envoi de mail d'une alerte dans la base de données

    param conn: Connexion à la base de données
    param alerte: Alerte qui doit être mise à jour dans la base de données
    """
    cursor = conn.cursor()
    req = f"UPDATE alerte SET `dernier_envoi`={datetime.now().strftime("%Y%m%d%H%M%S")} WHERE `idAlerte`=\'{alerte["idAlerte"]}\'"
    cursor.execute(req)
    conn.commit()
    cursor.close()


def recup_liste_alertes(connexion) -> list:
    """
    Récupère la liste des alertes et la retourne
    
    param connexion: Connexion à la BDD
    return: Liste des alertes
    """
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM alerte WHERE Utilisateur_idUtilisateur = 1 ORDER BY Sonde_idSonde")
    records = cursor.fetchall()
    lesAlertes = []
    for record in records:
        cr = connexion.cursor()
        cr.execute(f"SELECT Nom FROM sonde WHERE idSonde = {record[8]}")
        result = cr.fetchone()[0]
        cr.close()
        lesAlertes.append({"id": record[0], "seuil": record[1], "operateur": record[2], "type": record[3], "etat": record[4], "freq": record[6], "sonde": result})
    cursor.close()
    return lesAlertes


def recup_alertes_sonde(conn, sonde: str) -> list[dict]:
    """
    Récupère la liste des alertes actives

    param conn: Connexion à la base de données
    param sonde: id de sonde
    return: Liste des alertes reliées à la sonde passée en paramètre
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT Niv, Operateur, Type, frequence_envoi_mail, dernier_envoi, Utilisateur_idUtilisateur, idAlerte FROM alerte WHERE Active = 1 AND Sonde_idSonde = {sonde}")
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
                "idAlerte": record[6],
            }
        )
    cursor.close()
    return lesAlertes


def trt_chaine(conn, liste_releves: list) -> tuple[list, list]:
    """
    Traite les relevés reçus du Webservice en vue de les stocker dans la base de données
    
    param conn: Connexion à la base de données
    param liste_releves: Liste des relevés reçus du Webservice
    return: Liste des relevés + liste des relevés de sonde à envoyer respectivement dans les tables "releve" et "sonde_has_releve" de la base de données
    """
    # Récupère la liste des sondes
    lesIdSondes = []
    # Stocke les relevés à enregistrer dans la BDD
    lesReleves = []
    # Stocke les releves_has_sonde à enregistrer dans la BDD
    lesRelSonde = []
    listeSondes = recup_sondes(conn)
    for sonde in listeSondes:
        if sonde["statut"] == 1:
            lesIdSondes.append(sonde["id"])
    # Récupère la liste des relevés déjà présents dans la BDD
    anciens_releves = recup_anciens_releves(conn)
    for releve in liste_releves:
        # Si le relevé n'est pas déjà présent dans la BDD, récupère ses infos
        if releve[0] not in anciens_releves:
            # Récupère la date et la convertit dans un format adapté à celui de la BDD
            date = convertit_date(releve[2])
            # Ajoute les données relatives au relevé dans la liste
            lesReleves.append({"id": releve[0], "date": date})
            # Récupère les données du relevé pour chaque sonde présente dans ce relevé
            for sonde in lesIdSondes:
                chaine = releve[1]
                # Cherche si la sonde est présent dans le relevé
                pos = chaine.find(sonde)
                if pos != -1:
                    # Voltage
                    volt = convert_hexa(chaine[pos + 10 : pos + 14]) / 1000
                    # Température
                    temp = convert_hexa(chaine[pos + 16 : pos + 18]) / 10
                    signeTemp = chaine[pos + 14 : pos + 16]
                    temp = float("-" + str(temp)) if signeTemp == "40" else float(temp)
                    # Taux d'humidité
                    humid = convert_hexa(chaine[pos + 18 : pos + 20])
                    humid = "" if humid == 255 else str(humid)
                    # RSSI
                    rssi = "-" + str(convert_hexa(chaine[pos + 20 : pos + 22]))
                    rssi = float(rssi)
                    # Ajoute les données relatives au relevé de sonde dans la liste
                    lesRelSonde.append(
                        {
                            "idSonde": sonde,
                            "idReleve": releve[0],
                            "Temperature": temp,
                            "Humidite": humid,
                            "Niveau_batterie": volt,
                            "rssi": rssi,
                        }
                    )
                    # Affiche dans la console les relevés récupérés
                    print("Sonde n° " + str(chaine[pos : pos + 8]) + " || Relevé n° : " + str(releve[0]) + " || " + str(releve[2]))
                    print("Voltage : " + str(volt) + "V || Température : " + str(temp) + "°C || Humidité : " + humid + "% || RSSI : " + str(rssi) + "dBm\n")
    return lesReleves, lesRelSonde


def lance_procedure_recup(conn):
    """
    Boucle sur la récupération des données auprès du Webservice, l'envoi de ces données vers la BDD à intervalles réguliers et le traitement des alertes

    param conn: Connexion à la base de données
    """
    # Récupère l'utilisateur pour accéder à sa clé account et se connecter au Webservice
    utilisateur = recup_user(conn)

    while True:
        # Récupère les données auprès du WebService à intervalle régulier
        datas = recup_datas_ws(utilisateur["acc_api"])

        # Traite les données récupérées auprès du WebService
        rel, rel_sonde = trt_chaine(conn, datas)

        # Si présence de nouveaux relevés, les envoie vers la base de données
        if len(rel) > 0:
            ajout_releve(conn, rel)
            ajout_releve_sonde(conn, rel_sonde)

        # Gère l'envoi des alertes en cas de seuil dépassé
        # gestion_alerte(conn)

        # Attend 5 minutes et 4 secondes
        time.sleep(60)
