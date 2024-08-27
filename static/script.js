// Initialize the map and set its view to the center of the Earth (latitude 0, longitude 0)
var map = L.map('map').setView([0, 0], 2);

// Set up the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Array to store markers
var markers = [];
var current_id = 0;
var centreHold;

// Geocoder for converting addresses to coordinates
var geocoder = L.Control.Geocoder.nominatim();

window.onload = async function() {
    current_id = await fetchCurrentId();
    temp = await fetchMarkers();
    temp.forEach(m => {
        addMarker(m.latitude, m.longitude, m.id);
    });
};

// Handle form submission to add a marker by latitude/longitude
document.getElementById('latlng-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get latitude and longitude from the form
    var lat = parseFloat(document.getElementById('latitude').value);
    var lng = parseFloat(document.getElementById('longitude').value);

    // Validate input
    if (isNaN(lat) || isNaN(lng)) {
        alert('Please enter valid latitude and longitude.');
        return;
    }

    addMarker(lat, lng);
});

// Handle form submission to add a marker by address
document.getElementById('address-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get address from the form
    var address = document.getElementById('address').value;

    geocoder.geocode(address, function(results) {
        if (results && results.length > 0) {
            var latLng = results[0].center;
            addMarker(latLng.lat, latLng.lng);
        } else {
            alert('Address not found.');
        }
    });
});

async function fetchCurrentId() {
    try {
        const response = await fetch('/get-current-id');
        const data = await response.json();
        return data.id;
    } catch (error) {
        console.error('Error fetching current ID:', error);
        return null;
    }
}

async function fetchMarkers() {
    try {
        const response = await fetch('/get-markers');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching markers:', error);
        return null;
    }
}

// Function to add a marker at the current map view center
function addMarkerAtView() {
    var center = map.getCenter();
    addMarker(center.lat, center.lng);
}

// Function to add marker and update UI
function addMarker(lat, lng, id) {
    // Use provided id if it exists, otherwise use current_id
    var markerId = id !== undefined ? id : current_id;

    // Create a marker with a popup that includes the "Delete Marker" button
    var marker = L.marker([lat, lng], { draggable: true, id: markerId }).addTo(map)
        .bindPopup(`<div class="text-container">
                        <b>Latitude:</b> ${lat}<br>
                        <b>Longitude:</b> ${lng}<br>
                        <button data-id="${markerId}" onclick="deleteMarker(this)">Delete Marker</button>
                    </div>`)
        .openPopup();

    // Update the popup content on marker drag
    marker.on('dragend', function(event) {
        var marker = event.target;
        var position = marker.getLatLng();
        marker.setPopupContent(`<div class="text-container">
                                    <b>Latitude:</b> ${position.lat}<br>
                                    <b>Longitude:</b> ${position.lng}<br>
                                    <button data-id="${marker.options.id}" onclick="deleteMarker(this)">Delete Marker</button>
                                </div>`);
        updateMarkerToServer(marker);
        marker.openPopup();
    });

    // Store marker in the array
    markers.push(marker);

    // Conditionally execute based on whether id was provided
    if (id === undefined) {
        addMarkerToServer(marker);
        current_id += 1;

        // Optionally, zoom to the new marker
        map.setView([lat, lng], 10);
    }
}

// Function to delete a marker
function deleteMarker(button) {
    var markerId = Number(button.getAttribute('data-id'));
    var marker = markers.find(m => m.options.id==markerId);

    map.removeLayer(marker);

    markers = markers.filter(m => m !== marker);

    delMarkerToServer(markerId);
}

// Convert marker list to coordinates and send to server
function markerToCoordinates(marker) {
    var position = marker.getLatLng();
    return { latitude: position.lat, longitude: position.lng };
}

function addMarkerToServer(marker) {
    fetch('/add-marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'vertex': markerToCoordinates(marker), 'id': current_id})
    });
}

function delMarkerToServer(markerId) {
    fetch('/del-marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: markerId})
    });
}

function updateMarkerToServer(marker) {
    console.log(marker.options.id);
    fetch('/update-marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'vertex': markerToCoordinates(marker), 'id': marker.options.id})
    });
}

function calculateCenter() {
    fetch('/calculate_centre', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Round the numbers to 8 decimal places
        const latitude = data.vertex.polar.latitude.toFixed(8);
        const longitude = data.vertex.polar.longitude.toFixed(8);
        const variance = data.arcvariance.toFixed(8);
    
        // Format the result to display in the results section
        console.log(data);
    
        if (centreHold != null) {
            map.removeLayer(centreHold);
        }
        console.log(data.arcdistances);
        // Create the result text including the list of distances
        let distancesHtml = '';
        if (data.arcdistances && data.arcdistances.length > 0) {
            distancesHtml = '<br><b>Distances:</b><ul>';
            data.arcdistances.forEach(distance => {
                distancesHtml += `<li>${distance.distance.toFixed(8)}</li>`;
            });
            distancesHtml += '</ul>';
        }
    
        const resultText = `
            <b>Latitude:</b> ${latitude} <br>
            <b>Longitude:</b> ${longitude} <br>
            <b>Variance:</b> ${variance} ${distancesHtml}
        `;
    
        document.getElementById('result').innerHTML = resultText;
        addCentreMarker(latitude, longitude);
    })
    .catch(error => console.error('Error calculating center:', error));
}

// Function to add a non-draggable red marker at the specified latitude and longitude
function addCentreMarker(lat, lng) {
    // Define a custom red icon
    var greenIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });
      
    // Create the marker with the red icon and make it non-draggable
    var centre = L.marker([lat, lng], {
        icon: greenIcon,
        draggable: false // Make the marker non-draggable
    }).addTo(map);

    // Optionally, bind a popup to the marker (customize as needed)
    centre.bindPopup(`<b>Latitude:</b> ${lat}<br><b>Longitude:</b> ${lng}`)
        .openPopup();

    centreHold = centre;
}

// Tab handling
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function refreshMarkers() {
    // Clear markers from the map
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    centreHold = null;

    // Send request to server to clear markers and reset ID
    fetch('/refresh', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            current_id=0;
            // Optionally, you can display a success message to the user
        })
        .catch(error => console.error('Error:', error));
}

// Open the default tab
document.getElementById("defaultOpen").click();
