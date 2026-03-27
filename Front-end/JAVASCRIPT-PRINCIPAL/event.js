const openBtn = document.getElementById("openForm");
const formBox = document.getElementById("formBox");
const addBtn = document.getElementById("addBtn");
const list = document.getElementById("resourcesList");

openBtn.addEventListener("click", function () {
    formBox.classList.toggle("hidden");
});

addBtn.addEventListener("click", function () {
    const titre = document.getElementById("titre").value.trim();
    const matiere = document.getElementById("matiere").value.trim();
    const fichierInput = document.getElementById("fichier");
    const fichier = fichierInput.files[0];

    if (titre === "" || matiere === "" || !fichier) {
        alert("Remplis le titre, la matière et choisis un fichier.");
        return;
    }

    const nomFichier = fichier.name;

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

    list.prepend(div);

    document.getElementById("titre").value = "";
    document.getElementById("matiere").value = "";
    fichierInput.value = "";
    formBox.classList.add("hidden");
});


document.getElementById("logoutBtn").addEventListener("click", async () => {
  try {
    await fetch("/logout", {
      method: "POST",
      credentials: "include"
    });

    // Redirection vers accueil
    window.location.href = "accueil.html";
  } catch (error) {
    console.error("Erreur lors de la déconnexion :", error);
  }
});




// evenement pour ecire les reponses





function goToReply() {
    const section = document.getElementById("replySection");
    if (!section) return;

    // SI caché → afficher
    if (section.style.display === "none" || section.style.display === "") {

        section.style.display = "block";

        // scroll
        section.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        // focus
        const textarea = section.querySelector("textarea");
        if (textarea) {
            textarea.focus();
        }

    } else {
        // SINON → cacher
        section.style.display = "none";
    }
}


// mettre en favoris 