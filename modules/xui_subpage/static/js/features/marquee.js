
let isAnimating = false;
let originalTitleText = null;
let marqueeObserver = null;

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function checkHeaderOverflow() {
    const header = document.querySelector('.header h1');
    const titleText = document.querySelector('.header h1 .title-text');
    
    if (!header || !titleText) return;
    
    if (isAnimating) {
        return;
    }
    
    if (!originalTitleText) {
        originalTitleText = titleText.textContent;
    }
    
    if (marqueeObserver) {
        marqueeObserver.disconnect();
    }
    
    stopMarquee();
    
    titleText.textContent = originalTitleText;
    header.classList.remove('scrolling');
    titleText.style.animation = 'none';
    
    setTimeout(() => {
        const headerWidth = header.offsetWidth;
        const textWidth = titleText.scrollWidth;
        
        if (textWidth > headerWidth) {
            header.classList.add('scrolling');
            startSmoothScroll(titleText, headerWidth, textWidth);
        } else {
            header.classList.remove('scrolling');
            reconnectObserver();
        }
    }, 50);
}

function startSmoothScroll(titleText, containerWidth, textWidth) {
    const header = titleText.closest('.header h1');
    
    isAnimating = true;
    
    if (titleText.scrollAnimation) {
        cancelAnimationFrame(titleText.scrollAnimation);
        titleText.scrollAnimation = null;
    }
    
    const existingAnimations = document.querySelectorAll('.header h1 .title-text[style*="transform"]');
    existingAnimations.forEach(el => {
        if (el.scrollAnimation) {
            cancelAnimationFrame(el.scrollAnimation);
            el.scrollAnimation = null;
        }
    });
    
    const originalText = originalTitleText || titleText.textContent;
    const gap = 200;
    const speed = 50;
    
  
    const gapText = '\u00A0'.repeat(15);
    const repeatedText = (originalText + gapText).repeat(8);
    titleText.textContent = repeatedText;
    
    let currentPosition = 0;
    let lastTime = performance.now();
    
    function animate(timestamp) {
        const deltaTime = timestamp - lastTime;
        lastTime = timestamp;
        
        currentPosition -= (speed * deltaTime) / 1000;
        
        const fullTextWidth = titleText.scrollWidth;
        
        const singleBlockWidth = fullTextWidth / 8;
        if (currentPosition <= -singleBlockWidth) {
            currentPosition += singleBlockWidth;
        }
        
        titleText.style.transform = `translateX(${currentPosition}px)`;
        titleText.scrollAnimation = requestAnimationFrame(animate);
    }
    
    titleText.scrollAnimation = requestAnimationFrame(animate);
}

function stopMarquee() {
    const header = document.querySelector('.header h1');
    const titleText = document.querySelector('.header h1 .title-text');
    
    if (!header || !titleText) return;
    
    isAnimating = false;
    
    if (titleText.scrollAnimation) {
        cancelAnimationFrame(titleText.scrollAnimation);
        titleText.scrollAnimation = null;
    }
    
    header.classList.remove('scrolling');
    titleText.style.animation = 'none';
    titleText.style.transform = 'none';
    
    if (originalTitleText) {
        titleText.textContent = originalTitleText;
    }
    
    reconnectObserver();
}

function reconnectObserver() {
    setTimeout(() => {
        if (marqueeObserver && !isAnimating) {
            const targetNode = document.querySelector('.header h1');
            if (targetNode) {
                marqueeObserver.observe(targetNode, { 
                    childList: true, 
                    subtree: true, 
                    characterData: true 
                });
            }
        }
    }, 100);
}

const debouncedCheckHeaderOverflow = debounce(checkHeaderOverflow, 100);

function initializeMarquee() {
    document.addEventListener('DOMContentLoaded', debouncedCheckHeaderOverflow);
    window.addEventListener('resize', debouncedCheckHeaderOverflow);
    
    setTimeout(debouncedCheckHeaderOverflow, 500);
    
    if (window.MutationObserver) {
        marqueeObserver = new MutationObserver((mutations) => {
            const relevantChange = mutations.some(mutation => {
                if (isAnimating && mutation.type === 'characterData') {
                    return false;
                }
                return mutation.type === 'childList' || 
                       (mutation.type === 'characterData' && !isAnimating);
            });
            
            if (relevantChange && !isAnimating) {
                originalTitleText = null;
                debouncedCheckHeaderOverflow();
            }
        });
        
        reconnectObserver();
    }
}

window.checkHeaderOverflow = debouncedCheckHeaderOverflow;
window.checkHeaderOverflowImmediate = checkHeaderOverflow;
window.startSmoothScroll = startSmoothScroll;
window.stopMarquee = stopMarquee;
window.initializeMarquee = initializeMarquee;

initializeMarquee();