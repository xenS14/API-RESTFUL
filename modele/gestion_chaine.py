from classe_metier import *
import mysql.connector

def extract_data(chaine):
    # Récupère l'id de la sonde
    idsonde = chaine[86:94]
    # Récupère la température
    temp = str(int(chaine[102:104], 16))
    if chaine[100:102] == "40":
        temp = "-" + temp[0:2] + "." + temp[2]
    else:
        temp = temp[0:2] + "." + temp[2]
    temp = float(temp)
    temp = round(temp, 2)
    print("Température :", temp, "°C")
    # Récupère le taux d'humidité (si le capteur n'a pas l'id 06182660)
    if idsonde != "06182660":
        humid = float(int(chaine[104:106], 16))
        print("Humidité : ", humid, "%")
    # Récupère le niveau de batterie
    batterie = float(int(chaine[96:100], 16) / 1000)
    #batt = float(int(chaine[96:100], 16))
    # Récupère le RSSI
    rssi = "-" + str(int(chaine[106:108], 16))
    rssi = float(rssi)
    #rssi = "RSSI : -" + rssi + "dBm"
    print(rssi)
    # Crée une instance de la classe Releve
    leReleve = Releve(temp, humid, batterie, rssi)
    req = leReleve.ajout_releve()
    return req


# Connection à la base de données
conn = mysql.connector.connect(user = 'manu',
                               host = 'localhost',
                              database = 'cubes1')
 


chaine = "545A004124240406020400000641884907900004150B0E17303800000008AAC0000001A404B6001900020B62182233000E5600B8384506182660000E1300B7FF3B01082D2D0D0A"
req = extract_data(chaine)

cursor = conn.cursor()

# Exécution de la requête
cursor.execute(req)

conn.commit()

cursor.close()

# Déconnexion de la base de données
conn.close()

