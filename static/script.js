// script.js

document.addEventListener('DOMContentLoaded', function() {
    window.updateCategory = function() {
        var category = document.getElementById('category-select').value;
        fetch(`/get_data/${category}`)
            .then(response => response.json())
            .then(data => {
                console.log('Category Data:', data); // Debug log
                if (data.error) {
                    document.getElementById('stats').innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    document.getElementById('stats').innerHTML = `
                        <h3>Current Count: ${data.current_count}</h3>
                    `;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('stats').innerHTML = `<p>Error fetching data.</p>`;
            });

        fetchBlockchainData();
    }

function fetchBlockchainData() {
    fetch('/get_balance')
        .then(response => response.json())
        .then(data => {
            console.log('Balance Data:', data); // Debug log

            document.getElementById('harmony-burn-amount').innerText =
                data.formattedHARM ? data.formattedHARM.toFixed(2) : 'N/A';

            document.getElementById('dfkchain-burn-amount').innerText =
                data.totalDFKJ ? data.totalDFKJ.toFixed(2) : 'N/A';

            document.getElementById('klaytn-burn-amount').innerText =
                data.formattedKLAY ? data.formattedKLAY.toFixed(2) : 'N/A';

            document.getElementById('total-burn-amount').innerText =
                data.totalBurn ? data.totalBurn.toFixed(2) : 'N/A';
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('harmony-burn-amount').innerText = 'N/A';
            document.getElementById('dfkchain-burn-amount').innerText = 'N/A';
            document.getElementById('klaytn-burn-amount').innerText = 'N/A';
            document.getElementById('total-burn-amount').innerText = 'N/A';
        });

        fetch('/get_dfkc_amount')
            .then(response => response.json())
            .then(data => {
                console.log('DFKC Amount Data:', data); // Debug log
                document.getElementById('dfkchain-locked-amount').innerText = data.result || 'N/A';
            })
            .catch(error => console.error('Error:', error));

        fetch('/get_klay_locked')
            .then(response => response.json())
            .then(data => {
                console.log('Klay Locked Data:', data); // Debug log
                document.getElementById('klaytn-locked-amount').innerText = data.result || 'N/A';
            })
            .catch(error => console.error('Error:', error));
    }

    window.updateCategory();
});
