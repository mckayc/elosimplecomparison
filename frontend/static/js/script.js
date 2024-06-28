// script.js

function submitMatch(winner, loser) {
    console.log(`Winner: ${winner}, Loser: ${loser}`); // Debug log
    fetch('/submit_match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `winner=${encodeURIComponent(winner)}&loser=${encodeURIComponent(loser)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Match submitted successfully'); // Debug log
            window.location.href = "/compare"; // Navigate to the compare page
        } else {
            console.log('Match submission failed'); // Debug log
        }
    })
    .catch(error => {
        console.error('Error:', error); // Debug log
    });
}
