fetch("/Front-end/HTML-PRINCIPAL/footer.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("footer").innerHTML = data;
  })
  .catch(error => console.log("Erreur footer :", error));