import mysql.connector

class Connexion:
    def __init__(self, user, host, database):
        self.user = user
        self.host = host
        self.database = database
        self.conn = None

    def se_connecter(self):
        self.conn = mysql.connector.connect(self.user, self.host, self.database)
        return self.conn
    
    def se_deconnecter(self):
        self.conn.close()


class Capteur:
    def __init__(self, id, nom, etat):
        self.id = id
        self.nom = nom
        self.etat = etat
    
    def get_capteur(self):
        req = f"SELECT * FROM sonde WHERE idSonde = {self.id}"
        return req

    def ajout_capteur(self):
        req = f"INSERT INTO sonde (Nom, Inactif) VALUES ({self.nom}, {self.etat})"
        return req

    def maj_capteur(self):
        req = f"UPDATE sonde SET Nom = {self.nom}, Inactif = {self.etat} WHERE idSonde = {self.id}"
        return req


class Releve:
    def __init__(self, temp, humid, batt, rssi, date, id = ""):
        self.id = id
        self.temp = temp
        self.humid = humid
        self.batt = batt
        self.rssi= rssi
        self.date = date
    
    def get_releve(self):
        if self.id == "":
            print("Pas d'id renseigné pour ce relevé")
            return
        else:
            req = f"SELECT * FROM relevé WHERE idRelevé = {self.id}"
            return req
    
    def ajout_releve(self):
        req = f"INSERT INTO relevé (Température, Humidité, Niveau_batterie, Signal_RSSI, Date_relevé, Sonde_idSonde) VALUES ({self.temp}, {self.humid}, {self.batt}, {self.rssi}, {self.date}, 1)"
        return req


class Alerte:
    def __init__(self, id, niv, operateur, type, actif, idUser, idReleve):
        self.id = id
        self.niv = niv
        self.operateur = operateur
        self.type = type
        self.actif = actif
        self.idUser = idUser
        self.idReleve = idReleve

    def get_alerte(self):
        req = f"SELECT * FROM alerte WHERE id = {self.id}"
        return req

    def ajout_alerte(self):
        req = f"INSERT INTO alerte (Niv, Operateur, Type, Actif, Utilisateur_idUtilisateur, Relevé_idRelevé) VALUES ({self.niv}, {self.operateur}, {self.type}, {self.actif}, {self.idUser}, {self.idReleve})"
        return req

