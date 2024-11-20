document.getElementById("signupForm").addEventListener("submit",async function(event) {
    event.preventDefault();

    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const address = document.getElementById("address").value.trim();
    const phoneNumber =document.getElementById("phoneNumber").value.trim();

     // Basic validation
     if (firstName === "" || lastName === "" || email === "" || password === "" || address === "") {
        document.getElementById("errorMessage").textContent = "All fields are required.";
        return;
    }
    if (!validatePassword(password)) {
        alert('Password must be at least 10 characters long and include at least 1 uppercase letter, 1 number, and 1 symbol(@$!%*?&#).');
        return;
    }

    if (!validatePhoneNumber(phoneNumber)) {
        alert('Invalid phone number');
        return;
    }


    checkEmailExists(email).then(function(emailExists) {
        if (emailExists) {
            alert('User already exists with the same email, please use another email.');
        } else {
            // If everything is okay, submit the form
            document.getElementById('signupForm').submit();
        }
    }).catch(function(error) {
        console.error('Error checking email:', error);
    });


    function validatePassword(password) {
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{10,}$/;
        return passwordRegex.test(password);
    }

    function validatePhoneNumber(phoneNumber) {
        const phoneRegex = /^[1-9]\d{9}$/;
        return phoneRegex.test(phoneNumber);
    }

    function checkEmailExists(email) {
        return new Promise(function(resolve, reject) {
            // Replace with actual API call to your backend to check if email exists
            fetch('/api/check-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                resolve(data.exists); // Assuming the response contains a field `exists` indicating if the email exists
            })
            .catch(error => {
                reject(error);
            });
        });
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/usersignup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name:lastName,
                email:email,
                phone_number:phoneNumber,
                password:password,
                address:address
            })
        });

        if (response.ok) {
            alert('Account Created successfully!');
            window.location.href = 'login.html'
        } else {
            alert('Account Creation failed.');
        }
    } catch (error) {
        console.error('Error:', error);
    }

    // Clear form
    document.getElementById("signupForm").reset();
    document.getElementById("errorMessage").textContent = "";
});
