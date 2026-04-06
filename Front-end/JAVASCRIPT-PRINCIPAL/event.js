// ==============================
// RÉCUPÉRATION DES ÉLÉMENTS HTML
// ==============================

const openBtn = document.getElementById("openForm");      // bouton pour afficher le formulaire
const formBox = document.getElementById("formBox");       // conteneur du formulaire
const addBtn = document.getElementById("addBtn");         // bouton pour ajouter une ressource
const list = document.getElementById("resourcesList");    // liste des ressources


// ==============================
// AFFICHER / CACHER LE FORMULAIRE
// ==============================

openBtn.addEventListener("click", () => {
    // Ajoute ou enlève la classe "hidden"
    formBox.classList.toggle("hidden");
});


// ==============================
// AJOUTER UNE RESSOURCE
// ==============================

addBtn.addEventListener("click", () => {

    // Récupération des valeurs des champs
    const titre = document.getElementById("titre").value.trim();
    const matiere = document.getElementById("matiere").value.trim();
    const fichierInput = document.getElementById("fichier");
    const fichier = fichierInput.files[0];

    // Vérification des champs
    if (titre === "" || matiere === "" || !fichier) {
        alert("Remplis le titre, la matière et choisis un fichier.");
        return;
    }

    // Récupération du nom du fichier
    const nomFichier = fichier.name;

    // Création de la carte HTML
    const div = document.createElement("div");
    div.className = "mini-card";

    div.innerHTML = `
        <div class="mini-title-row">
            <div class="mini-title">${titre}</div>
        </div>

        <div class="mini-meta">
            <span class="tag tag-green">Nouveau</span>
            <span class="tag tag-blue">${matiere}</span>
            <span class="tag tag-gray">${nomFichier}</span>
        </div>
    `;

    // Ajout en haut de la liste
    list.prepend(div);

    // Réinitialisation du formulaire
    document.getElementById("titre").value = "";
    document.getElementById("matiere").value = "";
    fichierInput.value = "";

    // Masquer le formulaire
    formBox.classList.add("hidden");
});


// ==============================
// DÉCONNEXION
// ==============================

document.getElementById("logoutBtn").addEventListener("click", async () => {
    try {
        // Appel serveur pour la déconnexion
        await fetch("/logout", {
            method: "POST",
            credentials: "include" // nécessaire pour les sessions/cookies
        });

        // Redirection vers la page d'accueil
        window.location.href = "accueil.html";

    } catch (error) {
        console.error("Erreur lors de la déconnexion :", error);
    }
});


// ==============================
// AFFICHER / CACHER LES RÉPONSES
// ==============================

function goToReply() {
    const section = document.getElementById("replySection");

    // Si visible → cacher
    if (section.style.display === "block") {
        section.style.display = "none";
    } 
    // Sinon → afficher
    else {
        section.style.display = "block";

        // Scroll fluide vers la section
        section.scrollIntoView({
            behavior: "smooth"
        });

        // Focus automatique sur le textarea
        const textarea = section.querySelector("textarea");
        if (textarea) {
            textarea.focus();
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".flash-message");

    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transition = "opacity 0.5s ease";

            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 3000); // 3 secondes
    });
});