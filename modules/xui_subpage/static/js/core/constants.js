
let BASE_PATH = '/connect/';

const REDIRECT_BASE = window.location.origin + '/?url=';

function updateBasePath(newPath) {
    if (newPath && newPath !== BASE_PATH) {
        BASE_PATH = newPath;
        window.BASE_PATH = BASE_PATH;
    }
}

window.BASE_PATH = BASE_PATH;
window.REDIRECT_BASE = REDIRECT_BASE;
window.updateBasePath = updateBasePath;