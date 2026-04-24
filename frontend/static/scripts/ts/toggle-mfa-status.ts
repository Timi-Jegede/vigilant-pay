import { set_mfa_status } from './mfa-status.js';

const mfaToggleLabel = document.getElementById('mfa-toggle-label') as HTMLElement | null;
const mfaElement = document.getElementById('mfa-meta') as HTMLElement | null;

document.addEventListener('DOMContentLoaded', () => {
    const currentStatus: boolean = mfaElement?.dataset.status === 'true';
    localStorage.setItem('currentStatus', JSON.stringify(currentStatus));

    updateMfaToggle(currentStatus);
});

function updateMfaToggle(status) {
    const toggleButton = document.querySelector('#toggle-button') as HTMLElement | null;
    const toggle = document.querySelector('#toggle') as HTMLElement | null;

    toggle?.classList.toggle('!bg-site-toggle-active-color', status);
    toggleButton?.classList.toggle('translate-x-6', status);
}

export async function mfaToggle(event): Promise<void>{
    event.preventDefault();
    
    const currentStatus = JSON.parse(localStorage.getItem('currentStatus')) === 'true';
    const newStatus = !currentStatus;

    try {
        await set_mfa_status({
            url: 'http://127.0.0.1:8000/mfa/mfa-status',
            status: newStatus
        });

        updateMfaToggle(newStatus);

        localStorage.setItem('currentStatus', JSON.stringify(newStatus));

    } catch(error) {
        console.log(error);
    }
}

mfaToggleLabel.addEventListener('click', mfaToggle);