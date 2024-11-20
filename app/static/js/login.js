document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    togglePassword.addEventListener('click', function() {
        // Toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️'; // Change icon based on visibility
    });
});

document.getElementById("loginForm").addEventListener("submit",async function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        const response = await fetch('http://127.0.0.1:5000/userlogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email:email,
                password:password
            })
        });
        if (response.ok) {
            alert('Login successful');
            window.location.href = 'userdashboard.html'
        } else {
            alert('Invalid Credentials');
        }
    } catch (error) {
        console.error('Error:', error);
    }

    // Basic validation
    if (email === "" || password === "") {
        document.getElementById("errorMessage").textContent = "Both fields are required.";
        return;
    }

    // Clear form
    document.getElementById("loginForm").reset();
    document.getElementById("errorMessage").textContent = "";
});
