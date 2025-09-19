
function isHapticAvailable() {
    return !!(window.Telegram?.WebApp?.HapticFeedback);
}

function isAndroid() {
    return /Android/i.test(navigator.userAgent);
}

function lightImpact() {
    if (isHapticAvailable()) {
        if (isAndroid()) {
            window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
        } else {
            window.Telegram.WebApp.HapticFeedback.impactOccurred('light');
        }
    }
}

function mediumImpact() {
    if (isHapticAvailable()) {
        if (isAndroid()) {
            window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
        } else {
            window.Telegram.WebApp.HapticFeedback.impactOccurred('medium');
        }
    }
}

function heavyImpact() {
    if (isHapticAvailable()) {
        if (isAndroid()) {
            window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
        } else {
            window.Telegram.WebApp.HapticFeedback.impactOccurred('heavy');
        }
    }
}

function successNotification() {
    if (isHapticAvailable()) {
        window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
    }
}

function errorNotification() {
    if (isHapticAvailable()) {
        window.Telegram.WebApp.HapticFeedback.notificationOccurred('error');
    }
}

function warningNotification() {
    if (isHapticAvailable()) {
        window.Telegram.WebApp.HapticFeedback.notificationOccurred('warning');
    }
}


function onPageLoad() {
    mediumImpact();
}

function onLanguageSwitch() {
    lightImpact();
}

function onZoomChange() {
    lightImpact();
}

function onLinkCopy() {
    successNotification();
}

function onQRSuccess() {
    successNotification();
}

window.isHapticAvailable = isHapticAvailable;
window.lightImpact = lightImpact;
window.mediumImpact = mediumImpact;
window.heavyImpact = heavyImpact;
window.successNotification = successNotification;
window.errorNotification = errorNotification;
window.warningNotification = warningNotification;
window.onPageLoad = onPageLoad;
window.onLanguageSwitch = onLanguageSwitch;
window.onZoomChange = onZoomChange;
window.onLinkCopy = onLinkCopy;
window.onQRSuccess = onQRSuccess;