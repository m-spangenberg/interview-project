// mobile-view menu functionality

const burgerIcon = document.querySelector('#navbarBurger');
const navbarMenu = document.querySelector('#navbarLinks');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
});

// form-builder -- delete entry from page

$(document).on('mouseenter', '#deleteEntry', function () {
    $(this).find(":button").show();
}).on('mouseleave', '.divbutton', function () {
    $(this).find(":button").hide();
}).on('click', ':button', function() {
    $(this).parent().remove();
});

// form-builder -- add question to builder page

