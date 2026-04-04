// charger le header
fetch("/Front-end/HTML-PRINCIPAL/header.html")
    .then(response => response.text())
    .then(data => {

        // insérer dans la page
        document.getElementById("header").innerHTML = data;

        const currentPath = window.location.pathname;
        const links = document.querySelectorAll(".nav-link");

        links.forEach(link => {
            const href = link.getAttribute("href");

            if (!href || href === "#") return;

            const cleanHref = href.trim();

            // activer le bon lien
            if (
                currentPath === cleanHref ||
                (cleanHref === "/questions/" && currentPath.startsWith("/questions")) ||
                (cleanHref === "/resources/" && currentPath.startsWith("/resources"))
            ) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    });