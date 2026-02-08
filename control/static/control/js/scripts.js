document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        const target = document.querySelector(targetId);

        if (!target) return;

        e.preventDefault();

        const navHeight = 90;
        const targetPosition = target.offsetTop - navHeight;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 600;
        let start = null;

        function animation(currentTime) {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }

        requestAnimationFrame(animation);

        // Fecha menu mobile
        const nav = document.querySelector('.navbar-collapse');
        if (nav.classList.contains('show')) {
            nav.classList.remove('show');
        }
    });
});

const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".nav-link");

window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 120;
        if (pageYOffset >= sectionTop) {
            current = section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {
        link.classList.remove("active");
        if (link.getAttribute("href") === "#" + current) {
            link.classList.add("active");
        }
    });
});
    // Script para rotação do ícone de seta
        document.addEventListener('DOMContentLoaded', function() {
            var buttons = document.querySelectorAll('.nav-item button[data-bs-toggle="collapse"]');
            buttons.forEach(function(button) {
                var targetId = button.getAttribute('data-bs-target');
                var targetElement = document.querySelector(targetId);
                var icon = button.querySelector('.submenu-icon');

                if (targetElement) {
                    targetElement.addEventListener('show.bs.collapse', function () {
                        if (icon) icon.style.transform = 'rotate(180deg)';
                    });
                    targetElement.addEventListener('hide.bs.collapse', function () {
                        if (icon) icon.style.transform = 'rotate(0deg)';
                    });
                }
            });
        });