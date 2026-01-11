// ========== TOCHKAFILMS ADVANCED ANIMATIONS ==========

document.addEventListener('DOMContentLoaded', function() {
    
    // ========== SCROLL REVEAL ANIMATION ==========
    function revealOnScroll() {
        const reveals = document.querySelectorAll('.reveal');
        
        reveals.forEach(reveal => {
            const windowHeight = window.innerHeight;
            const elementTop = reveal.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', revealOnScroll);
    
    // ========== PARTICLE SYSTEM ==========
    function createParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles';
        document.body.appendChild(particlesContainer);
        
        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 10 + 5) + 's';
            particle.style.animationDelay = Math.random() * 2 + 's';
            
            particlesContainer.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 15000);
        }
        
        // Create particles periodically
        setInterval(createParticle, 2000);
    }
    
    createParticles();
    
    // ========== SMOOTH SCROLLING FOR NAVIGATION ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========== FILM CARD HOVER EFFECTS ==========
    const filmCards = document.querySelectorAll('.film-card');
    
    filmCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add glow effect to nearby cards
            const allCards = document.querySelectorAll('.film-card');
            allCards.forEach(otherCard => {
                if (otherCard !== this) {
                    otherCard.style.opacity = '0.7';
                    otherCard.style.transform = 'scale(0.95)';
                }
            });
        });
        
        card.addEventListener('mouseleave', function() {
            // Remove effects from all cards
            const allCards = document.querySelectorAll('.film-card');
            allCards.forEach(otherCard => {
                otherCard.style.opacity = '1';
                otherCard.style.transform = 'scale(1)';
            });
        });
        
        // Add ripple effect on click
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // ========== NAVBAR SCROLL EFFECT ==========
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        // Add background blur when scrolled
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(0, 0, 0, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'rgba(0, 0, 0, 0.85)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // ========== LOADING ANIMATION ==========
    function showLoading(element) {
        const loader = document.createElement('div');
        loader.className = 'loading-spinner';
        loader.style.position = 'absolute';
        loader.style.top = '50%';
        loader.style.left = '50%';
        loader.style.transform = 'translate(-50%, -50%)';
        loader.style.zIndex = '1000';
        
        element.style.position = 'relative';
        element.appendChild(loader);
        
        return loader;
    }
    
    function hideLoading(loader) {
        if (loader && loader.parentNode) {
            loader.parentNode.removeChild(loader);
        }
    }
    
    // ========== FORM ENHANCEMENTS ==========
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        // Add floating label effect
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentNode.classList.remove('focused');
            }
        });
        
        // Add typing animation
        input.addEventListener('input', function() {
            this.style.transform = 'scale(1.02)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // ========== BUTTON CLICK ANIMATIONS ==========
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create click wave effect
            const wave = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            wave.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: wave 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.appendChild(wave);
            
            setTimeout(() => {
                wave.remove();
            }, 600);
        });
    });
    
    // ========== SEARCH ENHANCEMENTS ==========
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    // Add search suggestions or live search here
                    console.log('Searching for:', query);
                }, 300);
            }
        });
    }
    
    // ========== NOTIFICATION ANIMATIONS ==========
    function animateNotificationBadge() {
        const badge = document.getElementById('notifications-badge');
        if (badge && badge.style.display !== 'none') {
            badge.classList.add('pulse');
            setTimeout(() => {
                badge.classList.remove('pulse');
            }, 2000);
        }
    }
    
    // Check for new notifications periodically
    setInterval(animateNotificationBadge, 30000);
    
    // ========== PAGE TRANSITION EFFECTS ==========
    function addPageTransitions() {
        const main = document.querySelector('main');
        if (main) {
            main.classList.add('page-transition');
        }
        
        // Add reveal class to sections
        const sections = document.querySelectorAll('section, .film-grid, .container > div');
        sections.forEach((section, index) => {
            section.classList.add('reveal');
            section.style.animationDelay = (index * 0.1) + 's';
        });
    }
    
    addPageTransitions();
    
    // ========== RESPONSIVE ANIMATIONS ==========
    function handleResize() {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            // Reduce animations on mobile for performance
            document.body.classList.add('mobile-optimized');
        } else {
            document.body.classList.remove('mobile-optimized');
        }
    }
    
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check
    
    // ========== EASTER EGG: KONAMI CODE ==========
    let konamiCode = [];
    const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA
    
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.keyCode);
        
        if (konamiCode.length > konamiSequence.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.join(',') === konamiSequence.join(',')) {
            // Activate special effects
            document.body.style.animation = 'rainbow 2s infinite';
            setTimeout(() => {
                document.body.style.animation = 'none';
            }, 10000);
        }
    });
    
    console.log('🎬 TochkaFilms Advanced Animations Loaded! 🎬');
});

// ========== CSS ANIMATIONS FOR JAVASCRIPT ==========
const style = document.createElement('style');
style.textContent = `
    @keyframes wave {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(229, 9, 20, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .mobile-optimized * {
        animation-duration: 0.3s !important;
        transition-duration: 0.3s !important;
    }
    
    .focused {
        transform: scale(1.02);
    }
`;

document.head.appendChild(style);
// ========== TRAILER FUNCTIONALITY ==========

function playTrailer() {
    const overlay = document.querySelector('.trailer-overlay');
    const iframe = document.querySelector('.trailer-wrapper iframe');
    
    if (overlay && iframe) {
        overlay.style.display = 'none';
        // Попытка автовоспроизведения
        iframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
    }
}

function showTrailerError() {
    const wrapper = document.getElementById('trailer-wrapper');
    const alternative = document.getElementById('trailer-alternative');
    
    if (wrapper && alternative) {
        wrapper.style.display = 'none';
        alternative.style.display = 'block';
    }
}

// Проверка загрузки iframe
document.addEventListener('DOMContentLoaded', function() {
    const trailerIframe = document.querySelector('.trailer-wrapper iframe');
    
    if (trailerIframe) {
        // Таймаут для проверки загрузки
        setTimeout(() => {
            try {
                // Проверяем доступность iframe
                if (!trailerIframe.contentDocument && !trailerIframe.contentWindow) {
                    showTrailerError();
                }
            } catch (e) {
                // Если есть ошибки CORS, показываем альтернативу
                console.log('Trailer iframe blocked, showing alternative');
                showTrailerError();
            }
        }, 3000);
        
        // Обработчик ошибки загрузки
        trailerIframe.addEventListener('error', showTrailerError);
        
        // Обработчик успешной загрузки
        trailerIframe.addEventListener('load', function() {
            console.log('Trailer loaded successfully');
        });
    }
});

// Обработка клика по трейлеру
document.addEventListener('click', function(e) {
    if (e.target.closest('.trailer-overlay')) {
        playTrailer();
    }
});