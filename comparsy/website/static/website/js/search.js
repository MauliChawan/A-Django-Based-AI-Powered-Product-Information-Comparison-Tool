// search.js — Hybrid Mode (Amazon Real-Time API)

// Open modal when + button clicked
document.getElementById("addProductBtn").addEventListener("click", function () {
    document.getElementById("productSearchModal").classList.remove("hidden");
});

// Close modal
document.getElementById("closeModal").addEventListener("click", function () {
    document.getElementById("productSearchModal").classList.add("hidden");
});

// Search button inside modal
document.getElementById("searchBtn").addEventListener("click", function () {
    let query = document.getElementById("searchInput").value.trim();

    if (query.length === 0) {
        alert("Please enter a product name!");
        return;
    }

    fetchProductFromAPI(query);
});

// Fetch product data from your Django API
function fetchProductFromAPI(query) {
    document.getElementById("searchResults").innerHTML =
        `<p class="text-blue-500">Searching Amazon for "${query}"...</p>`;

    // **FIX 1: Using the correct /api/search/ endpoint**
    fetch(`/api/search/?query=${encodeURIComponent(query)}`)
        .then(res => {
            // **FIX 2: Check for non-200 status before attempting JSON parsing**
            if (!res.ok) {
                // If the status is 502 (API failure) or 500, throw a specific error
                throw new Error(`Server returned status: ${res.status} (${res.statusText})`);
            }
            return res.json();
        })
        .then(data => {
            // **FIX 3: Correctly looking for the "results" key returned by views.py**
            if (data.error || !data.results || data.results.length === 0) {
                const errorMsg = data.error || "No products found.";
                document.getElementById("searchResults").innerHTML =
                    `<p class="text-red-500">Search Failed: ${errorMsg}</p>`;
                return;
            }

            renderSearchResults(data.results);
        })
        .catch(err => {
            console.error("Fetch Error:", err);
            // Display the specific error message, including HTTP status if available
            document.getElementById("searchResults").innerHTML =
                `<p class="text-red-500">Error fetching product data. Details: ${err.message || 'Unknown network error'}</p>`;
        });
}

// Renders product list in modal
function renderSearchResults(results) {
    let container = document.getElementById("searchResults");
    container.innerHTML = "";

    results.forEach((p, index) => {
        let card = document.createElement("div");
        card.className =
            "border p-3 rounded-lg shadow-sm hover:bg-gray-100 cursor-pointer flex gap-4";
        card.innerHTML = `
            <img src="${p.image}" class="w-20 h-20 object-cover rounded">
            <div>
                <h3 class="font-semibold">${p.title}</h3>
                <p class="text-sm text-gray-600">₹${p.price}</p>
                <p class="text-xs text-gray-500">${p.rating} ⭐ (${p.total_ratings} reviews)</p>
            </div>
        `;

        card.addEventListener("click", function () {
            addProductToComparison(p);
            document.getElementById("productSearchModal").classList.add("hidden");
        });

        container.appendChild(card);
    });
}

// Add product to comparing table (max 3)
let compareList = [];

function addProductToComparison(product) {
    if (compareList.length >= 3) {
        alert("You can compare only 3 products at a time.");
        return;
    }

    compareList.push(product);
    updateComparisonTable();
}

// Update full comparison table
function updateComparisonTable() {
    let table = document.getElementById("comparisonTable");
    table.innerHTML = "";

    if (compareList.length === 0) {
        table.innerHTML = "<p class='text-gray-500'>No products added.</p>";
        return;
    }

    let header = `
        <tr>
            <th class="border p-2">Feature</th>
            ${compareList.map(p => `<th class="border p-2">${p.title}</th>`).join("")}
        </tr>
    `;

    let priceRow = `
        <tr>
            <td class="border p-2 font-semibold">Price</td>
            ${compareList.map(p => `<td class="border p-2">₹${p.price}</td>`).join("")}
        </tr>
    `;

    let ratingRow = `
        <tr>
            <td class="border p-2 font-semibold">Rating</td>
            ${compareList.map(p => `<td class="border p-2">${p.rating} ⭐</td>`).join("")}
        </tr>
    `;

    let reviewsRow = `
        <tr>
            <td class="border p-2 font-semibold">Reviews</td>
            ${compareList.map(p => `<td class="border p-2">${p.total_ratings}</td>`).join("")}
        </tr>
    `;

    let specsRow = `
        <tr>
            <td class="border p-2 font-semibold">Specifications</td>
            ${compareList.map(p =>
                `<td class="border p-2 text-sm">${p.specifications || "N/A"}</td>`
            ).join("")}
        </tr>
    `;

    table.innerHTML = `
        <table class="w-full border-collapse">
            ${header}
            ${priceRow}
            ${ratingRow}
            ${reviewsRow}
            ${specsRow}
        </table>
    `;
}