document.addEventListener('DOMContentLoaded', {});


function reinitialiserGraph() {
  let champ = document.getElementById('monChart')
  champ.innerHTML = `<canvas id="myChart" width="400" height="300"></canvas>`
}


function afficherGraphique(type, sonde, nbreleve) {

  // Réinitialise la zone contenant le graphe (efface le graphe précédent)
  reinitialiserGraph()

  let ctx = document.getElementById('myChart').getContext('2d');
  
  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/${sonde}/${nbreleve}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json();
    })
    .then(data => {
      let donnees = []
      let lbl = []
      let unite;
      Object.keys(data).map(releve => {
        if (type === "temperature") {
          donnees.push(data[releve].temp)
          unite = " (°C)"
        }
        else {
          donnees.push(data[releve].humid)
          unite = " (%)"
        }
        lbl.push(data[releve].date)
      }).join('')
      let config = {
        type: 'line',
        data: {
          labels: lbl.reverse(),
          datasets: [{
            label: type.charAt(0).toUpperCase() + type.slice(1) + unite, // Première lettre en majuscule
            data: donnees.reverse(),
            borderColor: type === 'temperature' ? 'rgba(28, 102, 24, 1)' : 'rgba(0, 0, 255, 1)',
            backgroundColor: type === 'temperature' ? 'rgba(26, 205, 0, 1)' : 'rgba(25, 84, 179, 1)',
            borderWidth: 2,
            fill: true,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
      };
      myChart = new Chart(ctx, config);
    })
    .catch(error => {
      console.error('Erreur de la requête:', error);
    }
  );
}


function afficherHistorique(sonde, nbreleve) {

  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/${sonde}/${nbreleve}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json();
    })
    .then(data => {
      // Traiter les données ici
      let elt = document.getElementById('monChart')
      let contenuHistorique = `<div class="divtab">
      <p id="presenttab">Les derniers relevés de la sonde ${data[0].nom}</p>
      <table class="tabdatas">
        <tr>
          <td class="coltitre">Température</td>
          <td class="coltitre">Humidité</td>
          <td class="coltitre">Date du relevé</td>
        </tr>`
      for (let i = 0; i < data.length; i++) {
        let laClasse = "";
        let picto = "static/img/";
        if (data[i].humid === '') {
          laClasse += `class="sanshumid"`
        }
        if (data[i].temp > 25) {
          picto += "soleil.png";
        }
        else if (data[i].temp >= 0) {
          picto += "couvert.png";
        }
        else {
          picto += "neige.png";
        }
        contenuHistorique += `
        <tr class="cell">
        <td><img src="${picto}">${data[i].temp}°C</td>
        <td ${laClasse}>${data[i].humid !== '' ? data[i].humid + '%' : '-</td>'}
        <td>${data[i].date}</td>
      </tr>`
      }
      contenuHistorique += `</table>
    </div>`
      elt.innerHTML = contenuHistorique;
    })
    .catch(error => {
      // Gérer les erreurs ici
      console.error('Erreur de la requête:', error);
    }
  );
}
