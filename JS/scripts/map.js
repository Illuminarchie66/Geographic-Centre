import {Point} from './point.js';

const map = L.map('map').setView([0, 0], 2);

// Set up the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Array to store markers
const markers = [];

// Geocoder for converting addresses to coordinates
const geocoder = L.Control.Geocoder.nominatim();

export {map,markers,geocoder};