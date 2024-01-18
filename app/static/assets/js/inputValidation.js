////////////////////////////////////////////////////////////////////////////////////////////////////
// Bootstrap JavaScript styling for disabling form submissions if there are invalid fields.
////////////////////////////////////////////////////////////////////////////////////////////////////
(validateForm = () => {
    'use strict'

    const forms = document.querySelectorAll('.needs-validation')
    let formValid = true;

    // Loop over forms, call validate functions, and prevent submission if needed.
    Array.from(forms).forEach(form => {
        phoneNumberValidate();
        emailValidate();
        usernameValidate();

        if(!form.checkValidity()) {
            formValid = false;
        };
        form.classList.add('was-validated');
    });
    return formValid;
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Validate login and registration forms
////////////////////////////////////////////////////////////////////////////////////////////////////
$('#registerForm, #loginForm').on('submit', function (event) {
    let isValid = validateForm();

    if(isValid == true) {
        return;
    } else {
        event.preventDefault();
    }
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Make sure length of phone number is 13 characters.
////////////////////////////////////////////////////////////////////////////////////////////////////
function phoneNumberValidate() {
    if(!document.getElementById('phoneNumber')) {
        return;
    }

    const phoneNumValidate = document.getElementById('phoneNumber');
    const isValid = phoneNumValidate.value.length === 13;

    if(!isValid) {
        phoneNumValidate.setCustomValidity('Invalid');
        phoneNumValidate.nextElementSibling.textContent = 'Phone Number is too short.';
    } else {
        phoneNumValidate.setCustomValidity('');
    };

    return isValid;
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Make sure length of the username is at least 2 characters.
////////////////////////////////////////////////////////////////////////////////////////////////////
function usernameValidate() {
    if(!document.getElementById('username')) {
        return;
    }

    const username = document.getElementById('username');
    const minLength = 2;
    const isValid = username.value.length === 0 || username.value.length >= minLength;

    if(!isValid) {
        username.setCustomValidity('Invalid');
        username.nextElementSibling.textContent = 'Username is too short';
    } else {
        username.setCustomValidity('');
    };

    return isValid;
}


////////////////////////////////////////////////////////////////////////////////////////////////////
// Make sure the entered email address is a vaild email format
// emailRegExp source: https://www.w3resource.com/javascript/form/email-validation.php
////////////////////////////////////////////////////////////////////////////////////////////////////
function emailValidate() {
    if(!document.getElementById('email')) {
        return;
    }

    const email = document.getElementById('email');

    const emailRegExp =
    /^\w+([\.-\\+]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    const isValid = email.value.length === 0 || emailRegExp.test(email.value);

    if(!isValid) {
        email.setCustomValidity('Invalid');
        email.nextElementSibling.textContent = 'Not a valid email format';
    } else {
        email.setCustomValidity('');
    };

    return isValid;
}

$('#email').on('keyup change', function() {
    emailValidate();
});
