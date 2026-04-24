document.addEventListener('DOMContentLoaded', getMfaConfiguredStatus);

function getMfaConfiguredStatus() {
    fetch('/mfa/mfa-configured-status', {
        method: 'GET'
    })
        .then(function (response) {
        if (!response.ok)
            throw new Error('');
        return response.json();
    })
        .then(function (data) {
        if (data.mfa_configured_status) {
            var configurationStatusElem = document.querySelector('#configuration-status');
            configurationStatusElem.innerHTML = "                        \n                                <svg class=\"w-5 h-5\" fill=\"currentColor\" viewBox=\"0 0 24 24\">\n                                    <path d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\"/>\n                                </svg>\n                                <span class=\"font-normal text-base-red\">Configured</span>";
        }
    })
        .catch(function (error) { return console.error(error); });
}


