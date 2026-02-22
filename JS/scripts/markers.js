import {Point} from './point.js';
import {map,markers} from './map.js';

function addMarkerAtView() {
    var center = map.getCenter();
    addMarker(new Point({latitude: center.lat, longitude: center.lng}));
}

function addMarker(p) {
    const marker = L.marker([p.polar.degrees.x, p.polar.degrees.y], { draggable: true}).addTo(map)

    marker.point = p;
    updatePopup(marker);

    marker.on('dragend', function (event) {
        const marker = event.target;
        const position = marker.getLatLng();

        marker.point.setLatLng(position.lat, position.lng);

        updatePopup(marker);
    });

    markers.push(marker);
}

function deleteMarker(marker) {
    const i = markers.indexOf(marker);
    markers.slice(i,i);
    map.removeLayer(marker);
}

function updatePopup(marker) {
    marker.bindPopup(`
        <div class="text-container">
            <b>Latitude:</b> ${marker.point.polar.degrees.x}<br>
            <b>Longitude:</b> ${marker.point.polar.degrees.x}<br>
            <button class="delete-marker-btn">
                Delete Marker
            </button>
        </div>
    `)

    marker.on("popupopen", function () {
        const btn = marker.getPopup().getElement().querySelector(".delete-marker-btn");

        btn.addEventListener("click", () => {
            deleteMarker(marker);
        });
    });

    marker.openPopup();
}

function refreshMarkers() {
    markers.forEach(marker => {
        deleteMarker(marker);
    });
}

document.getElementById("add-marker-view-btn").addEventListener("click", addMarkerAtView);
document.getElementById("refresh-btn").addEventListener("click", refreshMarkers);

export {addMarker}