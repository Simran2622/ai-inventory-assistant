/*
This file runs on products.html. It:
  1. Fetches and displays all products in a table
  2. Handles adding a new product
  3. Handles deleting a product
  4. Handles recording a sale for a product
  5. Handles fetching and displaying the AI insight for a product
*/

window.addEventListener("DOMContentLoaded", loadProducts);


// ---------- Load and display all products ----------

async function loadProducts() {
    const response = await apiRequest("/products");

    if (!response || !response.ok) {
        alert("Failed to load products.");
        return;
    }

    const products = await response.json();
    const tableBody = document.getElementById("products-table-body");
    tableBody.innerHTML = "";

    if (products.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='6'>No products yet. Add one above.</td></tr>";
        return;
    }

    products.forEach(function (product) {
        const row = document.createElement("tr");

        if (product.current_stock <= product.minimum_stock_level) {
            row.className = "low-stock-row";
        }

        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.category || "-"}</td>
            <td>${product.current_stock}</td>
            <td>${product.minimum_stock_level}</td>
            <td>${product.supplier_lead_time_days}</td>
            <td>
                <button class="btn-small btn-insight" onclick="showInsight(${product.id})">AI Insight</button>
                <button class="btn-small btn-edit" onclick="recordSale(${product.id})">Record Sale</button>
                <button class="btn-small btn-delete" onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        `;

        tableBody.appendChild(row);

        // This row will hold the AI insight text when requested - starts empty/hidden.
        const insightRow = document.createElement("tr");
        insightRow.id = `insight-row-${product.id}`;
        insightRow.innerHTML = `<td colspan="6"><div class="insight-box" id="insight-box-${product.id}"></div></td>`;
        tableBody.appendChild(insightRow);
    });
}


// ---------- Add a new product ----------

document.getElementById("add-product-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const newProduct = {
        name: document.getElementById("new-name").value,
        category: document.getElementById("new-category").value || null,
        current_stock: parseInt(document.getElementById("new-stock").value),
        minimum_stock_level: parseInt(document.getElementById("new-min-level").value),
        supplier_lead_time_days: parseInt(document.getElementById("new-lead-time").value),
    };

    const response = await apiRequest("/products", {
        method: "POST",
        body: JSON.stringify(newProduct),
    });

    const messageEl = document.getElementById("add-product-message");

    if (response.ok) {
        messageEl.textContent = "Product added successfully.";
        messageEl.className = "success-message";
        document.getElementById("add-product-form").reset();
        loadProducts(); // refresh the table to show the new product
    } else {
        messageEl.textContent = "Failed to add product.";
        messageEl.className = "error-message";
    }
});


// ---------- Delete a product ----------

async function deleteProduct(productId) {
    const confirmed = confirm("Are you sure you want to delete this product?");
    if (!confirmed) {
        return;
    }

    const response = await apiRequest(`/products/${productId}`, {
        method: "DELETE",
    });

    if (response.ok) {
        loadProducts(); // refresh the table
    } else {
        alert("Failed to delete product.");
    }
}


// ---------- Record a sale ----------

async function recordSale(productId) {
    const quantity = prompt("How many units were sold?");
    if (!quantity) {
        return;
    }

    const date = prompt("What date? (YYYY-MM-DD)", new Date().toISOString().split("T")[0]);
    if (!date) {
        return;
    }

    const response = await apiRequest(`/products/${productId}/sales`, {
        method: "POST",
        body: JSON.stringify({
            quantity_sold: parseInt(quantity),
            sale_date: date,
        }),
    });

    if (response.ok) {
        alert("Sale recorded successfully.");
    } else {
        alert("Failed to record sale.");
    }
}


// ---------- Show AI insight for a product ----------

async function showInsight(productId) {
    const box = document.getElementById(`insight-box-${productId}`);

    box.classList.add("visible");
    box.innerHTML = "Loading insight...";

    const response = await apiRequest(`/products/${productId}/insight`);

    if (!response || !response.ok) {
        box.innerHTML = "Could not load AI insight for this product.";
        return;
    }

    const data = await response.json();

    box.innerHTML = `
        <strong>Average daily sales:</strong> ${data.average_daily_sales} units/day<br>
        <strong>Trend:</strong> ${data.trend}<br>
        <strong>Predicted demand (next ${data.supplier_lead_time_days} days):</strong> ${data.predicted_demand} units<br>
        <strong>Low stock:</strong> ${data.is_low_stock ? "Yes" : "No"}<br><br>
        <strong>AI Recommendation:</strong><br>
        ${data.ai_recommendation}
    `;
}


// ---------- Logout ----------

document.getElementById("logout-link").addEventListener("click", function (event) {
    event.preventDefault();
    clearToken();
    window.location.href = "index.html";
});