import {Point} from './point.js';
import {geocoder} from './map.js';
import {addBaseMarker} from './markers.js'

document.getElementById('latlng-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const lat = parseFloat(document.getElementById('latitude').value);
    const lng = parseFloat(document.getElementById('longitude').value);

    if (isNaN(lat) || isNaN(lng)) {
        alert('Please enter valid latitude and longitude.');
        return;
    }

    addBaseMarker(new Point({latitude: lat, longitude: lng}));
});

document.getElementById('address-form')
    .addEventListener('submit', async function(event) {

    event.preventDefault();

    const address = document.getElementById('address').value;

    try {
        const results = await geocoder.geocode(address);

        if (results && results.length > 0) {
            const latLng = results[0].center;

            addBaseMarker(
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

document.addEventListener("DOMContentLoaded", function () {

    const tabLinks = document.querySelectorAll(".tablinks");
    const tabContents = document.querySelectorAll(".tabcontent");

    function openTab(tabName, clickedButton) {

        tabContents.forEach(tab => {
            tab.style.display = "none";
        });

        tabLinks.forEach(btn => {
            btn.classList.remove("active");
        });

        document.getElementById(tabName).style.display = "block";
        clickedButton.classList.add("active");
    }

    tabLinks.forEach(button => {
        if (button.dataset.tab == 'InfoTab') {
            openTab('InfoTab', button);
        }

        button.addEventListener("click", function () {
            const tabName = this.dataset.tab;
            openTab(tabName, this);
        });
    });


});