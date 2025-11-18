// ---------------------------
// Modal Open/Close
// ---------------------------
document.getElementById("addProductBtn").addEventListener("click", () => {
    document.getElementById("productSearchModal").classList.remove("hidden");
});

document.getElementById("closeModal").addEventListener("click", () => {
    document.getElementById("productSearchModal").classList.add("hidden");
});


// ---------------------------
// Search button
// ---------------------------
document.getElementById("searchBtn").addEventListener("click", () => {
    let query = document.getElementById("searchInput").value.trim();

    if (!query) {
        alert("Enter a product name.");
        return;
    }

    fetchProducts(query);
});


// ---------------------------
// Fetch data from Django API
// ---------------------------
function fetchProducts(query) {
    const resultsBox = document.getElementById("searchResults");
    resultsBox.innerHTML = `<p class="text-blue-500">Searching for "${query}"...</p>`;

    fetch(`/api/search/?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);

            // MUST match key "results"
            if (!data.results || data.results.length === 0) {
                resultsBox.innerHTML = `<p class="text-red-500">No results found.</p>`;
                return;
            }

            renderResults(data.results);
        })
        .catch(error => {
            console.error("Fetch error:", error);
            resultsBox.innerHTML = `<p class="text-red-500">Error fetching results.</p>`;
        });
}


// ---------------------------
// Render Amazon Results
// ---------------------------
function renderResults(products) {
    let box = document.getElementById("searchResults");
    box.innerHTML = "";

    products.forEach(product => {
        let item = document.createElement("div");
        item.className =
            "border p-3 rounded-lg shadow-sm hover:bg-gray-100 cursor-pointer flex gap-4";

        item.innerHTML = `
            <img src="${product.image}" class="w-20 h-20 object-cover rounded">
            <div>
                <h3 class="font-semibold">${product.title}</h3>
                <p class="text-sm text-gray-600">₹${product.price}</p>
                <p class="text-xs text-gray-500">${product.rating} ⭐ (${product.total_ratings})</p>
            </div>
        `;

        item.addEventListener("click", () => {
            addProductToComparison(product);
            document.getElementById("productSearchModal").classList.add("hidden");
        });

        box.appendChild(item);
    });
}


// ---------------------------
// Comparison List
// ---------------------------
let compareList = [];

// Add product
function addProductToComparison(product) {
    if (compareList.length >= 3) {
        alert("Max 3 products allowed.");
        return;
    }

    compareList.push(product);
    updateComparisonTable();
}


// ---------------------------
// Update Table
// ---------------------------
function updateComparisonTable() {
    let table = document.getElementById("comparisonTable");

    if (compareList.length === 0) {
        table.innerHTML = "<p class='text-gray-500'>No products added.</p>";
        return;
    }

    table.innerHTML = `
        <table class="w-full border-collapse">
            <tr>
                <th class="border p-2">Feature</th>
                ${compareList.map(p => `<th class="border p-2">${p.title}</th>`).join("")}
            </tr>

            <tr>
                <td class="border p-2 font-semibold">Price</td>
                ${compareList.map(p => `<td class="border p-2">₹${p.price}</td>`).join("")}
            </tr>

            <tr>
                <td class="border p-2 font-semibold">Rating</td>
                ${compareList.map(p => `<td class="border p-2">${p.rating} ⭐</td>`).join("")}
            </tr>

            <tr>
                <td class="border p-2 font-semibold">Reviews</td>
                ${compareList.map(p => `<td class="border p-2">${p.total_ratings}</td>`).join("")}
            </tr>
        </table>
    `;
}
