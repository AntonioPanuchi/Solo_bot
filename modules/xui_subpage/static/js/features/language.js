
let currentLanguage = 'ru';
let appTexts = null;

function detectUserLanguage(languageSettings = null) {
    if (!languageSettings) {
        const browserLang = navigator.language || navigator.userLanguage;
        if (browserLang.startsWith('en')) {
            return 'en';
        }
        return 'ru';
    }
    
    const { default_mode, fallback } = languageSettings;
    
    if (default_mode === 'ru') return 'ru';
    if (default_mode === 'en') return 'en';
    
    if (default_mode === 'user') {
        if (window.Telegram?.WebApp?.initDataUnsafe?.user?.language_code) {
            const tgLang = window.Telegram.WebApp.initDataUnsafe.user.language_code;
            
            if (tgLang.startsWith('en')) return 'en';
            if (tgLang.startsWith('ru')) return 'ru';
        }
        
        const browserLang = navigator.language || navigator.userLanguage;
        
        if (browserLang.startsWith('en')) return 'en';
        if (browserLang.startsWith('ru')) return 'ru';
    }
    
    return fallback || 'ru';
}

function t(key) {
    return appTexts?.[key] || key;
}

async function loadAppTexts(language = 'ru') {
    try {
        const data = await window.api.getTexts(language);
        appTexts = data.texts;
        return data.language;
    } catch (err) {
        appTexts = {};
        return 'ru';
    }
}

async function changeLanguage(lang) {
    currentLanguage = lang;
    await loadAppTexts(lang);
    updatePageLanguage();
}

function updatePageLanguage() {
    const installationTitle = document.querySelector('.section-title');
    if (installationTitle) {
        installationTitle.textContent = t('installation');
    }

    updatePlatformDropdownTexts();

    const tvInstructions = document.getElementById('tv-qr-camera-instructions');
    if (tvInstructions) {
        tvInstructions.textContent = t('tv_camera_instructions');
    }

    const tvModalTitle = document.getElementById('tv-qr-modal-title');
    if (tvModalTitle && window.getCurrentPlatform) {
        const currentPlatform = window.getCurrentPlatform();
        if (currentPlatform === 'appletv') {
            tvModalTitle.textContent = t('appletv_modal_title');
        } else if (currentPlatform === 'androidtv') {
            tvModalTitle.textContent = t('androidtv_modal_title');
        } else {
            tvModalTitle.textContent = t('appletv_modal_title');
        }
    }

    const subscriptionKeyname = document.getElementById('subscription-keyname');
    const subscriptionExpiry = document.getElementById('subscription-expiry');

    if (subscriptionKeyname && !subscriptionKeyname.textContent.trim()) {
        subscriptionKeyname.textContent = t('loading');
    }

    if (subscriptionKeyname && subscriptionKeyname.textContent === t('subscription_active')) {
        subscriptionKeyname.textContent = t('subscription_active');
    }

    if (subscriptionExpiry && subscriptionExpiry.textContent && subscriptionExpiry.dataset.expiry) {
        const expiryDate = new Date(subscriptionExpiry.dataset.expiry);
        const remainingTimeText = window.formatRemainingTime ? window.formatRemainingTime(expiryDate) : subscriptionExpiry.textContent;
        subscriptionExpiry.textContent = remainingTimeText;

        if (window.checkSubscriptionExpiry) {
            setTimeout(() => window.checkSubscriptionExpiry(), 100);
        }
    } else if (subscriptionExpiry && (
        !subscriptionExpiry.textContent.trim() ||
        subscriptionExpiry.textContent.includes('загрузка') ||
        subscriptionExpiry.textContent.includes('loading') ||
        subscriptionExpiry.textContent === t('valid_until_loading')
    )) {
        subscriptionExpiry.textContent = t('valid_until_loading');
    }

    const platformName = document.getElementById('platform-name');
    if (platformName && window.getCurrentPlatform) {
        const currentPlatform = window.getCurrentPlatform();
        if (!platformName.textContent.trim() || platformName.textContent === t('ios') || platformName.textContent === t(currentPlatform)) {
            platformName.textContent = t(currentPlatform);
        }
    }

    if (window.currentSelectedApp) {
        window.updateInstallationSteps(window.currentSelectedApp);
    }
}

function updatePlatformDropdownTexts() {
    const platformOptions = document.querySelectorAll('.platform-option');
    platformOptions.forEach(option => {
        const platform = option.dataset.value;
        const span = option.querySelector('span');
        if (span && platform) {
            span.textContent = t(platform);
        }
    });

    const platformName = document.getElementById('platform-name');
    if (platformName && window.getCurrentPlatform) {
        const currentPlatform = window.getCurrentPlatform();
        platformName.textContent = t(currentPlatform);
    }
}


function initializeLanguage() {
    updatePageLanguage();
}

window.detectUserLanguage = detectUserLanguage;
window.changeLanguage = changeLanguage;
window.updatePageLanguage = updatePageLanguage;
window.loadAppTexts = loadAppTexts;
window.initializeLanguage = initializeLanguage;
window.t = t;

function initLanguageToggle() {
    const toggle = document.querySelector('.language-toggle');
    const options = document.querySelectorAll('.language-option');
    
    if (!toggle || !options.length) return;
    
    toggle.setAttribute('data-active', currentLanguage);
    options.forEach(option => {
        if (option.dataset.lang === currentLanguage) {
            option.classList.add('active');
        } else {
            option.classList.remove('active');
        }
    });
    
    async function switchLanguage(targetLang) {
        toggle.classList.add('switching');
        setTimeout(() => toggle.classList.remove('switching'), 300);
        
        window.onLanguageSwitch?.();
        
        toggle.setAttribute('data-active', targetLang);
        options.forEach(opt => {
            if (opt.dataset.lang === targetLang) {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });
        
        await changeLanguage(targetLang);
        
        setTimeout(() => {
            const maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
            window.scrollTo({
                top: maxScroll,
                behavior: 'smooth'
            });
        }, 50);
    }
    
    toggle.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const clickedOption = e.target.closest('.language-option');
        
        let newLang;
        if (clickedOption) {
            const clickedLang = clickedOption.dataset.lang;
            if (clickedLang === currentLanguage) {
                newLang = currentLanguage === 'ru' ? 'en' : 'ru';
            } else {
                newLang = clickedLang;
            }
        } else {
            newLang = currentLanguage === 'ru' ? 'en' : 'ru';
        }
        
        await switchLanguage(newLang);
    });
}

window.getCurrentLanguage = () => currentLanguage;
window.setCurrentLanguage = (lang) => { currentLanguage = lang; };
window.getAppTexts = () => appTexts;
window.initLanguageToggle = initLanguageToggle;