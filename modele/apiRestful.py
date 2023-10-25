from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

releves = [
    {"id": 13873,
     "ch": "545A004124240406020400000641884907900004150B0E173B0500000008AAC0000001A404B7001900020B62182233000E5600B8384406182660000E1300B7FF3C010A5EDC0D0A",
     "date": "Thu, 25 Nov 2021 12:04:00 GMT"}
]

sondes = []


class Releve(Resource):
    def get(self, id):
        for releve in releves:
            if id == releve["id"]:
                return releve, 200
        return "Relevé introuvable", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("ch")
        parser.add_argument("date")
        args = parser.parse_args()

        for releve in releves:
            if id == releve["id"]:
                return "Ce relevé {} existe déjà".format(id), 400

        releve = {
            "id": id,
            "ch": args["ch"],
            "date": args["date"]
        }
        releves.append(releve)
        return releve, 201


class Sonde(Resource):
    def get(self, id):
        for sonde in sondes:
            if id == sonde["id"]:
                return sonde, 200
        return "Sonde introuvable", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("Nom")
        parser.add_argument("etat")
        args = parser.parse_args()

        for sonde in sondes:
            if id == sonde["id"]:
                return "Cette sonde {} existe déjà".format(id), 400

        sonde = {
            "id": id,
            "Nom": args["Nom"],
            "etat": args["etat"]
        }
        releves.append(sonde)
        return sonde, 201
    
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("Nom")
        parser.add_argument("etat")
        args = parser.parse_args()

        for sonde in sondes:
            if (id == sonde["id"]):
                sonde["Nom"] = args["Nom"]
                sonde["etat"] = args["etat"]
                return sonde, 200

        sonde = {
            "id": id,
            "Nom": args["Nom"],
            "etat": args["etat"],
        }
        sondes.append(sonde)
        return sonde, 201


api.add_resource(Releve, "/releve/<int:id>")
api.add_resource(Sonde, "/sonde/<int:id>")
app.run(debug=True)
