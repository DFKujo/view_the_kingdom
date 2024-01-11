document.addEventListener('DOMContentLoaded', function() {
    // Function to update the category and display statistics
    window.updateCategory = function() {
        var category = document.getElementById('category-select').value;
        fetch(`/get_data/${category}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('stats').innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    document.getElementById('stats').innerHTML = `
                        <h3>Current Count: ${data.current_count}</h3>
                        <p>Change in 24 hours: ${data.change_24h}</p>
                        <p>Change in 7 days: ${data.change_7d}</p>
                        <p>Change in 30 days: ${data.change_30d}</p>
                    `;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('stats').innerHTML = `<p>Error fetching data.</p>`;
            });
    }
});
