// Initialize the map and set its view to the center of the Earth (latitude 0, longitude 0)
var map = L.map('map').setView([0, 0], 2);

// Set up the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Array to store markers
var markers = [];

// Handle form submission to add a marker
document.getElementById('marker-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get latitude and longitude from the form
    var lat = parseFloat(document.getElementById('latitude').value);
    var lng = parseFloat(document.getElementById('longitude').value);

    // Validate input
    if (isNaN(lat) || isNaN(lng)) {
        alert('Please enter valid latitude and longitude.');
        return;
    }

    var marker = L.marker([lat, lng], { draggable: true }).addTo(map)
        .bindPopup('Latitude: ' + lat + '<br>Longitude: ' + lng)
        .openPopup();

    // Update the popup content on marker drag
    marker.on('dragend', function(event) {
        var marker = event.target;
        var position = marker.getLatLng();
        marker.setPopupContent('Latitude: ' + position.lat + '<br>Longitude: ' + position.lng);
    });


    // Store marker in the array
    markers.push(marker);

    // Optionally, zoom to the new marker
    map.setView([lat, lng], 10);

    sendCoordinates(markers);
});

function markersToCoordinates(markerList) {
    return markerList.map(marker => {
        var position = marker.getLatLng();
        return { latitude: position.lat, longitude: position.lng };
    });
}

function sendCoordinates(markerList) {
    var coordinates = markersToCoordinates(markerList);
    var temp = JSON.stringify(coordinates);
    console.log(temp);
    fetch('/submit-coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: temp
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        console.log('Success:', data); // Log success data in the console
        // Update the sum displayed on the page
        document.getElementById('lat-sum').textContent = 'Latitude Sum: ' + data.lat_sum;
        document.getElementById('lng-sum').textContent = 'Longitude Sum: ' + data.lng_sum;
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred.');
    });
}
