let platformConfigs = {};

function generateDownloadButtonText(url, displayName) {
    if (url.includes('apple.com')) {
        return t('open_in_app_store');
    }
    if (url.includes('play.google.com')) {
        return t('open_in_google_play');
    }

    let text = `${t('download')} ${displayName}`;
    if (url.endsWith('.apk')) {
        text += ' [apk]';
    }
    return text;
}

function getAppButtons(app, platform, downloadUrls, buttonsEnabled) {
    const buttons = [];
    const appName = typeof app === 'string' ? app : app.name;
    const displayName = typeof app === 'string' ? app : (app.displayName || app.name);
    const appNameLower = appName.toLowerCase();

    for (let i = 1; i <= 10; i++) {
        const buttonKey = `${appNameLower}_${i}`;
        const urlKey = `${appNameLower}_${i}`;

        const url = downloadUrls[platform]?.[urlKey];
        const buttonOrder = buttonsEnabled[platform]?.[buttonKey];

        if (url && buttonOrder > 0) {
            let buttonText;

            if (platform === 'ios' && appNameLower === 'happ' && i === 1) {
                buttonText = () => t('open_in_app_store_rus');
            } else if (platform === 'ios' && appNameLower === 'happ' && i === 2) {
                buttonText = () => t('open_in_app_store_mir');
            } else if (platform === 'macos' && appNameLower === 'happ' && i === 1) {
                buttonText = () => t('for_m_series');
            } else if (platform === 'macos' && appNameLower === 'happ' && i === 2) {
                buttonText = () => t('for_intel');
            } else {
                buttonText = () => generateDownloadButtonText(url, displayName);
            }

            buttons.push({
                text: buttonText,
                url: url,
                order: buttonOrder
            });
        }
    }

    return buttons.sort((a, b) => a.order - b.order);
}

function detectOperatingSystem() {
    const userAgent = navigator.userAgent.toLowerCase();
    const platform = navigator.platform.toLowerCase();

    if (/appletv|tvos/.test(userAgent)) {
        return 'appletv';
    }

    if (/android.*tv|googletv|smarttv|androidtv/.test(userAgent)) {
        return 'androidtv';
    }

    if (/iphone|ipod/.test(userAgent)) {
        return 'ios';
    }

    if (/ipad/.test(userAgent)) {
        return 'ios';
    }

    if (/android/.test(userAgent)) {
        return 'android';
    }

    if (/mac/.test(platform) || /darwin/.test(platform)) {
        return 'macos';
    }

    if (/win/.test(platform) || /windows/.test(userAgent)) {
        return 'windows';
    }

    if (/linux/.test(platform) || /x11/.test(platform)) {
        return 'linux';
    }

    return 'ios';
}


function buildPlatformConfigs(settings) {
    if (!settings || !settings.apps || Object.keys(settings.apps).length === 0) {
        return;
    }
    
    const { deeplinks, app_links, apps, buttons } = settings;
    
    platformConfigs = {
        ios: {
            icon: 'fab fa-apple',
            apps: []
        },
        android: {
            icon: 'fab fa-android', 
            apps: []
        },
        windows: {
            icon: 'fab fa-windows',
            apps: []
        },
        macos: {
            icon: 'fab fa-apple',
            apps: []
        },
        linux: {
            icon: 'fab fa-linux',
            apps: []
        },
        appletv: {
            icon: 'fab fa-apple',
            apps: []
        },
        androidtv: {
            icon: 'fab fa-android',
            apps: []
        }
    };
    
    if (apps.ios?.Happ > 0) {
        const downloadUrls = getAppButtons('Happ', 'ios', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.ios.apps.push({
                name: 'Happ',
                proto: deeplinks.happ,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_happ_ios'),
                    connect: () => t('connect_happ')
                }
            });
        }
    }
    
    if (apps.ios?.V2rayTun > 0) {
        const downloadUrls = getAppButtons('V2rayTun', 'ios', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.ios.apps.push({
                name: 'V2rayTun',
                proto: deeplinks.v2raytun,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_v2raytun_ios'),
                    connect: () => t('connect_v2raytun')
                }
            });
        }
    }
    
    if (apps.ios?.Shadowrocket > 0) {
        const downloadUrls = getAppButtons('Shadowrocket', 'ios', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.ios.apps.push({
                name: 'Shadowrocket',
                proto: deeplinks.shadowrocket,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_shadowrocket_ios'),
                    connect: () => t('connect_shadowrocket')
                }
            });
        }
    }
    
    if (apps.ios?.Streisand > 0) {
        const downloadUrls = getAppButtons('Streisand', 'ios', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.ios.apps.push({
                name: 'Streisand',
                proto: deeplinks.streisand,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_streisand_ios'),
                    connect: () => t('connect_streisand')
                }
            });
        }
    }
    
    if (apps.android?.Happ > 0) {
        const downloadUrls = getAppButtons('Happ', 'android', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.android.apps.push({
                name: 'Happ',
                proto: deeplinks.happ,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_happ_android'),
                    connect: () => t('connect_happ')
                }
            });
        }
    }
    
    if (apps.android?.Hiddify > 0) {
        const downloadUrls = getAppButtons('Hiddify', 'android', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.android.apps.push({
                name: 'Hiddify',
                proto: deeplinks.hiddify,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_hiddify_android'),
                    connect: () => t('connect_hiddify')
                }
            });
        }
    }
    
    if (apps.android?.V2rayTun > 0) {
        const downloadUrls = getAppButtons('V2rayTun', 'android', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.android.apps.push({
                name: 'V2rayTun',
                proto: deeplinks.v2raytun,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_v2raytun_android'),
                    connect: () => t('connect_v2raytun')
                }
            });
        }
    }
    
    if (apps.windows?.Happ > 0) {
        const downloadUrls = getAppButtons('Happ', 'windows', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.windows.apps.push({
                name: 'Happ',
                proto: deeplinks.happ,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_happ_windows'),
                    connect: () => t('connect_happ'),
                    note: () => t('antivirus_note')
                }
            });
        }
    }
    
    if (apps.windows?.Hiddify > 0) {
        const downloadUrls = getAppButtons('Hiddify', 'windows', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.windows.apps.push({
                name: 'Hiddify',
                proto: deeplinks.hiddify,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_hiddify_windows'),
                    connect: () => t('connect_hiddify'),
                    note: () => t('antivirus_note')
                }
            });
        }
    }
    
    if (apps.windows?.V2rayTun > 0) {
        const downloadUrls = getAppButtons('V2rayTun', 'windows', app_links, buttons);

        if (downloadUrls.length > 0) {
            platformConfigs.windows.apps.push({
                name: 'V2rayTun',
                proto: deeplinks.v2raytun,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_v2raytun_windows'),
                    connect: () => t('connect_v2raytun')
                }
            });
        }
    }

    if (apps.windows?.Koalaclash > 0) {
        const downloadUrls = getAppButtons({name: 'Koalaclash', displayName: 'Koala Clash'}, 'windows', app_links, buttons);

        if (downloadUrls.length > 0) {
            platformConfigs.windows.apps.push({
                name: 'Koalaclash',
                displayName: 'Koala Clash',
                proto: deeplinks.clash,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_koalaclash_windows'),
                    connect: () => t('connect_koalaclash'),
                    note: () => t('antivirus_note')
                }
            });
        }
    }
    
    if (apps.macos?.Happ > 0) {
        const downloadUrls = getAppButtons('Happ', 'macos', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.macos.apps.push({
                name: 'Happ',
                proto: deeplinks.happ,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_happ_macos'),
                    connect: () => t('connect_happ')
                }
            });
        }
    }
    
    if (apps.macos?.Hiddify > 0) {
        const downloadUrls = getAppButtons('Hiddify', 'macos', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.macos.apps.push({
                name: 'Hiddify',
                proto: deeplinks.hiddify,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_hiddify_macos'),
                    connect: () => t('connect_hiddify')
                }
            });
        }
    }
    
    if (apps.macos?.V2rayTun > 0) {
        const downloadUrls = getAppButtons('V2rayTun', 'macos', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.macos.apps.push({
                name: 'V2rayTun',
                proto: deeplinks.v2raytun,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_v2raytun_macos'),
                    connect: () => t('connect_v2raytun')
                }
            });
        }
    }
    
    if (apps.macos?.Shadowrocket > 0) {
        const downloadUrls = getAppButtons('Shadowrocket', 'macos', app_links, buttons);

        if (downloadUrls.length > 0) {
            platformConfigs.macos.apps.push({
                name: 'Shadowrocket',
                proto: deeplinks.shadowrocket,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_shadowrocket_macos'),
                    connect: () => t('connect_shadowrocket')
                }
            });
        }
    }

    if (apps.macos?.Koalaclash > 0) {
        const downloadUrls = getAppButtons({name: 'Koalaclash', displayName: 'Koala Clash'}, 'macos', app_links, buttons);

        if (downloadUrls.length > 0) {
            platformConfigs.macos.apps.push({
                name: 'Koalaclash',
                displayName: 'Koala Clash',
                proto: deeplinks.clash,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_koalaclash_macos'),
                    connect: () => t('connect_koalaclash')
                }
            });
        }
    }
    
    if (apps.linux?.Hiddify > 0) {
        const downloadUrls = getAppButtons('Hiddify', 'linux', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.linux.apps.push({
                name: 'Hiddify',
                proto: deeplinks.hiddify,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_hiddify_linux'),
                    connect: () => t('connect_hiddify')
                }
            });
        }
    }
    
    if (apps.linux?.Happ > 0) {
        const downloadUrls = getAppButtons('Happ', 'linux', app_links, buttons);
        
        if (downloadUrls.length > 0) {
            platformConfigs.linux.apps.push({
                name: 'Happ',
                proto: deeplinks.happ,
                downloadUrls: downloadUrls,
                instructions: {
                    install: () => t('install_happ_linux'),
                    connect: () => t('connect_happ')
                }
            });
        }
    }
    
    if (apps.appletv?.Happ > 0) {
        platformConfigs.appletv.apps.push({
            name: 'Happ',
            proto: deeplinks.happ,
            noButtons: true,
            instructions: {
                install: () => t('install_happ_appletv'),
                subscribe: () => t('add_subscription_tv'),
                connect: () => t('connect_happ_appletv')
            }
        });
    }
    
    if (apps.androidtv?.Happ > 0) {
        platformConfigs.androidtv.apps.push({
            name: 'Happ',
            proto: deeplinks.happ,
            noButtons: true,
            instructions: {
                install: () => t('install_happ_androidtv'),
                subscribe: () => t('add_subscription_tv'),
                connect: () => t('connect_happ_androidtv')
            }
        });
    }

    ['ios', 'android', 'windows', 'macos', 'linux', 'appletv', 'androidtv'].forEach(platform => {
        if (platformConfigs[platform] && apps[platform]) {
            platformConfigs[platform].apps.sort((a, b) => {
                const orderA = apps[platform][a.name] || 999;
                const orderB = apps[platform][b.name] || 999;
                
                if (orderA === orderB) {
                    return a.name.localeCompare(b.name);
                }
                
                return orderA - orderB;
            });
        }
    });
}

window.detectOperatingSystem = detectOperatingSystem;
window.buildPlatformConfigs = buildPlatformConfigs;

window.getPlatformConfigs = () => platformConfigs;