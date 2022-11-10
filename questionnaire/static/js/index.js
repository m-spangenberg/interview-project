// mobile-view menu functionality

const burgerIcon = document.querySelector('#navbarBurger');
const navbarMenu = document.querySelector('#navbarLinks');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
});

// form-builder -- delete entry from page

$(document).on('click', '#deleteEntry', function () {
    $(this).find("#deleteEntry");
    }).on('click', '#deleteEntry', function() {
    $(this).parent().remove();
});

// form-builder -- add entry to builder page

$(document).on('click', '#addEntry', function() {

    let question = $("input[name=entryTextField]").val();
    let input_options = $("input[name=entryOptionField]").val();
    let input_types = $("select[name=entryInputTypeField] option:checked").val();

    $entryDiv = $(
        `<div id="x" class="box is-shadowless my-2 mx-2">
        <button id="deleteEntry" class="delete is-medium is-pulled-right"></button>
        <label id="x" class="label">Q: ${question} </label>
        <label id="x" class="label">A: ${input_types}, (${input_options})</label>
        </div>`
    );

    $($entryDiv).insertBefore("#entryCreation");
});

// form-builder -- only enable input options for select and radio in dropdown

$(document).ready(function() {
    // ensure option field is disabled on load (input is default)
    $("input[name=entryOptionField]").prop('disabled', true);
});


$(document).on('click', 'select[name=entryInputTypeField]', function() {

    let selectedInputType = $("select[name=entryInputTypeField] option:checked").val();

    if (selectedInputType === 'input') {
        $("input[name=entryOptionField]").prop('disabled', true);
    } else {
        $("input[name=entryOptionField]").prop('disabled', false);
    }
});

