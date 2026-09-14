

const navToggle = document.getElementById('navToggle');
const siteNav = document.getElementById('siteNav');
const socialsToggle = document.getElementById('toggle-social');
const socialsCont = document.getElementById('socials');

    function toggleNav() {
        navToggle.classList.toggle('open');
        siteNav.classList.toggle('open');
    }

    function toggleSocials(){
        socialsCont.classList.toggle('open');
    }

    navToggle.addEventListener('click', toggleNav);
    siteNav.addEventListener('click', toggleNav);
    socialsToggle.addEventListener('click', toggleSocials);