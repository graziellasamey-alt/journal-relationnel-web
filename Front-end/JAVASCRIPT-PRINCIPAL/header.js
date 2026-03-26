fetch("/Front-end/HTML-PRINCIPAL/header.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("header").innerHTML = data;

        const currentPage = window.location.pathname.split("/").pop();

        const links = document.querySelectorAll(".nav-link");

        links.forEach(link => {
            const href = link.getAttribute("href");

            if (!href) return;

            // nettoyage pour éviter les erreurs
            const cleanHref = href.trim();

            if (cleanHref === currentPage) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    });