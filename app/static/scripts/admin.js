// admin.js - Funcionalidades do Painel Administrativo

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initMobileMenu();
    initDropdowns();
    initModals();
    initFilters();
    initTables();
    initCharts();
    initActions();
    initSearch();
    
    // Atualizar estatísticas periodicamente
    updateStats();
    setInterval(updateStats, 60000); // Atualizar a cada minuto
    
    // Adicionar estilos CSS dinâmicos
    addDynamicStyles();
});

// Menu Mobile
function initMobileMenu() {
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const sidebar = document.querySelector('.admin-sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
        
        // Fechar menu ao clicar fora
        document.addEventListener('click', function(event) {
            if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
}

// Dropdowns
function initDropdowns() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const dropdown = this.nextElementSibling;
            dropdown.classList.toggle('show');
        });
    });
    
    // Fechar dropdowns ao clicar fora
    document.addEventListener('click', function() {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('show');
        });
    });
}

// Modais
function initModals() {
    const modals = document.querySelectorAll('.admin-modal');
    const closeButtons = document.querySelectorAll('.modal-close');
    
    // Fechar modal
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.admin-modal').classList.remove('active');
        });
    });
    
    // Fechar modal ao clicar fora
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.admin-modal').forEach(modal => {
                modal.classList.remove('active');
            });
        }
    });
    
    // Botões para abrir modais
    document.querySelectorAll('[data-action="edit"]').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.id;
            openEditUserModal(userId);
        });
    });
    
    document.querySelectorAll('[data-action="view"]').forEach(button => {
        button.addEventListener('click', function() {
            const questionId = this.dataset.id;
            openViewQuestionModal(questionId);
        });
    });
    
    document.querySelectorAll('[data-action="delete"]').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.id;
            const userName = this.closest('tr').querySelector('td:nth-child(2)').textContent.trim();
            openConfirmModal('Excluir Usuário', `Tem certeza que deseja excluir o usuário "${userName}"? Esta ação não pode ser desfeita.`, () => {
                deleteUser(userId);
            });
        });
    });
    
    // Botões de cancelar
    document.getElementById('cancelEdit')?.addEventListener('click', function() {
        document.getElementById('editUserModal').classList.remove('active');
    });
    
    document.getElementById('cancelView')?.addEventListener('click', function() {
        document.getElementById('viewQuestionModal').classList.remove('active');
    });
    
    document.getElementById('confirmCancel')?.addEventListener('click', function() {
        document.getElementById('confirmModal').classList.remove('active');
    });
    
    // Botão Adicionar Usuário
    document.getElementById('addUserBtn')?.addEventListener('click', function() {
        openAddUserModal();
    });
    
    // Botão Atualizar Perguntas
    document.getElementById('refreshQuestions')?.addEventListener('click', function() {
        updateQuestions();
    });
}

// Filtros
function initFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            applyFilters();
        });
    });
}

function applyFilters() {
    const userType = document.getElementById('filterUserType')?.value;
    const userStatus = document.getElementById('filterUserStatus')?.value;
    const questionStatus = document.getElementById('filterStatus')?.value;
    const questionGame = document.getElementById('filterGame')?.value;
    
    // Filtrar tabela de usuários
    if (userType || userStatus) {
        filterUserTable(userType, userStatus);
    }
    
    // Filtrar tabela de perguntas
    if (questionStatus || questionGame) {
        filterQuestionTable(questionStatus, questionGame);
    }
}

function filterUserTable(type, status) {
    const rows = document.querySelectorAll('.admin-table tbody tr');
    
    rows.forEach(row => {
        const userTypeCell = row.querySelector('td:nth-child(4)');
        const userStatusCell = row.querySelector('td:nth-child(6)');
        
        if (!userTypeCell || !userStatusCell) return;
        
        const userType = userTypeCell.textContent.toLowerCase();
        const userStatus = userStatusCell.textContent.toLowerCase();
        
        let show = true;
        
        if (type !== 'all') {
            if (type === 'admin' && !userType.includes('admin')) show = false;
            if (type === 'editor' && !userType.includes('editor')) show = false;
            if (type === 'user' && !userType.includes('usuário')) show = false;
        }
        
        if (status !== 'all') {
            if (status === 'active' && !userStatus.includes('ativo')) show = false;
            if (status === 'inactive' && !userStatus.includes('inativo')) show = false;
            if (status === 'pending' && !userStatus.includes('pendente')) show = false;
        }
        
        row.style.display = show ? '' : 'none';
    });
}

function filterQuestionTable(status, game) {
    const rows = document.querySelectorAll('.admin-table tbody tr');
    
    rows.forEach(row => {
        const questionStatusCell = row.querySelector('td:nth-child(6)');
        const questionGameCell = row.querySelector('td:nth-child(4)');
        
        if (!questionStatusCell || !questionGameCell) return;
        
        const questionStatus = questionStatusCell.textContent.toLowerCase();
        const questionGame = questionGameCell.textContent.toLowerCase();
        
        let show = true;
        
        if (status !== 'all') {
            if (status === 'pending' && !questionStatus.includes('pendente')) show = false;
            if (status === 'answered' && !questionStatus.includes('respondida')) show = false;
            if (status === 'published' && !questionStatus.includes('publicada')) show = false;
        }
        
        if (game !== 'all') {
            if (!questionGame.includes(game.toLowerCase())) show = false;
        }
        
        row.style.display = show ? '' : 'none';
    });
}

// Tabelas
function initTables() {
    // Selecionar todos
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.user-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Adicionar efeito hover nas linhas
    const rows = document.querySelectorAll('.admin-table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.02)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Gráficos
function initCharts() {
    // Gráfico de usuários
    const usersCtx = document.getElementById('usersChart');
    if (usersCtx) {
        const usersChart = new Chart(usersCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Novos Usuários',
                    data: [12, 19, 8, 15, 12, 18, 15],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#f8fafc'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                }
            }
        });
        
        // Armazenar referência do gráfico
        window.usersChart = usersChart;
    }
    
    // Gráfico de distribuição
    const distributionCtx = document.getElementById('distributionChart');
    if (distributionCtx) {
        const distributionChart = new Chart(distributionCtx, {
            type: 'doughnut',
            data: {
                labels: ['Administradores', 'Editores', 'Usuários'],
                datasets: [{
                    data: [3, 5, 148],
                    backgroundColor: [
                        '#ef4444',
                        '#3b82f6',
                        '#10b981'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#f8fafc',
                            padding: 20
                        }
                    }
                }
            }
        });
        
        // Armazenar referência do gráfico
        window.distributionChart = distributionChart;
    }
}

// Ações
function initActions() {
    // Salvar usuário
    document.getElementById('saveUser')?.addEventListener('click', function() {
        const form = document.getElementById('editUserForm');
        if (form && form.checkValidity()) {
            saveUser();
        } else if (form) {
            form.reportValidity();
        }
    });
    
    // Enviar resposta
    document.getElementById('sendResponse')?.addEventListener('click', function() {
        const response = document.getElementById('questionResponse')?.value;
        if (response && response.trim()) {
            sendResponse(response);
        } else {
            showNotification('Por favor, digite uma resposta.', 'warning');
        }
    });
    
    // Aprovar pergunta
    document.querySelectorAll('[data-action="approve"]').forEach(button => {
        button.addEventListener('click', function() {
            const questionId = this.dataset.id;
            const questionText = this.closest('tr').querySelector('td:nth-child(3)').textContent.trim();
            openConfirmModal('Aprovar Pergunta', `Deseja aprovar esta pergunta e publicar como FAQ?`, () => {
                approveQuestion(questionId);
            });
        });
    });
    
    // Rejeitar pergunta
    document.querySelectorAll('[data-action="reject"]').forEach(button => {
        button.addEventListener('click', function() {
            const questionId = this.dataset.id;
            const questionText = this.closest('tr').querySelector('td:nth-child(3)').textContent.trim();
            openConfirmModal('Rejeitar Pergunta', `Deseja rejeitar esta pergunta?`, () => {
                rejectQuestion(questionId);
            });
        });
    });
    
    // Confirmar ação
    document.getElementById('confirmAction')?.addEventListener('click', function() {
        const callback = this._callback;
        if (callback) {
            callback();
        }
    });
}

// Busca
function initSearch() {
    const searchInput = document.querySelector('.admin-search input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.admin-table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        }, 300));
    }
}

// Funções para abrir modais
function openEditUserModal(userId) {
    const modal = document.getElementById('editUserModal');
    const row = document.querySelector(`[data-id="${userId}"]`)?.closest('tr');
    
    if (row && modal) {
        const nome = row.querySelector('td:nth-child(2)').textContent.trim();
        const email = row.querySelector('td:nth-child(3)').textContent.trim();
        const tipo = row.querySelector('td:nth-child(4)').textContent.trim();
        const status = row.querySelector('td:nth-child(6)').textContent.trim();
        
        const nameInput = document.getElementById('editUserName');
        const emailInput = document.getElementById('editUserEmail');
        const typeSelect = document.getElementById('editUserType');
        const statusSelect = document.getElementById('editUserStatus');
        
        if (nameInput) nameInput.value = nome;
        if (emailInput) emailInput.value = email;
        if (typeSelect) {
            typeSelect.value = tipo.toLowerCase().includes('admin') ? 'admin' : 
                              tipo.toLowerCase().includes('editor') ? 'editor' : 'user';
        }
        if (statusSelect) {
            statusSelect.value = status.toLowerCase().includes('ativo') ? 'active' : 
                                status.toLowerCase().includes('inativo') ? 'inactive' : 'pending';
        }
        
        modal.classList.add('active');
    }
}

function openAddUserModal() {
    const modal = document.getElementById('editUserModal');
    const nameInput = document.getElementById('editUserName');
    const emailInput = document.getElementById('editUserEmail');
    const typeSelect = document.getElementById('editUserType');
    const statusSelect = document.getElementById('editUserStatus');
    
    if (modal) {
        if (nameInput) nameInput.value = '';
        if (emailInput) emailInput.value = '';
        if (typeSelect) typeSelect.value = 'user';
        if (statusSelect) statusSelect.value = 'active';
        
        modal.classList.add('active');
    }
}

function openViewQuestionModal(questionId) {
    const modal = document.getElementById('viewQuestionModal');
    const row = document.querySelector(`[data-id="${questionId}"]`)?.closest('tr');
    
    if (row && modal) {
        const user = row.querySelector('td:nth-child(2)').textContent.trim();
        const question = row.querySelector('td:nth-child(3)').textContent.trim();
        const game = row.querySelector('td:nth-child(4)').textContent.trim();
        const date = row.querySelector('td:nth-child(5)').textContent.trim();
        
        const userSpan = document.getElementById('questionUser');
        const questionText = document.getElementById('questionText');
        const gameSpan = document.getElementById('questionGame');
        const dateSpan = document.getElementById('questionDate');
        
        if (userSpan) userSpan.textContent = user;
        if (questionText) questionText.textContent = question;
        if (gameSpan) gameSpan.textContent = game;
        if (dateSpan) dateSpan.textContent = date;
        
        const responseTextarea = document.getElementById('questionResponse');
        if (responseTextarea) responseTextarea.value = '';
        
        modal.classList.add('active');
    }
}

function openConfirmModal(title, message, callback) {
    const modal = document.getElementById('confirmModal');
    const titleElement = document.getElementById('confirmTitle');
    const messageElement = document.getElementById('confirmMessage');
    const confirmBtn = document.getElementById('confirmAction');
    
    if (modal && titleElement && messageElement && confirmBtn) {
        titleElement.textContent = title;
        messageElement.textContent = message;
        confirmBtn._callback = callback;
        modal.classList.add('active');
    }
}

// Funções de API
function updateStats() {
    fetch('/admin-api/get_stats/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            // Atualizar estatísticas na interface
            updateStatCards(data);
        })
        .catch(error => {
            console.error('Erro ao atualizar estatísticas:', error);
        });
}

function updateStatCards(data) {
    // Atualizar os cartões de estatística com dados reais
    const statCards = document.querySelectorAll('.stat-card-value');
    statCards.forEach(card => {
        const title = card.closest('.stat-card')?.querySelector('.stat-card-title')?.textContent;
        if (title) {
            if (title.includes('Usuários')) {
                card.textContent = data.total_usuarios || 0;
            } else if (title.includes('Artigos')) {
                card.textContent = data.total_artigos || 0;
            } else if (title.includes('Desastres')) {
                card.textContent = data.total_desastres || 0;
            } else if (title.includes('Jogos')) {
                card.textContent = data.total_jogos || 0;
            } else if (title.includes('Perguntas')) {
                card.textContent = data.perguntas_pendentes || 0;
            }
        }
    });
}

function saveUser() {
    const name = document.getElementById('editUserName')?.value;
    const email = document.getElementById('editUserEmail')?.value;
    const type = document.getElementById('editUserType')?.value;
    const status = document.getElementById('editUserStatus')?.value;
    
    if (!name || !email || !type || !status) {
        showNotification('Por favor, preencha todos os campos.', 'error');
        return;
    }
    
    // Simular salvamento
    showNotification('Salvando usuário...', 'info');
    
    setTimeout(() => {
        showNotification('Usuário salvo com sucesso!', 'success');
        const modal = document.getElementById('editUserModal');
        if (modal) modal.classList.remove('active');
        
        // Recarregar página após 1 segundo
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }, 1000);
}

function deleteUser(userId) {
    // Simular exclusão
    showNotification('Excluindo usuário...', 'info');
    
    setTimeout(() => {
        showNotification('Usuário excluído com sucesso!', 'success');
        const modal = document.getElementById('confirmModal');
        if (modal) modal.classList.remove('active');
        
        // Remover linha da tabela
        const row = document.querySelector(`[data-id="${userId}"]`)?.closest('tr');
        if (row) {
            row.style.opacity = '0.5';
            row.style.transform = 'translateX(20px)';
            setTimeout(() => {
                row.remove();
                showNotification('Linha removida da tabela.', 'info');
            }, 500);
        }
    }, 1000);
}

function sendResponse(response) {
    // Simular envio de resposta
    showNotification('Enviando resposta...', 'info');
    
    setTimeout(() => {
        showNotification('Resposta enviada com sucesso!', 'success');
        const modal = document.getElementById('viewQuestionModal');
        if (modal) modal.classList.remove('active');
        
        // Aqui você pode atualizar a linha correspondente
        showNotification('Status da pergunta atualizado.', 'info');
    }, 1000);
}

function approveQuestion(questionId) {
    // Simular aprovação
    showNotification('Aprovando pergunta...', 'info');
    
    setTimeout(() => {
        showNotification('Pergunta aprovada e publicada como FAQ!', 'success');
        const modal = document.getElementById('confirmModal');
        if (modal) modal.classList.remove('active');
        
        // Atualizar status na tabela
        const row = document.querySelector(`[data-id="${questionId}"]`)?.closest('tr');
        if (row) {
            const statusCell = row.querySelector('td:nth-child(6)');
            if (statusCell) {
                statusCell.innerHTML = '<span class="badge badge-published">Publicada</span>';
            }
        }
    }, 1000);
}

function rejectQuestion(questionId) {
    // Simular rejeição
    showNotification('Rejeitando pergunta...', 'info');
    
    setTimeout(() => {
        showNotification('Pergunta rejeitada!', 'error');
        const modal = document.getElementById('confirmModal');
        if (modal) modal.classList.remove('active');
        
        // Atualizar status na tabela
        const row = document.querySelector(`[data-id="${questionId}"]`)?.closest('tr');
        if (row) {
            const statusCell = row.querySelector('td:nth-child(6)');
            if (statusCell) {
                statusCell.innerHTML = '<span class="badge">Rejeitada</span>';
            }
        }
    }, 1000);
}

function updateQuestions() {
    showNotification('Atualizando perguntas...', 'info');
    
    setTimeout(() => {
        showNotification('Perguntas atualizadas com sucesso!', 'success');
        // Aqui você pode recarregar os dados da tabela
    }, 1000);
}

// Utilitários
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationsContainer') || createNotificationsContainer();
    
    const notification = document.createElement('div');
    notification.className = `admin-notification`;
    notification.innerHTML = `
        <div class="notification-icon ${type}">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 
                              type === 'error' ? 'exclamation-circle' : 
                              type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${type === 'success' ? 'Sucesso' : 
                                           type === 'error' ? 'Erro' : 
                                           type === 'warning' ? 'Aviso' : 'Informação'}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    container.appendChild(notification);
    
    // Fechar notificação
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            notification.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 5000);
}

function createNotificationsContainer() {
    const container = document.createElement('div');
    container.id = 'notificationsContainer';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    document.body.appendChild(container);
    return container;
}

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

function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .admin-notification {
            animation: slideIn 0.3s ease forwards;
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .slide-in {
            animation: slideInLeft 0.3s ease forwards;
        }
        
        @keyframes slideInLeft {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .loading {
            position: relative;
            opacity: 0.7;
            pointer-events: none;
        }
        
        .loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            border: 2px solid var(--admin-border);
            border-top-color: var(--admin-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: -10px;
            margin-top: -10px;
        }
    `;
    document.head.appendChild(style);
}

// Exportar funções para uso global
window.AdminPanel = {
    showNotification,
    openEditUserModal,
    openViewQuestionModal,
    openConfirmModal,
    updateStats,
    initCharts,
    initModals
};

// Inicializar quando a página estiver completamente carregada
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        window.AdminPanel.initCharts();
        window.AdminPanel.initModals();
    });
} else {
    window.AdminPanel.initCharts();
    window.AdminPanel.initModals();
}