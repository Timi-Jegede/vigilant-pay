function getMfaConfiguredStatus() {
    fetch('/mfa/mfa-configured-status', {
        method: 'GET'  
    })
    .then(response => {
        if (!response.ok) throw new Error('');
        return response.json()
    })
    .then(data => {
        if (data.mfa_configured_status) {
            const configurationStatusElem = document.querySelector('#configuration-status') as HTMLElement;
            configurationStatusElem.innerHTML = `                        
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                </svg>
                                <span class="font-normal text-base-red">Configured</span>`;
        }
    })
    .catch(error => console.error(error))
}