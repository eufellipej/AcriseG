// Navigation system
document.querySelectorAll('nav a, .footer-links a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Update active link
        document.querySelectorAll('nav a').forEach(navLink => {
            navLink.classList.remove('active');
        });
        this.classList.add('active');
        
        // Show corresponding section
        const targetId = this.getAttribute('href').substring(1);
        document.querySelectorAll('main > section').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(targetId).classList.remove('hidden');
        
        // Scroll to top
        window.scrollTo(0, 0);
    });
});

// Carousel functionality
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const dots = document.querySelectorAll('.carousel-dot');

function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => {
        slide.style.display = 'none';
    });
    
    // Remove active class from all dots
    dots.forEach(dot => {
        dot.classList.remove('active');
    });
    
    // Show selected slide and activate dot
    slides[index].style.display = 'flex';
    dots[index].classList.add('active');
    currentSlide = index;
}

// Initialize carousel
showSlide(0);

// Add click events to dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        showSlide(index);
    });
});

// Auto advance carousel
setInterval(() => {
    let nextSlide = (currentSlide + 1) % slides.length;
    showSlide(nextSlide);
}, 5000);

// Form tabs functionality
document.querySelectorAll('.form-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        const tabType = this.getAttribute('data-tab');
        const tabContent = this.getAttribute('data-type');
        
        // Handle main tabs (login/register)
        if (tabType) {
            // Update active tab
            this.parentElement.querySelectorAll('.form-tab').forEach(t => {
                t.classList.remove('active');
            });
            this.classList.add('active');
            
            // Show corresponding content
            document.querySelectorAll('.form-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tabType}-content`).classList.add('active');
        }
        
        // Handle login type tabs (user/admin)
        if (tabContent) {
            // Update active tab
            this.parentElement.querySelectorAll('.form-tab').forEach(t => {
                t.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
});

// Back to top button
const backToTopButton = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'flex';
    } else {
        backToTopButton.style.display = 'none';
    }
});

backToTopButton.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Form submission handling
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show success message
        const alert = document.createElement('div');
        alert.classList.add('alert', 'alert-success');
        alert.textContent = 'Operação realizada com sucesso!';
        
        this.parentNode.insertBefore(alert, this);
        
        // Clear form
        this.reset();
        
        // Remove alert after 3 seconds
        setTimeout(() => {
            alert.remove();
        }, 3000);
    });
});

// Article suggestion toggle
document.getElementById('suggest-article').addEventListener('click', function() {
    const suggestionForm = document.getElementById('article-suggestion');
    suggestionForm.classList.toggle('hidden');
});

// Initialize map
const map = L.map('map').setView([0, 0], 2);

// Add tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add markers for disaster events
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

// Add markers with custom icons
disasters.forEach(disaster => {
    let iconColor;
    let iconSize;
    
    switch(disaster.severity) {
        case 'extreme':
            iconColor = '#e74c3c';
            iconSize = [30, 30];
            break;
        case 'high':
            iconColor = '#f39c12';
            iconSize = [25, 25];
            break;
        default:
            iconColor = '#27ae60';
            iconSize = [20, 20];
    }
    
    const customIcon = L.divIcon({
        className: 'custom-icon',
        html: `<div style="background-color: ${iconColor}; width: ${iconSize[0]}px; height: ${iconSize[1]}px; border-radius: 50%; border: 2px solid white;"></div>`,
        iconSize: iconSize,
        iconAnchor: [iconSize[0]/2, iconSize[1]/2]
    });
    
    const marker = L.marker(disaster.position, {icon: customIcon}).addTo(map);
    marker.bindPopup(`
        <h3>${disaster.name}</h3>
        <p>${disaster.description}</p>
        <p><strong>Tipo:</strong> ${disaster.type}</p>
        <p><strong>Severidade:</strong> ${disaster.severity}</p>
    `);
});

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Show home page by default
    document.getElementById('home').classList.remove('hidden');
});