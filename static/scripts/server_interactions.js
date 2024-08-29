function markerToCoordinates(marker) {
    var position = marker.getLatLng();
    return { latitude: position.lat, longitude: position.lng };
}

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

    var settings = getSettings();

    if (centreHold != null) {
        map.removeLayer(centreHold);
    }
    
    console.log('Settings:', settings);

    iterations.forEach(iteration => map.removeLayer(iteration));
    iterations = []
    fetch('/calculate_centre', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ settings: settings, session_id: sessionId }),
    })
    .then(response => response.json())
    .then(data => {
        // Round the numbers to 8 decimal places
        const latitude = data.vertex.polar.latitude.toFixed(8);
        const longitude = data.vertex.polar.longitude.toFixed(8);
        const variance = data.arcvariance.toFixed(4);
    
        // Format the result to display in the results section
        console.log(data);
        
        console.log(data.arcdistances);
        // Create the result text including the list of distances
        let distancesHtml = '';
        let total = 0;
        if (data.arcdistances && data.arcdistances.length > 0) {
            distancesHtml = '<br><b>Distances:</b><ul>';
            data.arcdistances.forEach(distance => {
                distancesHtml += `<li>${distance.distance.toFixed(2)}km</li>`;
                total += distance.distance;
            });
            distancesHtml += '</ul>';
        }
    
        const resultText = `
            <b>Latitude:</b> ${latitude} <br>
            <b>Longitude:</b> ${longitude} <br>
            <b>Total distance:</b> ${total.toFixed(4)}km <br>
            <b>Variance:</b> ${variance} ${distancesHtml}
        `;
    
        document.getElementById('result').innerHTML = resultText;
        addCentreMarker(latitude, longitude);
    })
    .catch(error => console.error('Error calculating center:', error));
}

function clearIterations() {
    fetch('/clear', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => console.error('Error:', error));
}