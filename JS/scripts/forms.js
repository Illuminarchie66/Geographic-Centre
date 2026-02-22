import {Point} from './point.js';
import {geocoder} from './map.js';
import {addMarker} from './markers.js'

document.getElementById('latlng-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get latitude and longitude from the form
    const lat = parseFloat(document.getElementById('latitude').value);
    const lng = parseFloat(document.getElementById('longitude').value);

    // Validate input
    if (isNaN(lat) || isNaN(lng)) {
        alert('Please enter valid latitude and longitude.');
        return;
    }

    addMarker(new Point({latitude: lat, longitude: lng}));
});

// Handle form submission to add a marker by address
document.getElementById('address-form')
    .addEventListener('submit', async function(event) {

    event.preventDefault();

    const address = document.getElementById('address').value;

    try {
        const results = await geocoder.geocode(address);

        if (results && results.length > 0) {
            const latLng = results[0].center;

            addMarker(
                new Point({
                    latitude: latLng.lat,
                    longitude: latLng.lng
                })
            );

        } else {
            alert('Address not found.');
        }

    } catch (err) {
        console.error(err);
        alert('Geocoding failed.');
    }
});
