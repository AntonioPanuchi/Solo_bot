
let scanning = false;
let stream = null;
let animationId = null;
let videoTrack = null;
let zoomCapabilities = null;
let supportsHardwareZoom = false;
let currentZoom = 1;

let tvQRModal = null;
let tvQRCancelBtn = null;
let tvQRCloseBtn = null;
let tvQRStatus = null;
let cameraContainer = null;
let cameraVideo = null;
let scannerCanvas = null;
let cameraInstructions = null;
let zoomSlider = null;
let zoomValue = null;

function initQRScanner() {
    tvQRModal = document.getElementById('tv-qr-modal');
    tvQRCancelBtn = document.getElementById('tv-qr-modal-cancel');
    tvQRCloseBtn = document.getElementById('tv-qr-modal-close');
    tvQRStatus = document.getElementById('tv-qr-status');
    cameraContainer = document.getElementById('tv-qr-camera-container');
    cameraVideo = document.getElementById('tv-qr-camera-video');
    scannerCanvas = document.getElementById('tv-qr-scanner-canvas');
    cameraInstructions = document.getElementById('tv-qr-camera-instructions');
    zoomSlider = document.getElementById('tv-qr-zoom-slider');
    zoomValue = document.getElementById('tv-qr-zoom-value');

    if (!tvQRModal) {
        return false;
    }

    setupEventListeners();
    
    setupZoomControls();

    return true;
}

function setupEventListeners() {
    tvQRCancelBtn?.addEventListener('click', hideTVModal);
    tvQRCloseBtn?.addEventListener('click', hideTVModal);

    tvQRModal?.addEventListener('click', (e) => {
        if (e.target === tvQRModal) {
            hideTVModal();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && tvQRModal && !tvQRModal.classList.contains('hidden')) {
            hideTVModal();
        }
    });
    
    setupTapToFocus();
}


function loadTVTexts() {
    const modalTitle = document.getElementById('tv-qr-modal-title');
    const currentPlatform = window.getCurrentPlatform?.();

    if (currentPlatform === 'appletv') {
        if (modalTitle) modalTitle.textContent = window.t('appletv_modal_title') || 'Apple TV Connection';
        if (cameraInstructions) cameraInstructions.textContent = window.t('tv_camera_instructions') || 'Point camera at QR code from TV';
    } else if (currentPlatform === 'androidtv') {
        if (modalTitle) modalTitle.textContent = window.t('androidtv_modal_title') || 'Android TV Connection';
        if (cameraInstructions) cameraInstructions.textContent = window.t('tv_camera_instructions') || 'Point camera at QR code from TV';
    }
}

function showTVQRModal() {
    if (!tvQRModal) {
        return;
    }

    loadTVTexts();
    tvQRModal.classList.remove('hidden');
    tvQRStatus.textContent = '';
    tvQRStatus.className = 'tv-qr-status';
    
    
    startScanning();
}

function hideTVModal() {
    if (!tvQRModal) return;

    stopScanning();
    tvQRModal.classList.add('hidden');
    tvQRStatus.textContent = '';
    tvQRStatus.className = 'tv-qr-status';
    cameraContainer.classList.add('hidden');
}

function checkCameraSupport() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        return false;
    }
    return true;
}

async function startScanning() {
    if (scanning) return;
    
    if (!checkCameraSupport()) {
        tvQRStatus.textContent = window.t('camera_not_supported') || 'Camera not supported on this device';
        tvQRStatus.className = 'tv-qr-status error';
        return;
    }
    
    try {
        stream = await getCameraStreamWithFallback();
        
        cameraVideo.srcObject = stream;
        
        cameraVideo.muted = true;
        cameraVideo.playsInline = true;
        cameraVideo.autoplay = true;
        
        await new Promise((resolve, reject) => {
            const timeout = setTimeout(() => reject(new Error('Video load timeout')), 10000);
            
            cameraVideo.onloadedmetadata = () => {
                clearTimeout(timeout);
                cameraVideo.play().then(resolve).catch(reject);
            };
            
            cameraVideo.onerror = () => {
                clearTimeout(timeout);
                reject(new Error('Video load error'));
            };
        });
        
        cameraContainer.classList.remove('hidden');
        scanning = true;
        
        videoTrack = stream.getVideoTracks()[0];
        await checkZoomCapabilities();
        
        startScanLoop();
        
    } catch (error) {
        const errorKey = 'tv_camera_error';
        tvQRStatus.textContent = window.t(errorKey) || 'Could not access camera';
        tvQRStatus.className = 'tv-qr-status error';
    }
}

async function getCameraStreamWithFallback() {
    const constraints = [
        {
            video: { 
                facingMode: 'environment',
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        },
        {
            video: { 
                facingMode: 'environment',
                width: { min: 320 },
                height: { min: 240 }
            }
        },
        {
            video: { 
                facingMode: 'environment'
            }
        },
        {
            video: true
        }
    ];

    for (let i = 0; i < constraints.length; i++) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia(constraints[i]);
            return stream;
        } catch (error) {
            if (i === constraints.length - 1) {
                throw error;
            }
        }
    }
}

function stopScanning() {
    scanning = false;
    
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    cameraVideo.srcObject = null;
    cameraContainer.classList.add('hidden');
    
    videoTrack = null;
    zoomCapabilities = null;
    supportsHardwareZoom = false;
    currentZoom = 1;
}

async function checkZoomCapabilities() {
    try {
        if (!videoTrack) {
            enableSoftwareZoom();
            return;
        }
        
        const capabilities = videoTrack.getCapabilities();
        
        if (capabilities.zoom) {
            zoomCapabilities = capabilities.zoom;
            supportsHardwareZoom = true;
            
            updateZoomSliderRange();
        } else {
            supportsHardwareZoom = false;
            enableSoftwareZoom();
        }
    } catch (error) {
        supportsHardwareZoom = false;
        enableSoftwareZoom();
    }
}

function enableSoftwareZoom() {
    if (zoomSlider && zoomValue) {
        zoomSlider.style.display = 'block';
        zoomValue.style.display = 'block';
    }
}

function updateZoomSliderRange() {
    if (!zoomSlider || !supportsHardwareZoom || !zoomCapabilities) return;
    
    const minZoom = Math.max(zoomCapabilities.min || 1, 1);
    const maxZoom = Math.min(zoomCapabilities.max || 3, 3);
}

async function applyZoom(zoomLevel) {
    try {
        if (supportsHardwareZoom && videoTrack) {
            await videoTrack.applyConstraints({
                advanced: [{ zoom: zoomLevel }]
            });
            
            currentZoom = zoomLevel;
            
            if (cameraVideo) {
                cameraVideo.style.transform = 'scale(1)';
            }
        } else {
            throw new Error('Hardware zoom not available');
        }
    } catch (error) {
        if (cameraVideo) {
            currentZoom = zoomLevel;
            cameraVideo.style.transform = `scale(${zoomLevel})`;
            cameraVideo.style.transformOrigin = 'center center';
        }
    }
}

function setupZoomControls() {
    if (!zoomSlider || !zoomValue) return;
    
    zoomSlider.addEventListener('input', function() {
        const zoomLevel = parseInt(this.value);
        zoomValue.textContent = zoomLevel + 'x';
        
        window.onZoomChange?.();
        
        applyZoom(zoomLevel);
    });
    
    const initialZoom = parseInt(zoomSlider.value) || 1;
    currentZoom = initialZoom;
    zoomValue.textContent = initialZoom + 'x';
}

function setupTapToFocus() {
    if (!cameraVideo) return;
    
    cameraVideo.addEventListener('click', handleTapToFocus);
    cameraVideo.addEventListener('touchstart', handleTapToFocus);
    
    cameraVideo.style.cursor = 'pointer';
}

async function handleTapToFocus(event) {
    event.preventDefault();
    
    if (!videoTrack || !scanning) {
        return;
    }
    
    try {
        const rect = cameraVideo.getBoundingClientRect();
        const x = (event.clientX || event.touches?.[0]?.clientX || 0) - rect.left;
        const y = (event.clientY || event.touches?.[0]?.clientY || 0) - rect.top;
        
        const normalizedX = Math.max(0, Math.min(1, x / rect.width));
        const normalizedY = Math.max(0, Math.min(1, y / rect.height));
        
        const capabilities = videoTrack.getCapabilities();
        
        showFocusIndicator(x + rect.left, y + rect.top);
        
        if (capabilities.focusMode && capabilities.focusMode.includes('continuous')) {
            const constraints = {
                advanced: [{
                    focusMode: 'continuous',
                    pointsOfInterest: [{ x: normalizedX, y: normalizedY }]
                }]
            };
            
            videoTrack.applyConstraints(constraints).catch(() => {
            });
            
        } else if (capabilities.focusMode) {
            const constraints = {
                advanced: [{
                    focusMode: 'single-shot',
                    pointsOfInterest: [{ x: normalizedX, y: normalizedY }]
                }]
            };
            
            videoTrack.applyConstraints(constraints).catch(() => {
            });
            
        } else if (capabilities.focusDistance) {
            const constraints = {
                advanced: [{ focusMode: 'manual' }]
            };
            
            videoTrack.applyConstraints(constraints).catch(() => {
            });
        }
        
    } catch (error) {
    }
}

function showFocusIndicator(x, y) {
    const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary') || '#3b82f6';
    
    const indicator = document.createElement('div');
    indicator.style.cssText = `
        position: fixed;
        left: ${x - 30}px;
        top: ${y - 30}px;
        width: 60px;
        height: 60px;
        pointer-events: none;
        z-index: 10001;
        animation: focusPulse 0.5s ease-out;
    `;
    
    const innerIndicator = document.createElement('div');
    innerIndicator.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 20px;
        height: 20px;
        background: ${accentColor};
        border-radius: 50%;
        opacity: 0.6;
        animation: focusInner 0.5s ease-out;
    `;
    
    indicator.appendChild(innerIndicator);
    
    if (!document.getElementById('focus-animation-style')) {
        const style = document.createElement('style');
        style.id = 'focus-animation-style';
        style.textContent = `
            @keyframes focusPulse {
                0% { 
                    opacity: 1; 
                    transform: scale(0.3); 
                }
                30% { 
                    opacity: 1; 
                    transform: scale(1.1); 
                }
                100% { 
                    opacity: 0; 
                    transform: scale(1); 
                }
            }
            @keyframes focusInner {
                0% { 
                    opacity: 0.8; 
                    transform: translate(-50%, -50%) scale(0.5); 
                }
                50% { 
                    opacity: 0.4; 
                    transform: translate(-50%, -50%) scale(1.2); 
                }
                100% { 
                    opacity: 0; 
                    transform: translate(-50%, -50%) scale(1); 
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        if (indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }, 500);
}

function startScanLoop() {
    if (!scanning) return;
    
    if (cameraVideo.readyState === cameraVideo.HAVE_ENOUGH_DATA) {
        const canvas = scannerCanvas;
        const ctx = canvas.getContext('2d');
        
        canvas.width = cameraVideo.videoWidth;
        canvas.height = cameraVideo.videoHeight;
        
        ctx.drawImage(cameraVideo, 0, 0, canvas.width, canvas.height);
        
        try {
            const qrCode = detectQRCode(canvas);
            if (qrCode) {
                handleQRCodeDetected(qrCode);
                return;
            }
        } catch (error) {
        }
    }
    
    animationId = requestAnimationFrame(startScanLoop);
}

function detectQRCode(canvas) {
    if (typeof jsQR === 'undefined') {
        return null;
    }
    
    try {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        return code ? code.data : null;
    } catch (error) {
        return null;
    }
}

async function handleQRCodeDetected(qrData) {
    stopScanning();
    
    tvQRStatus.textContent = window.t('qr_detected') || 'QR detected';
    tvQRStatus.className = 'tv-qr-status';
    
    const result = extractCodeFromQR(qrData);
    
    if (!result.success) {
        tvQRStatus.textContent = `❌ ${window.t('qr_parse_error') || 'Unable to recognize QR code'}`;
        tvQRStatus.className = 'tv-qr-status error';
        return;
    }
    
    
    await sendSubscriptionToTV(result.code);
}

function extractCodeFromQR(qrData) {
    
    if (qrData.startsWith('happ://send_to_device/')) {
        try {
            const base64Data = qrData.replace('happ://send_to_device/', '');
            
            const jsonData = atob(base64Data);
            
            const data = JSON.parse(jsonData);
            const keys = Object.keys(data);
            
            if (data.uid) {
                const uidString = String(data.uid);
                if (uidString.length > 0) {
                    return { success: true, code: uidString };
                } else {
                    return { 
                        success: false, 
                        error: 'UID пустой',
                        debug: `UID: "${uidString}", тип: ${typeof data.uid}, длина: ${uidString.length}`
                    };
                }
            } else {
                return { 
                    success: false, 
                    error: 'Поле uid не найдено',
                    debug: `Доступные ключи: [${keys.join(', ')}], JSON: ${jsonData.substring(0, 200)}`
                };
            }
            
        } catch (error) {
            return { 
                success: false, 
                error: 'Ошибка декодирования',
                debug: `${error.message}`
            };
        }
    }
    
    const match = qrData.match(/\b\d{5}\b/);
    if (match) {
        return { success: true, code: match[0] };
    }
    
    const urlMatch = qrData.match(/\/(\d{5})(?:\/|$|\?)/);
    if (urlMatch) {
        return { success: true, code: urlMatch[1] };
    }
    
    return { success: false, error: 'Код не найден в QR-данных' };
}

async function sendSubscriptionToTV(code) {
    const subscriptionLink = window.currentSubscriptionLink;
    
    if (!subscriptionLink) {
        tvQRStatus.textContent = `❌ ${window.t('no_subscription_link') || 'No subscription link'}`;
        tvQRStatus.className = 'tv-qr-status error';
        return;
    }
    
    tvQRStatus.textContent = window.t('sending_to_tv') || 'Sending to TV...';
    tvQRStatus.className = 'tv-qr-status';
    
    try {
        const base64Data = btoa(subscriptionLink);
        const basePath = window.BASE_PATH || '/connect/';
        const apiUrl = `${basePath}api/tv`;
        
        
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                data: base64Data
            })
        });
        
        
        const responseData = await response.json();
        
        if (responseData.success) {
            tvQRStatus.textContent = `✅ ${window.t('subscription_sent_success') || 'Subscription sent to TV!'}`;
            tvQRStatus.className = 'tv-qr-status success';
            
            window.onQRSuccess?.();
        } else {
            throw new Error(responseData.error || 'Unknown error');
        }
    } catch (error) {
        tvQRStatus.textContent = `❌ ${window.t('send_error') || 'Failed to send subscription'}`;
        tvQRStatus.className = 'tv-qr-status error';
    }
}

window.initQRScanner = initQRScanner;
window.showTVQRModal = showTVQRModal;
window.hideTVModal = hideTVModal;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQRScanner);
} else {
    initQRScanner();
}