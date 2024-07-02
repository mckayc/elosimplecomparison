// script.js

// Function to add new item input fields
function addItemField() {
    const itemInputs = document.getElementById('itemInputs');
    const newItemInput = document.createElement('input');
    newItemInput.type = 'text';
    newItemInput.name = 'items[]';
    newItemInput.placeholder = 'Enter item';
    newItemInput.required = true;
    itemInputs.appendChild(newItemInput);
}

// Add event listener for the "Add Item" button
document.addEventListener('DOMContentLoaded', function() {
    const addItemButton = document.querySelector('button[type="button"]');
    if (addItemButton) {
        addItemButton.addEventListener('click', addItemField);
    }
});
