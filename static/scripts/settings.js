function toggleSettingsPanel() {
    var panel = document.getElementById('settings-panel');
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}

function saveSettings() {
    var experimental = document.getElementById('experimental').checked;
    var alpha = parseFloat(document.getElementById('alpha').value);
    var precision = parseInt(document.getElementById('precision').value, 10);
    var track = parseInt(document.getElementById('track').value, 10);
    var balanced = document.getElementById('balanced').checked;
    
    // Save settings to session storage or another storage method
    sessionStorage.setItem('experimental', experimental);
    sessionStorage.setItem('alpha', alpha);
    sessionStorage.setItem('precision', precision);
    sessionStorage.setItem('track', track);
    sessionStorage.setItem('balanced', balanced);

    // Hide the settings panel after saving
    toggleSettingsPanel();
}

function getSettings() {
    return {
        experimental: sessionStorage.getItem('experimental') === 'true',
        alpha: parseFloat(sessionStorage.getItem('alpha')) || 1,
        precision: parseInt(sessionStorage.getItem('precision'), 10) || 10,
        track: parseInt(sessionStorage.getItem('track'), 10) || 10,
        balanced: sessionStorage.getItem('balanced') === 'true'
    };
}