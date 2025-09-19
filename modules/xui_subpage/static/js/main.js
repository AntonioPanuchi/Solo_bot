let appSettings = null;
let currentSubscriptionLink = '';
let currentSelectedApp = null;

window.currentSelectedApp = null;
window.currentSubscriptionLink = '';
window.appSettings = null;

async function loadAppSettings() {
  try {
    appSettings = await window.api.getSettings();
    window.appSettings = appSettings;
    
    if (appSettings.base_path && window.updateBasePath) {
      window.updateBasePath(appSettings.base_path);
    }
    
    if (appSettings.language) {
      window.setCurrentLanguage(window.detectUserLanguage(appSettings.language));
    } else {
      window.setCurrentLanguage(window.detectUserLanguage());
    }
    
    await window.loadAppTexts(window.getCurrentLanguage());
    
    window.buildPlatformConfigs(appSettings);
    
    window.applyColorTheme(appSettings.color_theme || 'dark');
    
  } catch (err) {
    window.setCurrentLanguage(window.detectUserLanguage());
    await window.loadAppTexts(window.getCurrentLanguage());
    window.applyColorTheme('dark');
  }
}




async function initializeApp() {
  try {
    await loadAppSettings();
    
    window.initializeLanguage();
    
    window.initLanguageToggle();
    
    await loadSubscriptionData();
    
    initializeUI();
    
    await new Promise(resolve => setTimeout(resolve, 300));
    
    hidePageLoader();
    
    window.onPageLoad?.();
    
  } catch (error) {
    window.showError?.('Failed to load application data');
    setTimeout(() => hidePageLoader(), 1000);
  }
}

async function loadSubscriptionData() {
  try {
    const params = new URLSearchParams(window.location.search);
    const keyName = params.get('key_name');
    const userId = window.telegram.getUserId();

    if (!keyName && !userId) {
      throw new Error('No key_name or user_id provided');
    }

    const data = await window.loadSubscription(keyName, userId);
    
    currentSubscriptionLink = data.link;
    window.currentSubscriptionLink = data.link;

    window.updateSubscriptionUI(data, keyName);

    const detectedOS = window.detectOperatingSystem();

    if (window.setPlatform) {
      window.setPlatform(detectedOS);
    }

    window.updatePlatform(detectedOS);

    const platformSelect = document.getElementById('platform-select');
    if (platformSelect) {
      platformSelect.value = detectedOS;
    }
    
  } catch (error) {
    window.showError?.('Failed to load subscription data');
  }
}

function showPageLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.remove('hidden');
  }
}

function hidePageLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('hidden');
    
    setTimeout(() => {
      if (loader.parentNode) {
        loader.parentNode.removeChild(loader);
      }
    }, 500);
  }
}

function initializeUI() {
  const platformSelect = document.getElementById('platform-select');
  if (platformSelect) {
    platformSelect.addEventListener('change', (e) => {
      window.updatePlatform(e.target.value);
    });
  }
  
  
  const getLinkBtn = document.getElementById('get-link-btn');
  if (getLinkBtn) {
    getLinkBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.copyKey();
    });
  }
  
  setupLinkHandler();
  
  setupSupportLinks();
  
  if (window.initQRScanner) {
    window.initQRScanner();
  }
}

function setupLinkHandler() {
  document.body.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a || !a.href) return;
    
    e.preventDefault();
    const href = a.getAttribute('href');
    window.telegram.openLink(href);
  });
}

function setupSupportLinks() {
  document.querySelectorAll('.support-chat-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const supportUrl = link.getAttribute('data-support-url');
      if (supportUrl) {
        window.telegram.openTelegramLink(supportUrl);
      }
      
      return false;
    });
  });
}








if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}
