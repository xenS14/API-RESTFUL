document.addEventListener('DOMContentLoaded', function () {});


function afficherGraphique(type, sonde, nbreleve) {
  
  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/${sonde}/${nbreleve}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json(); // ou response.text() si la réponse n'est pas JSON
    })
    .then(data => {
      let donnees = []
      let lbl = []
      Object.keys(data).map(releve => {
        if (type === "temperature") {
          donnees.push(data[releve].temp)
        }
        else {
          donnees.push(data[releve].humid)
        }
        lbl.push(data[releve].date)
      }).join('')
      let config = {
        type: 'line',
        data: {
          labels: lbl.reverse(),
          datasets: [{
            label: type.charAt(0).toUpperCase() + type.slice(1), // Première lettre en majuscule
            data: donnees.reverse(),
            borderColor: type === 'temperature' ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            fill: false,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
      };
      let ctx = document.getElementById('myChart').getContext('2d');
      window.myChart = new Chart(ctx, config);
    })
    .catch(error => {
      console.error('Erreur de la requête:', error);
    });

  // if (window.myChart) {
  //   window.myChart.destroy();
  // }

}


function afficherHistorique(sonde) {

  // Effectuer une requête GET avec la Fetch API
  fetch(`http://127.0.0.1:5000/${sonde}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('La requête a échoué avec le statut:' + response.status);
      }
      return response.json(); // ou response.text() si la réponse n'est pas JSON
    })
    .then(data => {
      // Traiter les données ici
      let elt = document.getElementById('monChart')
      elt.innerHTML = `
      <div class="divtab">
        <p id="presenttab">Les derniers relevés de la sonde ${data[0].nom}</p>
        <table class="tabdatas">
          <tr>
            <td class="coltitre">Température</td>
            <td class="coltitre">Humidité</td>
            <td class="coltitre">Date du relevé</td>
          </tr>
          ${Object.keys(data).map(sonde => `
            <tr>
              <td>${data[sonde].temp}°C</td>
              <td>${data[sonde].humid !== '' ? data[sonde].humid + '%' : '-</td>'}
              <td>${data[sonde].date}</td>
            </tr>
          `).join('')}
        </table>
      </div>
    `;
      console.log(data);
    })
    .catch(error => {
      // Gérer les erreurs ici
      console.error('Erreur de la requête:', error);
    });
}
