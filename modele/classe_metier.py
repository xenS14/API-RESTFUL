class Sonde:
    def __init__(self, id, nom, etat):
        self.id = id
        self.nom = nom
        self.etat = etat
    
    def get_sonde(self):
        req = f"SELECT * FROM sonde WHERE id = {self.id}"
        return req

    def ajout_sonde(self):
        req = f"INSERT INTO sonde (nom, etat) VALUES ({self.nom}, {self.etat})"
        return req

    def maj_sonde(self):
        req = f"UPDATE sonde SET nom = {self.nom}, etat = {self.etat} WHERE id = {self.id}"
        return req


class Releve:
    def __init__(self, temp, humid, batt, rssi, date = "06-06-2023", id = ""):
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
            req = f"SELECT * FROM relevé WHERE id = {self.id}"
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
        req = f"SELECT * FROm alerte WHERE id = {self.id}"
        return req

    def ajout_alerte(self):
        req = f"INSERT INTO alerte (niv, operateur, type, actif, idUser, idReleve) VALUES ({self.niv}, {self.operateur}, {self.type}, {self.actif}, {self.idUser}, {self.idReleve})"
        return req

