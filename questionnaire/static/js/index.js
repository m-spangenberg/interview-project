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

    // Set empty options to None for consistency
    if (!input_options){
        input_options = 'None';
    }

    // Capitalize input type
    let input_capitalize = input_types[0].toUpperCase() + input_types.slice(1).toLowerCase();
        
    // construct entry
    $entryDiv = $(
        `<div id="x" class="box is-shadowless my-2 mx-2">
        <button id="deleteEntry" class="delete is-medium is-pulled-right"></button>
        <label id="x" class="label">Q: ${question} </label>
        <label id="x" class="label">A: ${input_capitalize}, (${input_options})</label>
        </div>`
    );

    $($entryDiv).insertBefore("#entryCreation");
});


// form-builder -- only enable input options for select and radio in dropdown
$(document).ready(function() {
    $("input[name=entryOptionField]").prop('disabled', true);
});


$(document).on('click', 'select[name=entryInputTypeField]', function() {

    let selectedInputType = $("select[name=entryInputTypeField] option:checked").val();

    if (selectedInputType === 'input') {
        // disable field
        $("input[name=entryOptionField]").prop('disabled', true);
        // clear field
        $("input[name=entryOptionField]").val('');
    } else {
        $("input[name=entryOptionField]").prop('disabled', false);
    }
});

