// NOTE:
// This code below is to show I can get by with JavaScript and JQuery,
// but I generally try to keep client side logic to a minimum with something like HTMX.

// form-builder -- delete entry from page
$(document).on('click', '#deleteEntry', function () {
    $(this).find("#deleteEntry");
    }).on('click', '#deleteEntry', function() {
    $(this).parent().remove();
});

// form-builder -- add entry to builder page
$(document).on('click', '#addEntry', function() {

    let question = $("input[name=entryTextField]").val();

    // if the user hasn't entered anything 
    if (!question) {
        return;
    }
    
    let input_options = $("input[name=entryOptionField]").val();
    let input_types = $("select[name=entryInputTypeField] option:checked").val();

    // set empty options to None for consistency
    if (!input_options){
        input_options = 'None';
    }

    // capitalize input type
    let input_capitalize = input_types[0].toUpperCase() + input_types.slice(1).toLowerCase();
        
    // generate meaningful id from existing form content and increment
    let id = parseInt($("div").parent().find('.box').last().prev().attr('id'));

    // when all entries are removed we need to check for NaN
    if (isNaN(id)){
        id = 1;
    } else {
        id++;
    }

    // construct entry
    $entryDiv = $(
        `<div id="${id}" class="box is-shadowless my-2 mx-2">
        <button id="deleteEntry" class="delete is-medium is-pulled-right"></button>
        <label class="label">Q: ${question} </label>
        <input type="hidden" id="question ${id}" name="question ${id}" value="${question}">
        <label class="label">A: ${input_capitalize}, (${input_options})</label>
        <input type="hidden" id="input ${id}" name="input ${id}" value="${input_capitalize}">
        <input type="hidden" id="option ${id}" name="option ${id}" value="${input_options}">
        </div>`
    );

    // clear field
    $("input[name=entryTextField]").val('');

    // insert the new entry below the existing ones
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

// form-builder -- save form to database by making an API call to an endpoint
$(document).on('click', '#saveEntry', function() {

    // construct the form state
    let formstate = [
        {"": ""}
    ]

    // stringify to json and POST with ajax
    $.ajax({
        type: "POST",
        url: "/api/v1/questionnaire/<string:formversion>/add",
        data: JSON.stringify({ formversion: formstate }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){alert(data);},
        error: function(errMsg) {
            alert(errMsg);
        }
    });

});
