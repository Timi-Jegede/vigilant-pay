import { set_mfa_status } from './mfa-status.js';
const mfaToggleLabel = document.getElementById('mfa-toggle-label');
const mfaElement = document.getElementById('mfa-meta');
document.addEventListener('DOMContentLoaded', () => {
    const currentStatus = mfaElement?.dataset.status === 'true';
    localStorage.setItem('currentStatus', JSON.stringify(currentStatus));
    updateMfaToggle(currentStatus);
});
function updateMfaToggle(status, transition) {
    const toggleButton = document.querySelector('#toggle-button');
    const toggle = document.querySelector('#toggle');
    const mfaTextStatus = document.getElementById('mfa-text-status');

    mfaTextStatus.textContent = status === true ? 'Enabled' : 'Disabled';

    if (transition) {
        const elements = [toggle, toggleButton];
        elements.forEach(elem => elem.classList.add(...transition));
    }

    if (status) {
        toggle.classList.remove('bg-site-toggle-inactive-color');
        toggle.classList.add('bg-site-toggle-active-color');
    } else {
        toggle.classList.remove('bg-site-toggle-active-color');
        toggle.classList.add('bg-site-toggle-inactive-color');  
    }
    toggleButton?.classList.toggle('translate-x-6', status);
}
export async function mfaToggle(event) {
    event.preventDefault();
    const currentStatus = JSON.parse(localStorage.getItem('currentStatus'));
    const newStatus = !currentStatus;
    try {
        await set_mfa_status({
            url: 'http://127.0.0.1:8000/mfa/mfa-status',
            status: newStatus
        });
        updateMfaToggle(newStatus, ['transition', 'duration-300']);
        localStorage.setItem('currentStatus', JSON.stringify(newStatus));
    }
    catch (error) {
        console.log(error);
    }
}
mfaToggleLabel.addEventListener('click', mfaToggle);
