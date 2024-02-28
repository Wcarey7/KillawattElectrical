////////////////////////////////////////////////////////////////////////////////////////////////////
// Edit button and close button
////////////////////////////////////////////////////////////////////////////////////////////////////
inputs = document.getElementsByTagName('input');
selects = document.getElementsByTagName('select');

inputsArray = Array.from(inputs);
selectsArray = Array.from(selects);
fields = inputsArray.concat(selectsArray);

cancelButton = document.getElementById('closeButton');
saveButton = document.getElementById('editButton');

urlEditCustomer = $('#editButton').data('edit');
thisRoutePrevPage = $('#closeButton').data('prev');

$('#editButton').on('click', function(event) {
    event.stopPropagation();

    $('#editButton').addClass('saveButton');
    $('#closeButton').addClass('cancelButton');
    $('#state').addClass('form-select');
    $('#select_to_add').addClass('form-select');
    
    cancelButton.textContent = 'Cancel';
    saveButton.textContent = 'Save';

    for (const field of fields) {
        field.disabled = false;
    }

    $('#editButton').off('click');
});


$('#closeButton').on('click', function() {
    if($('#closeButton').hasClass('cancelButton')) {
        // Refresh page to get original field values. 
        // Set True to force reload without cache in Firefox.
        location.reload(true);
        for (const field of fields) {
            field.disabled = true;
        }
    } else {
        location.replace(thisRoutePrevPage);
    };
});


$(document).on('click', '.saveButton', function(event) {
    event.preventDefault();
    let isValid = validateForm();
    // TODO: Create function. if other_phone or other_email input field is empty disable validation and then delete from database and fields.
    if(isValid == true) {
        $.ajax({
            method: 'POST',
            url: urlEditCustomer,
            data: data = $('#editCustomerForm').serialize(),
            beforeSend: function(jqXHR) {
                jqXHR.setRequestHeader('X-CSRFToken', csrf_token);
            }
        })
        .done(function(data) {
            if(data.status == '200 OK') {
                location.reload();
                for (const field of fields) {
                    field.disabled = true;
                }
            };
        });
    };
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Add email and phone input field on customer summary page
////////////////////////////////////////////////////////////////////////////////////////////////////
$(document).ready(function() {
    // The dropdown field is only enabled after the edit button is clicked.
    $('#select_to_add').on('change', function() {
        let inputFieldName;
        let inputFieldLabel;
        let inputFieldID;
        let inputFieldType;
        let inputMaxLength = "255";
        let inputMinLength = "";

        let currentElement = document.getElementById('selectContact');

        let newlistGroupItem = document.createElement('li');
        $(newlistGroupItem).addClass('list-group-item');

        selectElement = document.querySelector('#select_to_add');
        inputFieldValue = selectElement.value;

        if(inputFieldValue == "") {
            return;
        }

        if(inputFieldValue == 'otherPhone') {
            inputFieldName = "other_phone_number";
            inputFieldID = "otherPhone";
            inputFieldLabel = "Other Phone";
            inputFieldType = "tel";
            inputMaxLength = "13";
            inputMinLength = "13";
        } else {
            inputFieldName = "other_email";
            inputFieldID = "otherEmail";
            inputFieldLabel = "Other Email";
            inputFieldType = "email";
        };

        // Check if input field already exists
        let existingInput = document.getElementById(inputFieldID);
        if (existingInput) {
            return;
        }

        $(currentElement).before(newlistGroupItem);
        $(newlistGroupItem).prepend(
            '<div class="row mb-3">' +
                '<label for=' + `"${inputFieldValue}"` + 'class="col-sm-4 col-form-label">' + `${inputFieldLabel}` + '</label>' +
                '<div class="col-sm-8">' +
                    '<input id=' + `"${inputFieldID}"` +  'name=' + `"${inputFieldName}"` +
                        'maxlength=' + `"${inputMaxLength}"` + 'minlength=' + `"${inputMinLength}"` +
                        'type=' + `"${inputFieldType}"` + 'class="form-control" required>' +
                    '</input>' +
                    '<div class="invalid-feedback">' +
                        'Please provide a valid.' + `${inputFieldValue}` +
                    '</div>' +
                '</div>' +
            '</div>'
        );

        selectElement.value = ""; // After a selection is made reset the select field to be blank.
        disableSelectOption(inputFieldValue); // Disable corresponding select option.
    });

    function disableSelectOption(value) {
        $('#select_to_add option[value="' + value + '"]').prop('disabled', true);
    }

    // Disable select options on page load if corresponding input fields already exist
    $('#editCustomerForm input').each(function() {
        let inputFieldID = $(this).attr('id');
        disableSelectOption(inputFieldID);
    });
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Load new customer form in a modal
////////////////////////////////////////////////////////////////////////////////////////////////////
$('#newCustomerBtn').on('click', function () {
    // Route specified in button attribute "data-route".
    const urlNewCustomer = $(this).data('route');

    $.get(urlNewCustomer, function (data) {
        $('#newCustomerModal .modal-content').html(data);
        $('#newCustomerModal').modal('toggle');

        $('#customerFormButton').on('click', function (event) {
            event.preventDefault();
            let isValid = validateForm();

            if(isValid == true) {
                $.post(urlNewCustomer, data = $('#newCustomerModalForm').serialize(), function (data) {
                    if(data.status == '200 OK') {
                        $('#newCustomerModal').modal('hide');
                        location.replace(document.location);
                    };
                });
            };
        });
    });
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Delete customer modal confirmation
////////////////////////////////////////////////////////////////////////////////////////////////////
rowIndex = $('tr').length;

loc = document.location;
originUrl = loc.origin;
currentBaseUrl = originUrl.concat(loc.pathname);
params = new URLSearchParams(loc.search);
currentPage = params.get("page");
pageNum = currentPage-1;
prevPageUrl = `${currentBaseUrl}?page=${pageNum}&search_tag=`;

$('#deleteBtnTD button').on('click', function () {
    // Route specified in button attribute "data-deleting".
    const urlDeleteCustomer = $(this).data('deleting');

    $('#deleteCustomerModalBtn').on('click', function () {
        $.ajax({
            method: 'POST',
            url: urlDeleteCustomer,
            beforeSend: function(jqXHR) {
                jqXHR.setRequestHeader('X-CSRFToken', csrf_token);
            }
        })
        .done(function(data) {
            if(data.status == '200 OK') {
                $('#deleteCustomerModal').modal('hide');
                if(rowIndex == 2 && currentPage >= 2) {
                    location.replace(prevPageUrl);
                }
                else {
                    location.replace(document.location);
                };
            };
        });
    });
}); 


////////////////////////////////////////////////////////////////////////////////////////////////////
// Keep user input text in search field across pages.
////////////////////////////////////////////////////////////////////////////////////////////////////
if(!document.URL.match(/search/) && !document.URL.match(/customer\/\d+/)) {
    sessionStorage.removeItem('searchText');
}
   
savedInputText = sessionStorage.getItem('searchText');
if(searchTagValue = document.getElementById('search_tag')) {
    searchTagValue.value = savedInputText;
};

$('#searchButton').on('click', function () {
    let inputText = document.getElementById('search_tag').value;
    sessionStorage.setItem('searchText', inputText);
});

$('#resetSearchButton').on('click', function () {
    sessionStorage.removeItem('searchText');
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Format phone number as user types: (XXX)XXX-XXXX
////////////////////////////////////////////////////////////////////////////////////////////////////
$(document).on('keyup change', 'input[type="tel"]', function(event) {
    const typeTels = $('input[type="tel"]');
    
    for (const typeTel of typeTels) {
        // '/\D/' Matches any character that is not a digit.
        // 'g' global match modifier. Finds all matches not just the first.
        let numKey = $(typeTel).val().replace(/\D/g,''); 

        // Do nothing if backspace, left and right arrow keys are pressed.
        if(event.which != 8 && event.which != 37 && event.which != 39) {
            $(typeTel).val('(' + numKey.substring(0,3) + ')' + numKey.substring(3,6) + '-' + numKey.substring(6,10));
        };
    phoneNumberValidate();
    }
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Format phone number when input field is pre-filled with data: (XXX)XXX-XXXX
////////////////////////////////////////////////////////////////////////////////////////////////////
(function () {
    if(document.getElementsByTagName('tel')) {
        const typeTels = $('input[type="tel"]');
        for (const typeTel of typeTels) {
            const phoneNum = typeTel.value;
            const phoneNumFormatted = phoneNum.replace(/(\d{3})(\d{3})(\d{4})/, '($1)$2-$3');
            typeTel.value = phoneNumFormatted;
        }
    }
})();
