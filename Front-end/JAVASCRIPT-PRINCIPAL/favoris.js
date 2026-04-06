
document.addEventListener("DOMContentLoaded", () => {

    // On sélectionne tous les boutons "favoris"
    const boutons = document.querySelectorAll(".add-fav");

    // On parcourt chaque bouton
    boutons.forEach(btn => {

        
        btn.addEventListener("click", async () => {

            // On récupère l'ID 
            const questionId = btn.dataset.questionId;
            const resourceId = btn.dataset.resourceId;

            // Si aucun ID trouvé → on arrête
            if (!questionId && !resourceId) return;

            //  On choisit  l'URL 
            const url = questionId
                ? `/questions/${questionId}/favorite`
                : `/resources/${resourceId}/favorite`;

            try {
                //  Envoi de la requête au serveur
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                
                const data = await response.json();

                
                if (!response.ok || !data.success) {
                    alert(data.message || "Erreur lors de l'ajout aux favoris.");
                    return;
                }

                //  Mise à jour visuelle du bouton
                if (data.is_favorite) {
                    btn.classList.add("active"); // bouton actif
                    btn.textContent = "En favoris";
                } else {
                    btn.classList.remove("active"); // bouton inactif
                    btn.textContent = "Mettre en favoris";
                }

            } catch (error) {
                //  erreurs réseau
                console.error("Erreur :", error);
                alert("Une erreur est survenue.");
            }

        });

    });

});