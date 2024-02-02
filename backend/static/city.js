
(function ($) {
    "use strict";


    Chart.defaults.color = "#6C7293";
    Chart.defaults.borderColor = "#000000";


async function fetchDataAndRenderChartc() {
    try {
        const id = $("#id").val(); // Assuming you have jQuery loaded
        console.log("********************",id)
        const response = await fetch('/getCityinfo/'+id);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        
        // Assuming your server responds with JSON data
        const data = await response.json();
        // Process and plot the data
        plotDatac(data);
    } catch (error) { }
}

function plotDatac(data) {
    console.log(data)
    const ctx = document.getElementById('CityTemperatureChartc').getContext('2d');
    

    var myChart1 = new Chart(ctx, {
        type: "line",
        data: {
            labels: data[0].slice(-20),
            datasets: [{
                    label: "date ",
                    data: data[0].slice(-20),
                    backgroundColor: "rgba(235, 22, 22, .7)"
                },
                {
                    label: "temp ",
                    data: data[1].slice(-20),
                    backgroundColor: "rgba(235, 22, 22, .7)"
                }
            
            ]
            },
        options: {
            responsive: true
        }
    });

}

    // Ensure the DOM is ready before calling the function
    $(document).ready(function () {
        fetchDataAndRenderChartc();
    });
    
 
    
})(jQuery);

