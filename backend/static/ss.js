document.addEventListener('DOMContentLoaded', function () {
    fetchDataAndRenderChart();
});

async function fetchDataAndRenderChart() {
    try {
        // Fetch the data from your endpoint
        const response = await fetch('/get-temperature-readings');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Assuming your server responds with JSON data
        const data = await response.json();
        
        // Process and plot the data
        plotData(data);
    } catch (error) {
        console.error('Could not fetch data from /iot1dashboard:', error);
    }
}

function plotData(data) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    
    const labels = data.map(entry => new Date(entry[3]).toLocaleTimeString());
    const temperatures = data.map(entry => entry[2]);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperature (°C)',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: temperatures,
                fill: false,
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm'
                        }
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            }
        }
    });
}
