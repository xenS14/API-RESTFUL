from flask import Flask, render_template


def lancer_app(releve: tuple[list, dict]):
    app = Flask(__name__)
    @app.route('/')
    def home():
        return render_template('index.html', title='Accueil', data=releve)
    if __name__ == "vue.affichage_donnees":
        app.run(debug=True)