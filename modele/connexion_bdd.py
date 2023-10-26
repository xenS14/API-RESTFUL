import mysql.connector
import classe_metier

# Connection à la base de données
conn = mysql.connector.connect(user = 'manu',
                               host = 'localhost',
                              database = 'cubes1')
 

cursor = conn.cursor()

# Exécution de la requête
cursor.execute("INSERT INTO sonde(`Nom`, `Inactif`) VALUES (6868686868, 0)")

conn.commit()

cursor.close()

# Déconnexion de la base de données
conn.close()
