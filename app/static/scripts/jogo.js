// Funções específicas para a página do jogo
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar FAQ
    initFAQ();

    // Destacar item ativo no menu
    setActiveNavLink();

    // Adicionar funcionalidade aos botões de download
    initDownloadButtons();

    // Inicializar funcionalidade de logout
    initLogout();
});

function initFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', function () {
            const faqItem = this.parentElement;
            faqItem.classList.toggle('active');
        });
    });
}

function setActiveNavLink() {
    const navLinks = document.querySelectorAll('nav a');
    const currentPage = window.location.pathname.split('/').pop();

    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

function initDownloadButtons() {
    const downloadButtons = document.querySelectorAll('.btn');

    downloadButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            alert('O download será iniciado em breve. Enquanto isso, continue explorando nosso jogo!');
        });
    });
}

function initLogout() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            alert('Logout realizado com sucesso!');
            window.location.href = 'index.html';
        });
    }
}