
const platformIcons = {
    'ios': 'fab fa-apple',
    'android': 'fab fa-android',
    'windows': 'fab fa-windows',
    'macos': 'fab fa-apple',
    'linux': 'fab fa-linux',
    'appletv': 'fas fa-tv',
    'androidtv': 'fas fa-tv'
};

function getPlatformName(platform) {
    return window.t ? window.t(platform) : platform;
}

let currentPlatform = null;

function initPlatformDropdown() {
    const dropdown = document.getElementById('platform-dropdown');
    const selected = document.getElementById('platform-selected');
    const menu = document.getElementById('platform-menu');
    const chevron = document.getElementById('platform-chevron');
    const options = document.querySelectorAll('.platform-option');

    if (!dropdown || !selected || !menu || !options.length) {
        return;
    }

    let isOpen = false;

    function toggleDropdown() {
        isOpen = !isOpen;
        menu.classList.toggle('show', isOpen);
        selected.classList.toggle('active', isOpen);
        chevron.classList.toggle('rotated', isOpen);

        if (isOpen && window.lightImpact) {
            window.lightImpact();
        }
    }

    function closeDropdown() {
        if (isOpen) {
            isOpen = false;
            menu.classList.remove('show');
            selected.classList.remove('active');
            chevron.classList.remove('rotated');
        }
    }

    function selectPlatform(platform) {
        if (platform === currentPlatform) return;

        if (window.mediumImpact) {
            window.mediumImpact();
        }

        currentPlatform = platform;

        const platformIcon = document.getElementById('platform-icon');
        const platformName = document.getElementById('platform-name');

        if (platformIcon && platformIcons[platform]) {
            platformIcon.className = `platform-icon ${platformIcons[platform]}`;
        }

        if (platformName) {
            platformName.textContent = getPlatformName(platform);
        }

        options.forEach(option => {
            option.classList.toggle('selected', option.dataset.value === platform);
        });

        closeDropdown();

        updatePlatform(platform);
    }

    selected.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleDropdown();
    });

    options.forEach(option => {
        option.addEventListener('click', (e) => {
            e.stopPropagation();
            selectPlatform(option.dataset.value);
        });
    });

    document.addEventListener('click', () => {
        closeDropdown();
    });

    document.addEventListener('keydown', (e) => {
        if (!isOpen) return;

        if (e.key === 'Escape') {
            closeDropdown();
        } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            const optionsArray = Array.from(options);
            const currentIndex = optionsArray.findIndex(opt => opt.dataset.value === currentPlatform);
            let newIndex;

            if (e.key === 'ArrowDown') {
                newIndex = (currentIndex + 1) % optionsArray.length;
            } else {
                newIndex = (currentIndex - 1 + optionsArray.length) % optionsArray.length;
            }

            selectPlatform(optionsArray[newIndex].dataset.value);
        } else if (e.key === 'Enter') {
            closeDropdown();
        }
    });

}

function updatePlatform(platform) {
    const platformConfigs = window.getPlatformConfigs();
    const config = platformConfigs[platform];
    if (!config) {
        return;
    }

    let filteredApps = config.apps;
    if (window.appSettings && window.appSettings.apps && window.appSettings.apps[platform]) {
        const platformSettings = window.appSettings.apps[platform];
        filteredApps = config.apps.filter(app => {
            return platformSettings[app.name] > 0;
        });
    }

    window.updateAppSelector(filteredApps);

    if (filteredApps.length > 0) {
        window.selectApp(filteredApps[0]);
    }
}

function getCurrentPlatform() {
    return currentPlatform || 'ios';
}

function setPlatform(platform) {
    if (currentPlatform === platform) return;

    currentPlatform = platform;

    const platformIcon = document.getElementById('platform-icon');
    const platformName = document.getElementById('platform-name');

    if (platformIcon && platformIcons[platform]) {
        platformIcon.className = `platform-icon ${platformIcons[platform]}`;
    }

    if (platformName) {
        platformName.textContent = getPlatformName(platform);
    }

    const options = document.querySelectorAll('.platform-option');
    options.forEach(option => {
        option.classList.toggle('selected', option.dataset.value === platform);
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPlatformDropdown);
} else {
    initPlatformDropdown();
}

window.updatePlatform = updatePlatform;
window.getCurrentPlatform = getCurrentPlatform;
window.setPlatform = setPlatform;