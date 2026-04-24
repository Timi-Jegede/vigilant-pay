function get_countries() {
    fetch('/terminal/countries-json', {
        method: 'GET'
    })
        .then(function (response) {
        if (!response.ok)
            throw new Error('Error fetching json.');
        return response.json();
    })
        .then(function (data) {
        if (data.countries) {
            const countriesArray = typeof data.countries === 'string'
                ? JSON.parse(data.countries)
                : data.countries;

            var selectCountry_1 = document.getElementById('location');
            countriesArray.forEach(function (country) {
                var option = document.createElement('option');
                option.classList.add('text-black');
                option.value = country.name;
                option.textContent = country.name;
                selectCountry_1.appendChild(option);
            });
        }
    })
        .catch(function (error) { return console.error(error); });
}
document.addEventListener('DOMContentLoaded', get_countries);
