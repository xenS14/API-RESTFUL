# API_RESTFUL
L'API permet de récupérer des données météorologiques auprès d'un Webservice, de traiter les données reçues de ce webservice, les stocker dans une base de données et, enfin, de les récupérer depuis la base de données pour les afficher dans une interface web.

Depuis l'interface web, différentes routes sont possibles pour récupérer des données :

- GET /sondes --> Récupère la liste des sondes avec leurs caractéristiques.
- GET /sonde/%idsonde% --> Récupère les caractéristiques d'une sonde à partir de l'id renseigné.
- GET /nbreleve/%idsonde% --> Récupère le nombre de relevés enregistré dans la base de données pour la sonde renseignée.
- GET /releve/%idsonde%/%nbreleve% --> Récupère le nombre de relevés renseigné dans l'URL pour la sonde renseignée. Les données sortent dans l'ordre descendant des identifiants de relevé (les si nbreleve = 5, les données reçues correspondront aux 5 plus récentes pour la sonde renseignée).
