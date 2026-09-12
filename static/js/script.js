const navToggle = document.getElementById('navToggle');
    const siteNav = document.getElementById('siteNav');

    function toggleNav() {
        navToggle.classList.toggle('open');
        siteNav.classList.toggle('open');
    }

    navToggle.addEventListener('click', toggleNav);
    siteNav.addEventListener('click', toggleNav);