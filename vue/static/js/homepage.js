function afficherHistorique(sonde, nbreleve) {

  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/releve/${sonde}/${nbreleve}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json();
    })
    .then(data => {
      // Traiter les données ici
      let elt = document.getElementById('monChart');
      let contenuHistorique;
      if (data.length > 0) {
      contenuHistorique = `<div class="divtab">
      <p id="presenttab">Les ${nbreleve} derniers relevés de la sonde ${data[0].nom}</p>
      <table class="tabdatas">
        <tr>
          <td class="coltitre">Température</td>
          <td class="coltitre">Humidité</td>
          <td class="coltitre">Date du relevé</td>
        </tr>`
      for (let i = 0; i < data.length; i++) {
        let laClasse = "";
        let picto = "static/img/";
        if (data[i].hum === '') {
          laClasse += `class="sanshumid"`
        }
        if (data[i].temp > 25) {
          picto += "soleil.png";
          alt = "Soleil";
        }
        else if (data[i].temp > 9.9) {
          picto += "eclaircies.png";
          alt = "Eclaircies";
        }
        else if (data[i].temp > 0) {
          picto += "couvert.png";
          alt = "Couvert";
        }
          else {
            picto += "neige.png";
            alt = "Eneigé";
          }
          contenuHistorique += `
        <tr class="cell">
        <td><img src="${picto}" alt="${alt}"><br>${data[i].temp}°C</td>
        <td ${laClasse}>${data[i].hum !== '' ? data[i].hum + '%' : '-</td>'}
        <td>${data[i].date}</td>
      </tr>`
        }
        contenuHistorique += `</table>
    </div>`
      }
      else {
        contenuHistorique = `<div class="divtab">
        <p id="presenttab">Il n'y a pas encore de relevés pour cette sonde.</p>
        </div>`
      }
      elt.innerHTML = contenuHistorique;
    })
    .catch(error => {
      // Gérer les erreurs ici
      console.error('Erreur de la requête:', error);
    }
  );
}


function reinitialiserGraph() {
  let champ = document.getElementById('monChart')
  champ.innerHTML = `<canvas id="myChart" width="400" height="480"></canvas>`
}


function afficherGraphique(type, sonde, nbreleve) {

  // Réinitialise la zone contenant le graphe (efface le graphe précédent)
  reinitialiserGraph()

  let ctx = document.getElementById('myChart').getContext('2d');
  
  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/releve/${sonde}/${nbreleve}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json();
    })
    .then(data => {
      if (data.length > 0) {
      let donnees = []
      let lbl = []
      let unite;
      Object.keys(data).map(releve => {
        if (type === "temperature") {
          donnees.push(data[releve].temp)
          unite = " (°C)"
        }
        else {
          donnees.push(data[releve].hum)
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
      }
      else {
        let elt = document.getElementById('monChart');
        let contenuHistorique = `<div class="divtab">
        <p id="presenttab">Il n'y a pas encore de relevés pour cette sonde.</p>
        </div>`
        elt.innerHTML = contenuHistorique;
      }
    })
    .catch(error => {
      console.error('Erreur de la requête:', error);
    }
    );
}