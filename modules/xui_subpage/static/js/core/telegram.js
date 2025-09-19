
let telegramWebApp = null;
let isWebAppAvailable = false;
let webAppData = null;

function initTelegramWebApp() {
    if (typeof window === 'undefined') return false;
    
    const tg = window.Telegram?.WebApp;
    if (!tg) {
        return false;
    }
    
    const hasValidInitData = !!(
        tg.initData && 
        typeof tg.initData === 'string' && 
        tg.initData.length > 0
    );
    
    if (!hasValidInitData) {
        return false;
    }
    
    telegramWebApp = tg;
    isWebAppAvailable = true;
    
    try {
        tg.expand();
        tg.ready();
        
        webAppData = {
            user: tg.initDataUnsafe?.user,
            chat: tg.initDataUnsafe?.chat,
            startParam: tg.initDataUnsafe?.start_param,
            queryId: tg.initDataUnsafe?.query_id,
            authDate: tg.initDataUnsafe?.auth_date
        };
        
    } catch (error) {
        isWebAppAvailable = false;
        return false;
    }
    
    return true;
}

function isTelegramWebAppAvailable() {
    return isWebAppAvailable;
}

function getTelegramWebApp() {
    return telegramWebApp;
}

function getTelegramUser() {
    return webAppData?.user || null;
}

function getTelegramUserId() {
    return webAppData?.user?.id || null;
}

function getTelegramUserLanguage() {
    return webAppData?.user?.language_code || null;
}

function getTelegramInitData() {
    return telegramWebApp?.initData || '';
}

function applyTelegramTheme() {
    if (!telegramWebApp?.themeParams) return;
    
    const theme = telegramWebApp.themeParams;
    const documentElement = document.documentElement;
    
    if (theme.bg_color) {
        documentElement.style.setProperty('--tg-theme-bg-color', theme.bg_color);
    }
    if (theme.text_color) {
        documentElement.style.setProperty('--tg-theme-text-color', theme.text_color);
    }
    if (theme.hint_color) {
        documentElement.style.setProperty('--tg-theme-hint-color', theme.hint_color);
    }
    if (theme.link_color) {
        documentElement.style.setProperty('--tg-theme-link-color', theme.link_color);
    }
    if (theme.button_color) {
        documentElement.style.setProperty('--tg-theme-button-color', theme.button_color);
    }
    if (theme.button_text_color) {
        documentElement.style.setProperty('--tg-theme-button-text-color', theme.button_text_color);
    }
    if (theme.secondary_bg_color) {
        documentElement.style.setProperty('--tg-theme-secondary-bg-color', theme.secondary_bg_color);
    }
}

function openLink(url) {
    if (isWebAppAvailable && telegramWebApp?.openLink) {
        telegramWebApp.openLink(url);
    } else {
        window.open(url, '_blank');
    }
}

function isDesktopPlatform() {
    const userAgent = navigator.userAgent.toLowerCase();
    const platform = navigator.platform.toLowerCase();

    return (
        /win/.test(platform) ||
        /mac/.test(platform) ||
        /linux/.test(platform) ||
        /windows/.test(userAgent) ||
        !/mobile|android|iphone|ipad|ipod/.test(userAgent)
    );
}

function openTelegramLink(url) {
    if (isDesktopPlatform()) {
        if (isWebAppAvailable && telegramWebApp?.openLink) {
            telegramWebApp.openLink(url);
        } else {
            window.open(url, '_blank');
        }
        return;
    }

    if (isWebAppAvailable && telegramWebApp?.openTelegramLink) {
        telegramWebApp.openTelegramLink(url);
    } else {
        window.open(url, '_blank');
    }
}

function showAlert(message) {
    if (isWebAppAvailable && telegramWebApp?.showAlert) {
        telegramWebApp.showAlert(message);
    } else {
        alert(message);
    }
}

function showConfirm(message, callback) {
    if (isWebAppAvailable && telegramWebApp?.showConfirm) {
        telegramWebApp.showConfirm(message, callback);
    } else {
        const result = confirm(message);
        if (callback) callback(result);
    }
}

function getDebugInfo() {
    return {
        isWebAppAvailable,
        webAppData,
        themeParams: telegramWebApp?.themeParams,
        version: telegramWebApp?.version,
        platform: telegramWebApp?.platform,
        colorScheme: telegramWebApp?.colorScheme
    };
}

const initialized = initTelegramWebApp();
if (initialized) {
    applyTelegramTheme();
}

window.telegram = {
    init: initTelegramWebApp,
    isAvailable: isTelegramWebAppAvailable,
    getWebApp: getTelegramWebApp,
    getUser: getTelegramUser,
    getUserId: getTelegramUserId,
    getUserLanguage: getTelegramUserLanguage,
    getInitData: getTelegramInitData,
    applyTheme: applyTelegramTheme,
    openLink,
    openTelegramLink,
    showAlert,
    showConfirm,
    getDebugInfo
};