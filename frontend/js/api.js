/*
This file centralizes all communication with our backend.

Every other JS file (auth.js, dashboard.js, products.js) will use the
functions here instead of writing fetch() calls directly - this way,
if our backend URL ever changes (e.g. when we deploy), we only need to
change it in ONE place.
*/

// This is the base address of our backend. Right now it's our local
// server. On Day 6, we'll change this one line to our deployed backend.
const API_BASE_URL = "http://127.0.0.1:8000";


// Saves the JWT token in the browser's storage, so it survives page
// reloads and navigating between pages.
function saveToken(token) {
    localStorage.setItem("access_token", token);
}

// Reads the saved token back out.
function getToken() {
    return localStorage.getItem("access_token");
}

// Removes the token - used when logging out.
function clearToken() {
    localStorage.removeItem("access_token");
}


/*
A single reusable function for making authenticated requests to our
backend. It automatically attaches the JWT token (if one exists) to
the Authorization header, so we don't have to repeat that in every
single fetch() call across the app.
*/
async function apiRequest(endpoint, options = {}) {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
    };

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    const response = await fetch(API_BASE_URL + endpoint, {
        ...options,
        headers: {
            ...headers,
            ...options.headers,
        },
    });

    // If the token is invalid or expired, the backend sends back 401.
    // In that case, we clear the bad token and send the user back to login.
    if (response.status === 401) {
        clearToken();
        window.location.href = "index.html";
        return null;
    }

    return response;
}