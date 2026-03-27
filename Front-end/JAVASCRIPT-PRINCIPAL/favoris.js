document.addEventListener("DOMContentLoaded", () => {
    const boutons = document.querySelectorAll(".add-fav");

    boutons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");

            if (btn.classList.contains("active")) {
                btn.textContent = "En favoris";
            } else {
                btn.textContent = "Mettre en favoris";
            }
        });
    });
});