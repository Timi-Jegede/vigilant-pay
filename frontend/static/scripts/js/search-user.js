document.querySelector('#search-user').addEventListener('click', () => {
    const searchedUser = document.querySelector('input[placeholder="Search user"]').value;
    fetch(`dashboard/search-user/?q=${searchedUser}`)
    .then(response => {
        if (!response.ok) console.log('error');
        return response.json()
    })
    .then (data => {
        console.log(data)
    })
})
