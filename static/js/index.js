// mobile-view menu functionality

const burgerIcon = document.querySelector('#navbarBurger');
const navbarMenu = document.querySelector('#navbarLinks');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
});