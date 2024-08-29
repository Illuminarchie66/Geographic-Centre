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
        map.setView([lat, lng], map.getZoom());
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

function addCentreMarker(lat, lng) {
    // Define a custom red icon
    var redIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });
      
    // Create the marker with the red icon and make it non-draggable
    var centre = L.marker([lat, lng], {
        icon: redIcon,
        draggable: false // Make the marker non-draggable
    }).addTo(map);

    // Optionally, bind a popup to the marker (customize as needed)
    centre.bindPopup(`<b>Latitude:</b> ${lat}<br><b>Longitude:</b> ${lng}`)
        .openPopup();

    centreHold = centre;
}

function refreshMarkers() {
    // Clear markers from the map
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    if (centreHold != null) {
        map.removeLayer(centreHold);
        centreHold = null;
    }
    iterations.forEach(iteration => map.removeLayer(iteration));
    iterations = []
    clearIterations()

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

function addIterationMarker(lat, lng) {
    var greenIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [12.5, 20.5],
        iconAnchor: [6.25, 20.5],
        shadowSize: [20.5, 20.5]
      });
      
    // Create the marker with the red icon and make it non-draggable
    var iteration = L.marker([lat, lng], {
        icon: greenIcon,
        draggable: false // Make the marker non-draggable
    }).addTo(map);

    iterations.push(iteration);
}