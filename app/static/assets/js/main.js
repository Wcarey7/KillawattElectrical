////////////////////////////////////////////////////////////////////////////////////////////////////
// Edit - Close - Save - Cancel buttons within the customer summary page
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


$(document).on('click', '.saveButton', function(event) {
    event.preventDefault();

    let otherPhoneFieldRemoved = false;
    let otherEmailFieldRemoved = false;
    let deleteOtherContactInfo = false;

    // Check if "other_phone" input is empty, remove if empty
    let otherPhoneInput = document.getElementById('otherPhone');
    if (otherPhoneInput && otherPhoneInput.value.trim() === '') {
        otherPhoneInput.parentNode.parentNode.parentNode.remove();
        otherPhoneFieldRemoved = true;
    }

    // Check if "other_email" input is empty, remove if empty
    let otherEmailInput = document.getElementById('otherEmail');
    if (otherEmailInput && otherEmailInput.value.trim() === '') {
        otherEmailInput.parentNode.parentNode.parentNode.remove();
        otherEmailFieldRemoved = true;
    }

    let isValid = validateForm();
    if (isValid == true) {
        let formData = $('#editCustomerForm').serialize();
        let otherformData = $('#otherCustomerForm').serialize();

        if (otherformData) {
            formData += '&' + otherformData;
        }

        if (otherPhoneFieldRemoved || otherEmailFieldRemoved) {
            deleteOtherContactInfo = true;
            formData += '&deleteOtherContactInfo=' + deleteOtherContactInfo;

            if (otherPhoneFieldRemoved) {
                let otherPhone = '';
                formData += '&otherPhone=' + otherPhone;
            }
            if (otherEmailFieldRemoved) {
                let otherEmail = '';
                formData += '&otherEmail=' + otherEmail;
            }
        };

        $.ajax({
            method: 'POST',
            url: urlEditCustomer,
            data: formData,
            beforeSend: function(jqXHR) {
                jqXHR.setRequestHeader('X-CSRFToken', csrf_token);
            }
        })
        .done(function(data) {
            if (data.status == '200 OK') {
                // Set True to force reload without cache in Firefox.
                location.reload(true);
                for (const field of fields) {
                    field.disabled = true;
                };
            } else {
                cancelOrClose()
            };
        });
    };
});


$('#closeButton').on('click', function() {
    cancelOrClose()
});


function cancelOrClose() {
    if ($('#closeButton').hasClass('cancelButton')) {
        // Refresh page to get original field values. 
        // Set True to force reload without cache in Firefox.
        location.reload(true);
        for (const field of fields) {
            field.disabled = true;
        }
    } else {
        location.replace(thisRoutePrevPage);
    };
}


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
        let otherCustomerFormUL = document.getElementById('otherCustomerFormUL');
        let selectElement = document.querySelector('#select_to_add');
        let inputFieldValue = selectElement.value;

        // Don't allow the blank option to be selectable.
        if(inputFieldValue == "") {
            return;
        }

        if(inputFieldValue == 'otherPhone') {
            inputFieldName = "other_phone_number";
            inputFieldID = "otherPhone";
            inputFieldLabel = "Other Phone";
            inputFieldType = "tel";
            inputMaxLength = "13";
            inputMinLength = "";
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

        if (otherCustomerFormUL) {
            $(currentElement).before(
                '<li class="list-group-item">' +
                    '<div class="row my-2">' +
                        '<label for=' + `"${inputFieldValue}"` + 'class="col-sm-4 col-form-label">' + 
                            `${inputFieldLabel}` + '</label>' +
                        '<div class="col-sm-8">' +
                            '<input id=' + `"${inputFieldID}"` +  'name=' + `"${inputFieldName}"` +
                                'maxlength=' + `"${inputMaxLength}"` + 'minlength=' + `"${inputMinLength}"` +
                                'type=' + `"${inputFieldType}"` + 'class="form-control">' +
                            '</input>' +
                            '<div class="invalid-feedback">' +
                                'Please provide a valid ' + `${inputFieldValue}` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</li>'
            );

            disableSelectOption(inputFieldValue); // Disable corresponding select option.
        }
        selectElement.value = ""; // After a selection is made reset the select field to be blank.
    });

    function disableSelectOption(value) {
        $('#select_to_add option[value="' + value + '"]').prop('disabled', true);
    }

    // Disable select options on page load if corresponding input fields already exist.
    $('#otherCustomerForm input').each(function() {
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
            } else {
                location.reload();
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
// Parenthesis dashes are removed when committed to the DB via an event attribute in the Model.
////////////////////////////////////////////////////////////////////////////////////////////////////
function formatPhoneNumber(input, event) {
    if (input.value !== '') {
        let numKey = input.value.replace(/\D/g, ''); // Remove non-numeric characters

        // Do nothing if backspace, left and right arrow keys are pressed.
        if(event.which != 8 && event.which != 37 && event.which != 39) {
            let formattedNumber = '(' + numKey.substring(0, 3) + ')' + numKey.substring(3, 6) + '-' + numKey.substring(6, 10);
            input.value = formattedNumber;
        }
    }
}

// Event listener for input event to format phone number
$(document).on('keyup change', 'input[type="tel"]', function(event) {
    formatPhoneNumber(this, event);
    phoneNumberValidate();
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Format phone number when input field is pre-filled with data: (XXX)XXX-XXXX
// When retrieved from the DB phone numbers don't have Parenthesis and dashes.
////////////////////////////////////////////////////////////////////////////////////////////////////
(function () {
    if(document.getElementsByTagName('tel')) {
        const typeTels = $('input[type="tel"]');
        for (const typeTel of typeTels) {
            const phoneNum = typeTel.value.trim();
            if (typeTel.value.trim() !== '') {
                const phoneNumFormatted = phoneNum.replace(/(\d{3})(\d{3})(\d{4})/, '($1)$2-$3');
                typeTel.value = phoneNumFormatted;
            }
        }
    }
})();

// Event listener for blur event to validate phone number
$(document).on('blur', 'input[type="tel"]', function() {
    phoneNumberValidate();
});
