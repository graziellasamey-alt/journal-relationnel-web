fetch("/Front-end/HTML-PRINCIPAL/header.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("header").innerHTML = data;

        const currentPath = window.location.pathname;
        const links = document.querySelectorAll(".nav-link");

        links.forEach(link => {
            const href = link.getAttribute("href");

            if (!href || href === "#") return;

            const cleanHref = href.trim();

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