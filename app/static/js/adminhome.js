document.addEventListener("DOMContentLoaded", function() {
    fetchUsers();

    function fetchUsers() {
        fetch('http://127.0.0.1:5000/userdetails')
            .then(response => response.json())
            .then(data => {
                populateUserTable(data.users); // Access the 'users' array
            })
            .catch(error => console.error('Error fetching users:', error));
    }

    function populateUserTable(users) {
        const tableBody = document.querySelector("#userTable tbody");
        tableBody.innerHTML = ""; // Clear any existing rows

        users.forEach((user, index) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${index + 1}</td>
                <td><input type="text" value="${user.first_name}" data-field="first_name" readonly></td>
                <td><input type="text" value="${user.last_name}" data-field="last_name" readonly></td>
                <td><input type="email" value="${user.email}" data-field="email" readonly></td>
                <td><input type="text" value="${user.phone_number}" data-field="phone_number" readonly></td>
                <td><input type="text" value="${user.address}" data-field="address" readonly></td>
                <td>
                    <button class="edit-btn" data-email="${user.email}">Edit</button>
                    <button class="update-btn" data-email="${user.email}" style="display: none;">Save</button>
                    <button class="delete-btn" data-email="${user.email}">Delete</button>
                </td>
            `;

            tableBody.appendChild(row);
        });

        document.querySelectorAll(".edit-btn").forEach(button => {
            button.addEventListener("click", handleEdit);
        });

        document.querySelectorAll(".update-btn").forEach(button => {
            button.addEventListener("click", handleUpdate);
        });

        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", handleDelete);
        });
    }

    function handleEdit(event) {
        const row = event.target.closest("tr");
        const inputs = row.querySelectorAll("input");
        
        inputs.forEach(input => {
            input.removeAttribute("readonly");
        });

        event.target.style.display = "none"; // Hide the Edit button
        row.querySelector(".update-btn").style.display = "inline"; // Show the Save button
    }

    function handleUpdate(event) {
        const email = event.target.getAttribute("data-email");
        const row = event.target.closest("tr");
        const updatedUser = {
            first_name: row.querySelector('input[data-field="first_name"]').value,
            last_name: row.querySelector('input[data-field="last_name"]').value,
            email: email,
            phone_number: row.querySelector('input[data-field="phone_number"]').value,
            address: row.querySelector('input[data-field="address"]').value
        };

        row.querySelectorAll("input").forEach(input => {
            updatedUser[input.getAttribute("data-email")] = input.value;
            input.setAttribute("readonly", true); // Set fields to readonly after update
        });

        fetch(`http://127.0.0.1:5000/updateuser`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedUser)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("User updated successfully!");
                fetchUsers(); // Refresh the user list
            } else {
                alert("Error updating user.");
            }
        })
        .catch(error => console.error('Error updating user:', error))
        .finally(() => {
            // Revert buttons back to initial state
            row.querySelector(".edit-btn").style.display = "inline";
            row.querySelector(".update-btn").style.display = "none";
        });
    }

    function handleDelete(event) {
        const email = event.target.getAttribute("data-email");

        if (confirm("Are you sure you want to delete this user?")) {
            fetch(`http://127.0.0.1:5000/deleteuser`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    fetchUsers(); // Refresh the user list
                } else {
                    alert("Error deleting user.");
                }
            })
            .catch(error => console.error('Error deleting user:', error));
        }
    }
});
