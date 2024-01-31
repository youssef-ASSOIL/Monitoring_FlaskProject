try {
    document.getElementById('toggleaddend').addEventListener('click', function() {
        document.getElementById('addend').style.display =   document.getElementById('addend').style.display == 'block' ? 'none' : 'block';
    });
} catch (error) {
    
}







(function ($) {
    "use strict";


    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
   
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });


   
    // Chart Global Color
    Chart.defaults.color = "#6C7293";
    Chart.defaults.borderColor = "#000000";



    async function fetchDataAndRenderChart() {
        try {
            const id = $("#id").val(); // Assuming you have jQuery loaded
    
            // Fetch the data from your endpoint
            const response = await fetch('/GetInfoEndDevice/' + id);
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            // Assuming your server responds with JSON data
            const data = await response.json();
    
            // Process and plot the data
            console.log(data);
            load(data)
        } catch (error) {
            console.error('Could not fetch data from /GetInfoEndDevice:', error);
        }
    }
    
    // Ensure the DOM is ready before calling the function
    $(document).ready(function () {
        fetchDataAndRenderChart();
    });
    
    
    function load(data) {
        document.getElementById('heredisk').innerText =  data[1][0].diskSize
        document.getElementById('hereram').innerText =  data[1][0].memorySize
        document.getElementById('hereproc').innerText =  data[1][0].processorLoad.length
       
       

        var ctx1 = $("#disk-plot").get(0).getContext("2d");
        var myChart1 = new Chart(ctx1, {
            type: "bar",
            data: {
                labels: data[0].slice(-10),
                datasets: [{
                        label: "Disk Usage",
                        data: data[1].slice(-10).map(e => e.diskUsage),
                        backgroundColor: "rgba(235, 22, 22, .7)"
                    }
                
                ]
                },
            options: {
                responsive: true
            }
        });

        var ctx2 = $("#ram-plot").get(0).getContext("2d");
        var myChart1 = new Chart(ctx2, {
            type: "line",
            data: {
                labels: data[0].slice(-10),
                datasets: [{
                        label: "Memory Usage",
                        data: data[1].slice(-10).map(e => e.memoryUsage),
                        backgroundColor: "rgba(235, 22, 22, .7)"
                    }
                
                ]
                },
            options: {
                responsive: true
            }
        });

        let d = data[1][0].processorLoad.map( (e,index) => ({
            label : "process " + index+1,
            data: data[1].slice(-100).map(e => e.processorLoad[index]),
            backgroundColor: "rgba(235, 22, 22, .7)"
        }))
        console.log(d)
        var ctx3 = $("#proc-plot").get(0).getContext("2d");
        var myChart1 = new Chart(ctx3, {
            type: "line",
            data: {
                labels: data[0].slice(-100),
                datasets: d
                },
            options: {
                responsive: true
            }
        });

     
    }

    

   

    
    
})(jQuery);

