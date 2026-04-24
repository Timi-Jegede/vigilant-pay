function user_details() {
    fetch('/user-details', {
        method: 'GET'
    })
        .then(function (response) {
        if (!response.ok)
            throw new Error('Error fetching json');
        return response.json();
    })
        .then(function (data) {
        var userDetailsElem = document.getElementById('user-details');
        userDetailsElem.textContent = data.user_details;
    })
        .catch(function (error) {
        console.error(error);
    });
}
document.addEventListener('DOMContentLoaded', user_details);
