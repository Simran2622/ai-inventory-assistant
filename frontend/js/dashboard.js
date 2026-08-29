/*
This file runs on dashboard.html. It:
  1. Fetches the dashboard summary from the backend
  2. Displays the totals in the summary cards
  3. Builds the low-stock table dynamically
  4. Handles the logout link
*/

// Run this as soon as the page loads.
window.addEventListener("DOMContentLoaded", loadDashboard);

async function loadDashboard() {
    const response = await apiRequest("/dashboard/summary");

    if (!response || !response.ok) {
        alert("Failed to load dashboard. Please log in again.");
        return;
    }

    const data = await response.json();

    // Fill in the summary cards.
    document.getElementById("total-products").textContent = data.total_products;
    document.getElementById("total-stock").textContent = data.total_stock_units;
    document.getElementById("low-stock-count").textContent = data.low_stock_count;

    // Build the low-stock table rows.
    const tableBody = document.getElementById("low-stock-table-body");
    tableBody.innerHTML = ""; // clear out any old rows first

    if (data.low_stock_products.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='4'>No low-stock products right now.</td></tr>";
    } else {
        data.low_stock_products.forEach(function (product) {
            const row = document.createElement("tr");
            row.className = "low-stock-row";

            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.category || "-"}</td>
                <td>${product.current_stock}</td>
                <td>${product.minimum_stock_level}</td>
            `;

            tableBody.appendChild(row);
        });
    }
}


// ---------- Logout ----------

document.getElementById("logout-link").addEventListener("click", function (event) {
    event.preventDefault();
    clearToken();
    window.location.href = "index.html";
});