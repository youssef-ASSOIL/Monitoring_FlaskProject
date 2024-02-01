// This function will be called when the dropdown value changes
async function loadDevices() {
    try {
        var selectedType = document.getElementById('deviceType').value;

        if (selectedType === 'iot') {
            // Make an AJAX request to the server to get IoT devices
            const response = await fetch('/get-iot-devices');

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const devices = await response.json(); // Assumes the server responds with JSON
            
            // Find the table body and clear it
            var tableBody = document.getElementById('infoTableBody');
            tableBody.innerHTML = '';
            
            // Populate the table with new rows for each device
            devices.forEach(device => {
                var row = tableBody.insertRow();
                row.insertCell(0).innerText = device.id;
                row.insertCell(1).innerText = device.mac;
                row.insertCell(2).innerText = device.temp;
                row.insertCell(3).innerText = device.datetime;
                row.insertCell(4).innerText = device.latitude;
                row.insertCell(5).innerText = device.longitude;
                // Add more cells as needed
            });
        }
    } catch (error) {
        console.error('Error loading devices:', error);
        // Handle the error as needed, e.g., display an error message to the user
    }
}
loadDevices()
// Add event listener to the dropdown
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('deviceType').addEventListener('change', loadDevices);
});
