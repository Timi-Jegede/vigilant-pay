function getCookie(name: string): string | null {
    let cookieValue: string | null = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}

function verifyMfa() {
    const verificationBox = document.querySelector('#verification-code') as HTMLInputElement;
    const verificationCode = verificationBox.value;
    const csrftoken = getCookie('csrftoken');

    fetch('/mfa/complete-mfa-setup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken || '',
        },
        body: JSON.stringify({verificationCode}),
    })
    .then(response => {
        if (!response.ok) throw new Error('Verification failed');
        return response.json();
    })
    .then(data => {
        if (data.settings) {
            window.location.href = data.settings;
        } else if (data.message) {
            const verificationMessage = document.getElementById('verification-message') as HTMLElement;
            verificationMessage.textContent = data.message;
        }
    })
    .catch(error => console.error('Error:', error));
}

const verifyButton = document.querySelector('#verify-button') as HTMLElement;
verifyButton.addEventListener('click', verifyMfa);