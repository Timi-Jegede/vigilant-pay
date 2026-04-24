function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function verifyMfa() {
    var verificationBox = document.querySelector('#verification-code');
    var verificationCode = verificationBox.value;
    var csrftoken = getCookie('csrftoken');
    fetch('/mfa/complete-mfa-setup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken || '',
        },
        body: JSON.stringify({ verificationCode: verificationCode }),
    })
        .then(function (response) {
        if (!response.ok)
            throw new Error('Verification failed');
        return response.json();
    })
        .then(function (data) {
        if (data.settings) {
            window.location.href = data.settings;
        }
        else if (data.message) {
            var verificationMessage = document.getElementById('verification-message');
            verificationMessage.textContent = data.message;
        }
    })
        .catch(function (error) { return console.error('Error:', error); });
}
var verifyButton = document.querySelector('#verify-button');
verifyButton.addEventListener('click', verifyMfa);
