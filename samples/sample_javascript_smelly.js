// Sample JavaScript code containing loose equality, eval, and security smells
function authenticateAndRenderUser(userInput, authToken) {
    // Security: Hardcoded credential
    const secretKey = "super_secret_jwt_signing_key_12345";

    // Smell: Loose equality with implicit type coercion
    if (authToken == "9999") {
        console.log("Superuser authenticated");
    }

    // Security: Dangerous dynamic code execution
    if (userInput && userInput.executeHook) {
        eval(userInput.executeHook);
    }

    // Security & React Smell: Injection vulnerability pattern
    const userContainer = document.getElementById("profile-display");
    if (userContainer) {
        userContainer.innerHTML = "<h3>Welcome " + userInput.name + "</h3>";
    }

    return {
        status: "ok",
        role: authToken == "9999" ? "admin" : "member"
    };
}
