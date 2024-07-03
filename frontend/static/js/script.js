document.addEventListener('DOMContentLoaded', (event) => {
    let compareForm = document.getElementById('compare-form');
    compareForm.addEventListener('submit', (event) => {
        event.preventDefault();
        let formData = new FormData(compareForm);
        fetch('/compare_items', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    });
});
