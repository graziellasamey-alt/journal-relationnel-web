// éléments
const openBtn = document.getElementById("openForm");
const formBox = document.getElementById("formBox");
const addBtn = document.getElementById("addBtn");
const list = document.getElementById("resourcesList");

// afficher / cacher le formulaire
openBtn.addEventListener("click", function () {
    formBox.classList.toggle("hidden");
});

// ajouter une ressource
addBtn.addEventListener("click", function () {

    const titre = document.getElementById("titre").value.trim();
    const matiere = document.getElementById("matiere").value.trim();
    const fichierInput = document.getElementById("fichier");
    const fichier = fichierInput.files[0];

    // vérifier les champs
    if (titre === "" || matiere === "" || !fichier) {
        alert("Remplis le titre, la matière et choisis un fichier.");
        return;
    }

    const nomFichier = fichier.name;

    // créer la carte
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

    // ajouter en haut
    list.prepend(div);

    // reset formulaire
    document.getElementById("titre").value = "";
    document.getElementById("matiere").value = "";
    fichierInput.value = "";
    formBox.classList.add("hidden");
});


// déconnexion
document.getElementById("logoutBtn").addEventListener("click", async () => {
  try {
    await fetch("/logout", {
      method: "POST",
      credentials: "include"
    });

    // redirection
    window.location.href = "accueil.html";

  } catch (error) {
    console.error("Erreur lors de la déconnexion :", error);
  }
});


// afficher / cacher les réponses
function goToReply() {
    const section = document.getElementById("replySection");

    if (section.style.display === "block") {
        section.style.display = "none";
    } else {
        section.style.display = "block";

        // scroll vers la section
        section.scrollIntoView({
            behavior: "smooth"
        });

        // focus sur le textarea
        const textarea = section.querySelector("textarea");
        if (textarea) {
            textarea.focus();
        }
    }
}