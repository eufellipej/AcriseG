/**
 * MAIN INITIALIZATION FUNCTION
 * Runs when the DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initCarousel();
    initFormTabs();
    initBackToTop();
    initForms();
    initArticleSuggestion();
    initMap();
    initUserDropdowns();
});

/**
 * INITIALIZE NAVIGATION SYSTEM
 * Handles main navigation and smooth scrolling
 */
function initNavigation() {
    // Main navigation links
    document.querySelectorAll('nav a, .footer-links a').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href.startsWith('#')) {
                e.preventDefault();
                updateActiveNavLink(this);
                
                if (window.location.pathname.endsWith('index.html')) {
                    scrollToSection(href.substring(1));
                }
            }
        });
    });
    
    // Logo link
    const logoLink = document.querySelector('.logo-link');
    if (logoLink) {
        logoLink.addEventListener('click', function(e) {
            if (window.location.pathname.endsWith('index.html')) {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
                updateActiveNavLink(document.querySelector('nav a[href="index.html"]'));
            }
        });
    }
}

function updateActiveNavLink(activeLink) {
    document.querySelectorAll('nav a').forEach(navLink => {
        navLink.classList.remove('active');
    });
    activeLink.classList.add('active');
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * INITIALIZE CAROUSEL FUNCTIONALITY
 */
function initCarousel() {
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.carousel-dot');
    
    if (slides.length === 0) return;

    let currentSlide = 0;
    let slideInterval;

    function showSlide(index) {
        slides.forEach(slide => slide.style.display = 'none');
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[index].style.display = 'flex';
        if (dots[index]) dots[index].classList.add('active');
        currentSlide = index;
    }

    function nextSlide() {
        showSlide((currentSlide + 1) % slides.length);
    }

    // Initialize
    showSlide(0);
    
    // Add click events to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            clearInterval(slideInterval);
            showSlide(index);
            startSlideInterval();
        });
    });
    
    // Auto-advance
    function startSlideInterval() {
        slideInterval = setInterval(nextSlide, 5000);
    }
    
    startSlideInterval();
}

/**
 * INITIALIZE FORM TABS
 */
function initFormTabs() {
    document.querySelectorAll('.form-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const tabType = this.getAttribute('data-tab');
            const tabContent = this.getAttribute('data-type');
            
            if (tabType) {
                this.parentElement.querySelectorAll('.form-tab').forEach(t => {
                    t.classList.remove('active');
                });
                this.classList.add('active');
                
                document.querySelectorAll('.form-content').forEach(content => {
                    content.classList.remove('active');
                });
                const content = document.getElementById(`${tabType}-content`);
                if (content) content.classList.add('active');
            }
            
            if (tabContent) {
                this.parentElement.querySelectorAll('.form-tab').forEach(t => {
                    t.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
}

/**
 * INITIALIZE BACK TO TOP BUTTON
 */
function initBackToTop() {
    const backToTopButton = document.querySelector('.back-to-top');
    
    if (!backToTopButton) return;

    window.addEventListener('scroll', () => {
        backToTopButton.style.display = window.pageYOffset > 300 ? 'flex' : 'none';
    });
    
    backToTopButton.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/**
 * INITIALIZE FORM HANDLING
 */
function initForms() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showFormSuccess(this);
            this.reset();
        });
    });
}

function showFormSuccess(form) {
    const existingAlert = form.parentNode.querySelector('.alert');
    if (existingAlert) existingAlert.remove();
    
    const alert = document.createElement('div');
    alert.classList.add('alert', 'alert-success');
    alert.textContent = 'Operação realizada com sucesso!';
    
    form.parentNode.insertBefore(alert, form);
    
    setTimeout(() => alert.remove(), 3000);
}

/**
 * INITIALIZE ARTICLE SUGGESTION TOGGLE
 */
function initArticleSuggestion() {
    const suggestArticleBtn = document.getElementById('suggest-article');
    if (!suggestArticleBtn) return;

    suggestArticleBtn.addEventListener('click', function() {
        const suggestionForm = document.getElementById('article-suggestion');
        if (suggestionForm) {
            suggestionForm.classList.toggle('hidden');
            if (!suggestionForm.classList.contains('hidden')) {
                suggestionForm.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
}

/**
 * INITIALIZE MAP FUNCTIONALITY
 */
function initMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement || typeof L === 'undefined') return;

    setTimeout(() => {
        const map = L.map('map').setView([0, 0], 2);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        addDisasterMarkers(map);
    }, 100);
}

function addDisasterMarkers(map) {
    const disasters = [
        {
            name: 'Terremoto',
            position: [-8.05, -34.9],
            description: 'Terremoto de magnitude 7.2 na costa',
            type: 'earthquake',
            severity: 'high'
        },
        {
            name: 'Furacão',
            position: [28.5, -80.5],
            description: 'Furacão categoria 4 se aproximando',
            type: 'hurricane',
            severity: 'extreme'
        },
        {
            name: 'Erupção Vulcânica',
            position: [-0.22, -78.51],
            description: 'Erupção ativa no Anel de Fogo',
            type: 'volcano',
            severity: 'medium'
        },
        {
            name: 'Inundação',
            position: [13.75, 100.49],
            description: 'Inundações no Sudeste Asiático',
            type: 'flood',
            severity: 'high'
        },
        {
            name: 'Deslizamento',
            position: [-9.19, -75.02],
            description: 'Deslizamentos nos Andes',
            type: 'landslide',
            severity: 'medium'
        }
    ];
    
    disasters.forEach(disaster => {
        const icon = createDisasterIcon(disaster.severity);
        const marker = L.marker(disaster.position, { icon }).addTo(map);
        
        marker.bindPopup(`
            <h3>${disaster.name}</h3>
            <p>${disaster.description}</p>
            <p><strong>Tipo:</strong> ${disaster.type}</p>
            <p><strong>Severidade:</strong> ${disaster.severity}</p>
        `);
    });
}

function createDisasterIcon(severity) {
    let iconColor, iconSize;
    
    switch(severity) {
        case 'extreme': iconColor = '#e74c3c'; iconSize = [30, 30]; break;
        case 'high': iconColor = '#f39c12'; iconSize = [25, 25]; break;
        default: iconColor = '#27ae60'; iconSize = [20, 20];
    }
    
    return L.divIcon({
        className: 'custom-icon',
        html: `<div style="background-color: ${iconColor}; width: ${iconSize[0]}px; height: ${iconSize[1]}px; border-radius: 50%; border: 2px solid white;"></div>`,
        iconSize: iconSize,
        iconAnchor: [iconSize[0]/2, iconSize[1]/2]
    });
}

/**
 * INITIALIZE USER DROPDOWNS
 */
function initUserDropdowns() {
    // User dropdown
    const userDropdown = document.querySelector('.user-dropdown');
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const content = this.querySelector('.dropdown-content');
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            }
        });
    }
    
    // Admin dropdown
    const adminDropdown = document.querySelector('.admin-dropdown');
    if (adminDropdown) {
        adminDropdown.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const content = this.querySelector('.dropdown-content');
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            }
        });
    }
    
    // Logout button
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Logout realizado com sucesso!');
            window.location.href = 'index.html';
        });
    }
}

