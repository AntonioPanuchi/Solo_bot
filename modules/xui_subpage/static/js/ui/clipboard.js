function copyKey() {
    const subscriptionLink = window.getSubscriptionLink?.() || window.currentSubscriptionLink;
    
    if (!subscriptionLink) {
        window.showError?.(window.t('no_subscription_link') || 'No subscription link available');
        return;
    }
    
    if (!navigator.clipboard) {
        copyTextFallback(subscriptionLink);
        return;
    }
    
    navigator.clipboard.writeText(subscriptionLink).then(() => {
        window.showSuccess?.(window.t('link_copied') || 'Link copied to clipboard');
        window.onLinkCopy?.();
    }).catch(err => {
        window.showError?.(window.t('failed_to_copy') || 'Failed to copy link');

        copyTextFallback(subscriptionLink);
    });
}

function copyTextFallback(text) {
    try {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.top = '-1000px';
        textArea.style.left = '-1000px';
        document.body.appendChild(textArea);
        
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        if (successful) {
            window.showSuccess?.(window.t('link_copied') || 'Link copied to clipboard');
                window.onLinkCopy?.();
        } else {
            throw new Error('execCommand failed');
        }
    } catch (err) {
        window.showError?.(window.t('failed_to_copy') || 'Failed to copy link');
    }
}

function copyText(text, successMessage, errorMessage) {
    if (!text) {
        window.showError?.(errorMessage || 'Nothing to copy');
        return;
    }
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            window.showSuccess?.(successMessage || 'Copied to clipboard');
                window.onLinkCopy?.();
        }).catch(() => {
            copyTextFallback(text);
        });
    } else {
        copyTextFallback(text);
    }
}

window.copyKey = copyKey;
window.copyText = copyText;