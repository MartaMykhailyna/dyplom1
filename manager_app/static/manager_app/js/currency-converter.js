function changeCurrency(currency) {
    fetch(`/currency/convert/${currency}/`)
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            updatePrices(data.rate, currency);
        } else {
            console.error('Error fetching conversion rate');
        }
    });
}

function updatePrices(rate, currencyCode) {
    const currencySymbols = {
        'UAH': '₴',
        'EUR': '€',
        'USD': '$',
        'GBP': '£'
    };
    const symbol = currencySymbols[currencyCode] || '';

    document.querySelectorAll('.product-price').forEach(elem => {
        const basePrice = parseFloat(elem.getAttribute('data-base-price'));
        elem.innerText = `${symbol}${(basePrice * rate).toFixed(2)}`;
    });
}
