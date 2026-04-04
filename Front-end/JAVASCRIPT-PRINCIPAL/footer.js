// charger le footer
fetch("/Front-end/HTML-PRINCIPAL/footer.html")
  .then(response => response.text())
  .then(data => {

    // insérer dans la page
    document.getElementById("footer").innerHTML = data;

  })
  .catch(error => console.log("Erreur footer :", error));