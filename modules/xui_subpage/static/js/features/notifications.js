
const NOTIFICATION_CONFIG = {
    duration: 1000,
    animationDuration: 300,
    maxWidth: '280px',
    position: {
        bottom: '20px',
        left: '50%'
    },
    zIndex: 1000
};

const NOTIFICATION_TYPES = {
    success: {
        icon: 'fa-check-circle',
        color: '#10b981'
    },
    error: {
        icon: 'fa-exclamation-circle',
        color: '#ef4444'
    },
    warning: {
        icon: 'fa-exclamation-triangle',
        color: '#f59e0b'
    },
    info: {
        icon: 'fa-info-circle',
        color: '#3b82f6'
    }
};

function showNotification(message, type = 'info', options = {}) {
    const config = { ...NOTIFICATION_CONFIG, ...options };
    const typeConfig = NOTIFICATION_TYPES[type] || NOTIFICATION_TYPES.info;
    
    const notification = createNotificationElement(message, typeConfig, config);
    document.body.appendChild(notification);
    
    animateIn(notification);
    
    setTimeout(() => {
        hideNotification(notification, config.animationDuration);
    }, config.duration);
    
    return notification;
}

function createNotificationElement(message, typeConfig, config) {
    const notification = document.createElement('div');
    
    notification.style.cssText = `
        position: fixed;
        bottom: ${config.position.bottom};
        left: ${config.position.left};
        transform: translateX(-50%);
        background: var(--bg-card);
        backdrop-filter: blur(10px);
        color: var(--text-primary);
        padding: 12px 16px;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-primary);
        box-shadow: var(--shadow-md);
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
        z-index: ${config.zIndex};
        max-width: ${config.maxWidth};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
    `;
    
    notification.innerHTML = `
        <i class="fas ${typeConfig.icon}" style="color: ${typeConfig.color}; font-size: 16px;"></i>
        <span>${message}</span>
    `;
    
    return notification;
}

function animateIn(notification) {
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(-50%) translateY(20px) scale(0.9)';
        
        requestAnimationFrame(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(-50%) translateY(0) scale(1)';
        });
    });
}

function hideNotification(notification, animationDuration) {
    if (!notification.parentNode) return;
    
    notification.style.opacity = '0';
    notification.style.transform = 'translateX(-50%) translateY(20px) scale(0.9)';
    
    setTimeout(() => {
        if (notification.parentNode) {
            document.body.removeChild(notification);
        }
    }, animationDuration);
}

function showSuccess(message, options = {}) {
    return showNotification(message, 'success', options);
}

function showError(message, options = {}) {
    return showNotification(message, 'error', options);
}

function showWarning(message, options = {}) {
    return showNotification(message, 'warning', options);
}

function showInfo(message, options = {}) {
    return showNotification(message, 'info', options);
}

function hideAllNotifications() {
    const notifications = document.querySelectorAll('[style*="z-index: 1000"]');
    notifications.forEach(notification => {
        if (notification.style.position === 'fixed') {
            hideNotification(notification, NOTIFICATION_CONFIG.animationDuration);
        }
    });
}

window.showNotification = showNotification;
window.showSuccess = showSuccess;
window.showError = showError;
window.showWarning = showWarning;
window.showInfo = showInfo;
window.hideAllNotifications = hideAllNotifications;