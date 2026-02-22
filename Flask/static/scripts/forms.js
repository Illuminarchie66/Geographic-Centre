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
