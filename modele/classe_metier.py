class Sonde:
    def __init__(self, id, nom, etat):
        self.id = id
        self.nom = nom
        self.etat = etat
    
    def get_sonde():
        req = "SELECT * FROM sonde WHERE id = {self.id}"
        return req

    def ajout_sonde():
        req = "INSERT INTO sonde (nom, etat) VALUES ({self.nom}, {self.etat})"
        return req

    def maj_sonde():
        req = "UPDATE sonde SET nom = {self.nom}, etat = {self.etat} WHERE id = {self.id}"
        return req


class Releve:
    def __init__(self, id, temp, humid, batt, rssi, date):
        self.id = id
        self.temp = temp
        self.humid = humid
        self.bat = batt
        self.rssi= rssi
        self.date = date
    
    def get_releve():
        req = "SELECT * FROM releve WHERE id = {self.id}"
        return req
    
    def ajout_releve():
        req = "INSERT INTO releve (temp, humid, batt, rssi, date) VALUES ({self.temp}, {self.humid}, {self.batt}, {self.rssi}, {self.date})"
        return req


class alerte:
    def __init__(self, id, niv, operateur, type, actif, idUser, idReleve):
        self.id = id
        self.niv = niv
        self.operateur = operateur
        self.type = type
        self.actif = actif
        self.idUser = idUser
        self.idReleve = idReleve

    def get_alerte():
        req = "SELECT * FROm alerte WHERE id = {self.id}"
        return req

    def ajout_alerte():
        req = "INSERT INTO alerte (niv, operateur, type, actif, idUser, idReleve) VALUES ({self.niv}, {self.operateur}, {self.type}, {self.actif}, {self.idUser}, {self.idReleve})"
        return req
