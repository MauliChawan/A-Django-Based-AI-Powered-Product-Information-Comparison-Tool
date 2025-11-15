async function searchProducts() {
    const query = document.getElementById("searchBox").value;

    if (!query) return;

    const response = await fetch(`/api/search/?query=${query}`);
    const data = await response.json();

    displayResults(data.results);
}

function displayResults(products) {
    let container = document.getElementById("results");
    container.innerHTML = "";

    products.forEach(p => {
        container.innerHTML += `
            <div class="product-card">
                <img src="${p.image}" />
                <h3>${p.title}</h3>
                <p class="price">${p.price}</p>
                <button onclick="selectProduct('${p.asin}')">Compare</button>
            </div>
        `;
    });
}
