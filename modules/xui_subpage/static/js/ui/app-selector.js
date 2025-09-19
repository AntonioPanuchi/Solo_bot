
function updateAppSelector(apps) {
    const appSelector = document.getElementById('app-selector');
    if (!appSelector) return;
    
    appSelector.innerHTML = apps.map((app, index) => `
        <button class="app-option ${index === 0 ? 'active' : ''}" data-app-index="${index}">
            ${app.displayName || app.name}
        </button>
    `).join('');
    
    appSelector.querySelectorAll('.app-option').forEach((option, index) => {
        option.addEventListener('click', () => {
            appSelector.querySelectorAll('.app-option').forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            window.selectApp(apps[index]);
        });
    });
}

function selectApp(app) {
    window.currentSelectedApp = app;
    window.updateInstallationSteps(app);
}

window.updateAppSelector = updateAppSelector;
window.selectApp = selectApp;