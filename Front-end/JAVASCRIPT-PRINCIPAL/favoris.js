document.addEventListener("DOMContentLoaded", () => {
    const boutons = document.querySelectorAll(".add-fav");

    boutons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const questionId = btn.dataset.questionId;

<<<<<<< HEAD
            if (btn.classList.contains("active")) {
                btn.textContent = "En favori";
            } else {
                btn.textContent = "Mettre en favoris";
=======
            if (!questionId) return;

            try {
                const response = await fetch(`/questions/${questionId}/favorite`, {
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

                if (data.is_favorite) {
                    btn.classList.add("active");
                    btn.textContent = "En favoris";
                } else {
                    btn.classList.remove("active");
                    btn.textContent = "Mettre en favoris";
                }

            } catch (error) {
                console.error("Erreur :", error);
                alert("Une erreur est survenue.");
>>>>>>> 71df4bf (Ajout du systeme de favoris questions)
            }
        });
    });
});