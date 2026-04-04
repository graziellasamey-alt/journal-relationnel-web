document.addEventListener("DOMContentLoaded", () => {

    // boutons favoris
    const boutons = document.querySelectorAll(".add-fav");

    boutons.forEach(btn => {

        // clic sur bouton
        btn.addEventListener("click", () => {

            btn.classList.toggle("active");

            // changer le texte
            if (btn.classList.contains("active")) {
                btn.textContent = "En favori";
            } else {
                btn.textContent = "Mettre en favoris";
            }

        });
    });

});