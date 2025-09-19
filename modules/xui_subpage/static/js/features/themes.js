
function applyColorTheme(theme) {
    const body = document.body;
    
    body.classList.remove('theme-dark', 'theme-cyberpunk', 'theme-ocean', 'theme-light', 'theme-fox');
    
    body.classList.add(`theme-${theme}`);
}

window.applyColorTheme = applyColorTheme;