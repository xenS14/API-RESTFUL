def extract_data(chaine):
    # Récupère l'id de la sonde
    idsonde = chaine[86:94]
    # Récupère la température
    temp = str(int(chaine[102:104], 16))
    if chaine[100:102] == "40":
        temp = "Température : -" + temp[0:2] + "." + temp[2] + "°C"
    else:
        temp = "Température : " + temp[0:2] + "." + temp[2] + "°C"
    print(temp)
    # Récupère le taux d'humidité (si le capteur n'a pas l'id 06182660)
    if idsonde != "06182660":
        humid = str(int(chaine[104:106], 16))
        humid = "Humidité  : " + humid + "%"
        print(humid)
    # Récupère le niveau de batterie

    # Récupère le RSSI
    rssi = str(int(chaine[106:108], 16))
    rssi = "RSSI : -" + rssi + "dBm"
    print(rssi)


chaine = "545A004124240406020400000641884907900004150B0E17263000000008AAC0000001A404B6001900020B62182233000E5600B9384506182660000E1300B7FF3D010637C40D0A"
extract_data(chaine)

"""# Start symbol
"54" = 'T'
"5A" = 'Z'
# Packet length
"00 41" = "65 bytes"
# Protocol type
"24 24" = "$$"
# Hardware type
"04 06" =
# Firmware version
"02 04 00 00" = 2.4
# IMEI
"06 41 88 49 07 90 00 04" = 641884907900004
# RCT Time
"15 0B 0E 17 26 30" = 
# Reserved
"00 00" = 00 00
# Status data length
"00 08" = "8 bytes"
# Alarm type
"AA" = "Interval data"
# Terminal information
"C0"
# Reserved
"00 00"
# Battery voltage
"01 A4"
# Power voltage
"04 B6"
# TAG information data length
"00 19"
# TAG type
"00"
# Number of the TAG
"02"
# Length of per TAG
"0B"
# ID
"62 18 22 33"
# Status
"00"
# Battery voltage
"0E 56"
# Temperature
"00 B9"
# Humidité
"38"
# RSSI
"45"
#06182660000E1300B7FF3D010637C40D0"""

"""temp = chaine[100:104]
humid = chaine[104:106]
print(temp, humid)
print("Température = " + str(int(temp, 16)))
print("Humidité = " + str(int(humid, 16)))"""
