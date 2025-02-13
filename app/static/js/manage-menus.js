function deleteMenu(button) {
    const menuId = button.getAttribute("data-menu-id");

    if (!menuId) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Invalid menu ID!",
        });
        return;
    }

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to undo this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!",
    }).then((result) => {
        if (result.isConfirmed) {
            fetch("/delete_menu", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ menu_id: menuId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    Swal.fire({
                        icon: "success",
                        title: "Deleted!",
                        text: "The menu has been deleted.",
                        timer: 2000,
                        showConfirmButton: false
                    }).then(() => {
                        location.reload(); // Reload page to reflect changes
                    });
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Error!",
                        text: data.error || "Failed to delete menu.",
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: "error",
                    title: "Error!",
                    text: "Something went wrong.",
                });
            });
        }
    });
}
function viewMenuItems(button) {
    const menuId = button.getAttribute('data-menu-id');

    if (!menuId) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Invalid menu ID!',
        });
        return;
    }

    fetch('/get_menu_items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ menu_id: menuId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.menu_items) {
            const menuItemsList = document.getElementById('menuItemsList');
            menuItemsList.innerHTML = ''; // Clear previous items

            data.menu_items.forEach(item => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.textContent = `${item.item_name} (${item.category})`;
                menuItemsList.appendChild(listItem);
            });

            const menuItemsModal = new bootstrap.Modal(document.getElementById('menuItemsModal'));
            menuItemsModal.show();
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.error || 'Failed to fetch menu items.',
            });
        }
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Something went wrong.',
        });
    });
}

function openEditModal(button) {
    const menuId = button.getAttribute('data-menu-id');
    fetch(`/get_menu/${menuId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("edit_menu_id").value = data.menu_id;
            document.getElementById("edit_menu_name").value = data.menu_name;
            document.getElementById("edit_menu_description").value = data.description;
            document.getElementById("edit_menu_price").value = data.price;

            const container = document.getElementById("existingMenuItems");
            container.innerHTML = "";

            // Make sure existing_index starts from 0
            data.items.forEach((item, existing_index) => {
                const itemDiv = document.createElement("div");
                itemDiv.classList.add("menu-item");
                itemDiv.innerHTML = `
                    <input type="hidden" name="existing_items[${existing_index}][id]" value="${item.item_id}">
                    <div class="field-container">
                        <label>Item Name</label>
                        <input type="text" name="existing_items[${existing_index}][name]" value="${item.item_name}" required />
                    </div>
                    <div class="field-container">
                        <label>Category</label>
                        <select name="existing_items[${existing_index}][category]" required>
                            <option value="appetizer" ${item.category === "appetizer" ? "selected" : ""}>Appetizer</option>
                            <option value="main" ${item.category === "main" ? "selected" : ""}>Main</option>
                            <option value="drink" ${item.category === "drink" ? "selected" : ""}>Drink</option>
                            <option value="dessert" ${item.category === "dessert" ? "selected" : ""}>Dessert</option>
                            <option value="custom" ${item.category === "custom" ? "selected" : ""}>Custom</option>
                        </select>
                    </div>
                    <button type="button" onclick="removeExistingMenuItem(${item.item_id}, this)">Delete</button>
                `;
                container.appendChild(itemDiv);
            });

            const modal = new bootstrap.Modal(document.getElementById("editMenuModal"));
            modal.show();
        });
}


let itemIndex = 0;  // Use let so it persists across function calls

function addEditMenuItem() {
    const container = document.getElementById("editMenuItemsContainer");

    const itemDiv = document.createElement("div");
    itemDiv.classList.add("menu-item", "new"); // Add class 'new' to distinguish newly added items

    itemDiv.innerHTML = `
        <div class="field-container">
            <label>Item Name</label>
            <input type="text" name="new_items[${itemIndex}][name]" required="" />
        </div>
        <div class="field-container">
            <label>Category</label>
            <select name="new_items[${itemIndex}][category]" required="">
                <option value="appetizer">Appetizer</option>
                <option value="main">Main</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
                <option value="custom">Custom</option>
            </select>
        </div>
        <button type="button" onclick="removeMenuItem(this)">Remove</button>
    `;

    container.appendChild(itemDiv);
    
    itemIndex++;  // Increment the index so the next item gets a different index
}


function removeExistingMenuItem(itemId, button) {
    fetch(`/delete_menu_item/${itemId}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status === 200) {
                button.parentElement.remove();  // Remove the item from the UI
            } else {
                alert(data.message || "Error deleting item");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error deleting item");
        });
}

function removeMenuItem(button) {
    button.parentElement.remove();
}

function submitEditMenu() {
    const form = document.getElementById("editMenuForm");
    const formData = new FormData(form);

    fetch("/edit_menu", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "menu update success") {
            Swal.fire("Success", "Menu updated successfully!", "success").then(() => {
                location.reload();
            });
        } else {
            Swal.fire("Error", data.message, "error");
        }
    })
    .catch(error => {
        Swal.fire("Error", "Something went wrong!", "error");
    });
}


// Handle form submission
document.getElementById("editMenuForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const menuId = formData.get("menu_id");

    fetch(`/edit_menu/${menuId}`, {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire({
                icon: "success",
                title: "Success",
                text: data.message,
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                location.reload(); // Reload the page to reflect changes
            });
        } else {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: data.error || "Failed to update menu.",
            });
        }
    })
    .catch(error => {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Something went wrong.",
        });
    });
});

function addMenuItem() {
    const container = document.getElementById("menuItemsContainer");

    // Count only the non-existing (new) items that were added via the button
    const newItemCount = container.querySelectorAll('.menu-item.new').length;

    const itemIndex = newItemCount; // This will ensure we start from 0 for new items

    const itemDiv = document.createElement("div");
    itemDiv.classList.add("menu-item", "new"); // Mark this as a new item

    itemDiv.innerHTML = `
        <div class="field-container">
            <label>Item Name</label>
            <input type="text" name="menu_items[${itemIndex}][name]" placeholder="Enter Item Name" required />
        </div>
        <div class="field-container">
            <label>Category</label>
            <select name="menu_items[${itemIndex}][category]" required>
                <option value="appetizer">Appetizer</option>
                <option value="main">Main</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
                <option value="custom">Custom</option>
            </select>
        </div>
        <button type="button" onclick="removeMenuItem(this)">Remove</button>
    `;

    container.appendChild(itemDiv);
}

function removeMenuItem(button) {
    const itemDiv = button.closest('.menu-item');
    itemDiv.remove();
}


function submitMenu() {
    const form = document.getElementById("packageForm");
    const formData = new FormData(form);

    fetch("/add_menu", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "menu insertion success") {
            Swal.fire("Success", "Menu added successfully!", "success").then(() => {
                location.reload();
            });
        } else {
            Swal.fire("Error", data.message, "error");
        }
    })
    .catch(error => {
        Swal.fire("Error", "Something went wrong!", "error");
    });
}
