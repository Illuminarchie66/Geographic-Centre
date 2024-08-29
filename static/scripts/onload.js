window.onload = async function() {
    document.getElementById("defaultOpen").click();

    current_id = await fetchCurrentId();
    temp = await fetchMarkers();
    temp.forEach(m => {
        addMarker(m.latitude, m.longitude, m.id);
    });
    clearIterations();

    // Retrieve values from session storage
    const experimental = sessionStorage.getItem('experimental') === 'true';
    const balanced = sessionStorage.getItem('balanced') === 'true';
    const alpha = sessionStorage.getItem('alpha') || 1;
    const precision = sessionStorage.getItem('precision') || 10;
    const track = sessionStorage.getItem('track') || 10;

    // Set the input values
    document.getElementById('experimental').checked = experimental;
    document.getElementById('balanced').checked = balanced;
    document.getElementById('alpha').value = alpha;
    document.getElementById('precision').value = precision;
    document.getElementById('track').value = track;
};