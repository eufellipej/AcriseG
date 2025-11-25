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

