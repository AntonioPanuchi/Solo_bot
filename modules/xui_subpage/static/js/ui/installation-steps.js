
function updateInstallationSteps(app) {
    const stepsContainer = document.getElementById('steps-container');
    if (!stepsContainer) return;
    
    const connectUrl = window.currentSubscriptionLink 
        ? `${window.REDIRECT_BASE}${encodeURI(app.proto + window.currentSubscriptionLink)}`
        : '#';
    
    let downloadButtons = '';
    if (!app.noButtons) {
        if (app.downloadUrls) {
            downloadButtons = app.downloadUrls.map(download => `
                <a href="${download.url}" class="btn-primary" target="_blank" style="margin-bottom: 6px;">
                    <i class="fas fa-external-link-alt"></i>
                    ${typeof download.text === 'function' ? download.text() : download.text}
                </a>
            `).join('');
        } else if (app.downloadUrl) {
            const downloadText = app.downloadUrl.includes('apple.com') 
                ? t('open_in_app_store')
                : app.downloadUrl.includes('play.google.com')
                ? t('open_in_google_play')
                : `${t('download')} ${app.name}`;
            
            downloadButtons = `
                <a href="${app.downloadUrl}" class="btn-primary" target="_blank">
                    <i class="fas fa-external-link-alt"></i>
                    ${downloadText}
                </a>
            `;
        }
    }
    
    const steps = [];
    
    steps.push({
        icon: 'fas fa-download',
        title: `${t('install_title')} ${app.displayName || app.name}`,
        description: typeof app.instructions.install === 'function' ? app.instructions.install() : app.instructions.install,
        note: app.instructions.note ? (typeof app.instructions.note === 'function' ? app.instructions.note() : app.instructions.note) : undefined,
        buttons: downloadButtons
    });
    
    if (app.instructions.subscribe) {
        let subscribeButtons = '';
        const currentPlatform = window.getCurrentPlatform ? window.getCurrentPlatform() : 'ios';
        
        if (currentPlatform === 'androidtv') {
            subscribeButtons = `
                <button class="btn-primary" onclick="showTVQRModal()" type="button">
                    <i class="fas fa-qrcode"></i>
                    ${t('qr_tv_happ')}
                </button>
            `;
        } else if (currentPlatform === 'appletv') {
            subscribeButtons = `
                <button class="btn-primary" onclick="showTVQRModal()" type="button">
                    <i class="fas fa-qrcode"></i>
                    ${t('qr_tv_happ')}
                </button>
            `;
        }
        
        steps.push({
            icon: 'fas fa-qrcode',
            title: t('add_subscription_title'),
            description: typeof app.instructions.subscribe === 'function' ? app.instructions.subscribe() : app.instructions.subscribe,
            buttons: subscribeButtons
        });
    } else {
        steps.push({
            icon: 'fas fa-cloud-upload-alt',
            title: t('add_subscription_title'),
            description: t(`add_subscription_${app.name.toLowerCase()}`),
            buttons: app.noButtons ? '' : `
                <a href="${connectUrl}" class="btn-primary" target="_blank">
                    <i class="fas fa-plus"></i>
                    ${t('add_subscription_button')}
                </a>
            `
        });
    }
    
    steps.push({
        icon: 'fas fa-check',
        title: t('connect_title'),
        description: typeof app.instructions.connect === 'function' ? app.instructions.connect() : app.instructions.connect
    });
    
    const fragment = document.createDocumentFragment();
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = steps.map(step => `
        <div class="step">
            <div class="step-icon">
                <i class="${step.icon}"></i>
            </div>
            <div class="step-content">
                <h3>${step.title}</h3>
                <p>${step.description}</p>
                ${step.note ? `<p style="font-size: 12px; color: var(--warning); margin-top: 8px; font-style: italic;"><i class="fas fa-exclamation-triangle"></i> ${step.note}</p>` : ''}
                ${step.buttons || ''}
            </div>
        </div>
    `).join('');
    
    stepsContainer.innerHTML = '';
    while (tempDiv.firstChild) {
        fragment.appendChild(tempDiv.firstChild);
    }
    stepsContainer.appendChild(fragment);
}

window.updateInstallationSteps = updateInstallationSteps;