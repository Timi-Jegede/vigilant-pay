function user_details() {
    fetch('/user-details', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) throw new Error('Error fetching json');

        return response.json()
    })
    .then(data => {
        const userDetailsElem = document.getElementById('user-details') as HTMLElement;
        userDetailsElem.textContent = data.user_details;
    })
    .catch(error => {
        console.error(error);
    })
}

document.addEventListener('DOMContentLoaded', user_details);