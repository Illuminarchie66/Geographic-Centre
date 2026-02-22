const settings = {
    experimental: false,
    balanced: false,
    alpha: 1,
    precision: 1e-10,
    track: 10
};

function initSettingsUI() {

    const experimental = document.getElementById("experimental");
    const balanced = document.getElementById("balanced");
    const alpha = document.getElementById("alpha");
    const precision = document.getElementById("precision");
    const track = document.getElementById("track");

    experimental.checked = settings.experimental;
    balanced.checked = settings.balanced;
    alpha.value = settings.alpha;
    precision.value = settings.precision;
    track.value = settings.track;

    experimental.addEventListener("change", () => {
        settings.experimental = experimental.checked;
    });

    balanced.addEventListener("change", () => {
        settings.balanced = balanced.checked;
    });

    alpha.addEventListener("input", () => {
        settings.alpha = parseFloat(alpha.value);
    });

    precision.addEventListener("input", () => {
        settings.precision = parseInt(precision.value);
    });

    track.addEventListener("input", () => {
        settings.track = parseInt(track.value);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initSettingsUI();
});


function toggleSettingsPanel() {
    var panel = document.getElementById('settings-panel');
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}

document.getElementById("settings-btn")
    .addEventListener("click", toggleSettingsPanel);
document.getElementById("close-btn")
    .addEventListener("click", toggleSettingsPanel);

export {settings}