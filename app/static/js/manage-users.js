document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function() {
            const username = this.getAttribute("data-username"); // Get username from data attribute

            if (!confirm(`Are you sure you want to delete user: ${username}?`)) return;

            fetch(`/delete_user/${username}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert(data.message);
                    this.closest("tr").remove(); // Remove the table row
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
