////////////////////////////////////////////////////////////////////////////////////////////////////
//              Below are Global 'utility' scripts. Loads in "includes/scripts.html"
///////////////////////////////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////////////////////////////////
// Allow modal to be draggable
////////////////////////////////////////////////////////////////////////////////////////////////////
$('.modal').draggable({
  handle: '.modal-header'
});


////////////////////////////////////////////////////////////////////////////////////////////////////
// Toast notifications
////////////////////////////////////////////////////////////////////////////////////////////////////
const toast = document.getElementById('toastNotify');
const toastNotification = bootstrap.Toast.getOrCreateInstance(toast);
if(toast) {
    toastNotification.show();
}


////////////////////////////////////////////////////////////////////////////////////////////////////
// Set local timezone for the user
////////////////////////////////////////////////////////////////////////////////////////////////////
let originUrl = document.location.origin;

function sendTimezone() {
    let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    fetch(`${originUrl}/user/set_timezone/`, {
        method: 'POST',
        body: new URLSearchParams({ timezone: timezone }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token,
        },
        credentials: "same-origin",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to set timezone');
        }
        console.log('Timezone set successfully');
    })
    .catch(error => {
        console.error('Error setting timezone:', error);
    });
};

// Call the sendTimezone function when the login page loads.
window.onload = function() {
    let loginUrl = `${originUrl}/auth/login/`
    if (window.location.href.indexOf(loginUrl) > -1) {
        sendTimezone();
    }
};
