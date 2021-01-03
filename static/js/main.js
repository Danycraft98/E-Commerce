/* Get Country list.*/
function get_country_list(element, current) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const result = JSON.parse(this.responseText);
            Object.keys(result).forEach(function (key) {
                const opt = document.createElement('option');
                opt.value = opt.innerText = result[key].name;
                if (opt.value === current) {
                    opt.setAttribute('selected', '')
                }
                element.appendChild(opt);
            });
        }
    };
    xhttp.open('GET', 'https://restcountries.eu/rest/v2/all', true);
    xhttp.send();
}