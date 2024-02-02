
(function ($) {
    "use strict";




   
    // Chart Global Color
    Chart.defaults.color = "#6C7293";
    Chart.defaults.borderColor = "#000000";

    

async function fetchDataAndRenderChart1() {
    try {
        const id = $("#id").val(); // Assuming you have jQuery loaded
    
        const response = await fetch('/get-temperature-readings/'+id);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Assuming your server responds with JSON data
        const data = await response.json();
        console.log("aaaa",data)
        // Process and plot the data
        plotData(data);
    } catch (error) { }
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


function initMap() {
  
}

    // Ensure the DOM is ready before calling the function
    $(document).ready(function () {
        fetchDataAndRenderChart1();
        //initMap()
    });
    
    

})(jQuery);

