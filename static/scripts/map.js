var map = L.map('map').setView([0, 0], 2);

// Set up the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Array to store markers
var markers = [];
var current_id = 0;
var centreHold;
var iterations = [];

// Geocoder for converting addresses to coordinates
var geocoder = L.Control.Geocoder.nominatim();

// Listen for the 'list_updated' event from the serve
