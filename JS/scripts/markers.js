import {Point} from './point.js';
import {map} from './map.js';

let markers = [];
let iteration_markers = [];
let centreMarker = null;

function getMarkers() {
    return markers;
}

function addMarker(p, icon=null, draggable=true, initOpen=true) {
    var marker;
    if (icon === null) {
        marker = L.marker([p.polar.degrees.x, p.polar.degrees.y], { draggable: draggable}).addTo(map)
    } else {
        marker = L.marker([p.polar.degrees.x, p.polar.degrees.y], { draggable: draggable, icon:icon}).addTo(map)
    }
    

    marker.point = p;
    updatePopup(marker);

    marker.on('dragend', function (event) {
        const marker = event.target;
        const position = marker.getLatLng();

        marker.point.setLatLng(position.lat, position.lng);

        updatePopup(marker, initOpen);
    });

    return marker;
}

function addBaseMarker(p) {
    var marker = addMarker(p);
    markers.push(marker);
}

function deleteBaseMarker(marker) {
    markers = markers.filter(m => m !== marker);
    map.removeLayer(marker);
}

function addCentreMarker(p) {
    deleteCentreMarker()

    var redIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    
    var marker = addMarker(p, redIcon, false);
    centreMarker = marker;
}

function deleteCentreMarker() {
    if (centreMarker !== null) {
        map.removeLayer(centreMarker);
        centreMarker = null;
    }
}

function addTrackMarker(p) {
    var greenIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [12.5, 20.5],
        iconAnchor: [6.25, 20.5],
        shadowSize: [20.5, 20.5]
    });
    
    var marker = addMarker(p, greenIcon, false, false);
    iteration_markers.push(marker);
}

function deleteTrackMarker(marker) {
    iteration_markers = iteration_markers.filter(m => m !== marker);
    map.removeLayer(marker);
}

function addMarkerAtView() {
    var center = map.getCenter();
    addBaseMarker(new Point({latitude: center.lat, longitude: center.lng}));
}

function updatePopup(marker, initOpen=true) {
    marker.bindPopup(`
        <div class="text-container">
            <b>Latitude:</b> ${marker.point.polar.degrees.x}<br>
            <b>Longitude:</b> ${marker.point.polar.degrees.y}<br>
            <button class="delete-marker-btn">
                Delete Marker
            </button>
        </div>
    `)

    marker.on("popupopen", function () {
        const btn = marker.getPopup().getElement().querySelector(".delete-marker-btn");

        btn.addEventListener("click", () => {
            deleteBaseMarker(marker);
        });
    });

    if (initOpen) {
        marker.openPopup();
    }
}

function refreshMarkers() {
    markers.forEach(marker => {
        deleteBaseMarker(marker);
    });
    refreshOutputMarkers();
    console.log(markers);
}

function refreshOutputMarkers() {
    deleteCentreMarker();
    iteration_markers.forEach(marker => {
        deleteTrackMarker(marker);
    });
}

document.getElementById("add-marker-view-btn").addEventListener("click", addMarkerAtView);
document.getElementById("refresh-btn").addEventListener("click", refreshMarkers);

export {addBaseMarker, addCentreMarker, addTrackMarker, refreshOutputMarkers, getMarkers}