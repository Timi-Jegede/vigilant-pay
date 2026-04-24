function get_countries() {
    fetch('/terminal/countries-json', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) throw new Error('Error fetching json.')
        return response.json()
    })
    .then(data => {
        if (data.countries) {
            const selectCountry = document.getElementById('location') as HTMLSelectElement;
            data.countries.forEach((country: {name: string}) => {
                const option = document.createElement('option') as HTMLOptionElement;
                option.value = country.name;
                option.textContent = country.name;

                selectCountry.appendChild(option);
            });
        }
    })
    .catch(error => console.error(error))
}

document.addEventListener('DOMContentLoaded', get_countries);