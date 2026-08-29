/*
This file handles everything on the login/register page (index.html):
  - Switching between the login and register forms
  - Submitting login/register data to the backend
  - Saving the JWT token and redirecting to the dashboard on success
*/

// Grab references to the HTML elements we need to work with.
const loginSection = document.getElementById("login-section");
const registerSection = document.getElementById("register-section");
const showRegisterLink = document.getElementById("show-register");
const showLoginLink = document.getElementById("show-login");

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

const loginMessage = document.getElementById("login-message");
const registerMessage = document.getElementById("register-message");


// ---------- Toggle between login and register forms ----------

showRegisterLink.addEventListener("click", function (event) {
    event.preventDefault(); // stops the link from actually navigating anywhere
    loginSection.style.display = "none";
    registerSection.style.display = "block";
});

showLoginLink.addEventListener("click", function (event) {
    event.preventDefault();
    registerSection.style.display = "none";
    loginSection.style.display = "block";
});


// ---------- Handle login form submission ----------

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault(); // stops the browser from reloading the page

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    // Our backend's /auth/login endpoint expects form data
    // (username + password), not JSON - same as we saw in Swagger.
    const formBody = new URLSearchParams();
    formBody.append("username", email);
    formBody.append("password", password);

    const response = await fetch(API_BASE_URL + "/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formBody,
    });

    if (response.ok) {
        const data = await response.json();
        saveToken(data.access_token);
        window.location.href = "dashboard.html";
    } else {
        loginMessage.textContent = "Incorrect email or password.";
        loginMessage.className = "error-message";
    }
});


// ---------- Handle register form submission ----------

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    // /auth/register expects JSON (unlike /auth/login), so we use
    // apiRequest() here since it already sets the JSON content type.
    const response = await apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email: email, password: password }),
    });

    if (response.ok) {
        registerMessage.textContent = "Account created! You can now log in.";
        registerMessage.className = "success-message";
        registerForm.reset();
    } else {
        const errorData = await response.json();
        registerMessage.textContent = errorData.detail || "Registration failed.";
        registerMessage.className = "error-message";
    }
});