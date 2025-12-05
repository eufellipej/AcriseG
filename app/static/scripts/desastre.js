// static/scripts/desastre.js

// Funções para a página de detalhes do desastre
function inicializarDesastre() {
    console.log('Página de desastre inicializada');
    
    // Configurar tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', mostrarTooltip);
        element.addEventListener('mouseleave', esconderTooltip);
    });
    
    // Configurar filtros de categoria
    const filtrosCategoria = document.querySelectorAll('.filtro-categoria');
    filtrosCategoria.forEach(filtro => {
        filtro.addEventListener('click', filtrarPorCategoria);
    });
    
    // Configurar botão de imprimir guia
    const btnImprimir = document.getElementById('imprimir-guia');
    if (btnImprimir) {
        btnImprimir.addEventListener('click', imprimirGuia);
    }
    
    // Configurar sistema de avaliação
    const estrelas = document.querySelectorAll('.estrela-avaliacao');
    estrelas.forEach(estrela => {
        estrela.addEventListener('click', avaliarConteudo);
        estrela.addEventListener('mouseenter', previewAvaliacao);
        estrela.addEventListener('mouseleave', resetPreviewAvaliacao);
    });
    
    // Configurar sistema de comentários
    const formComentario = document.getElementById('form-comentario');
    if (formComentario) {
        formComentario.addEventListener('submit', enviarComentario);
    }
    
    // Inicializar mapa de risco (se existir)
    const mapaContainer = document.getElementById('mapa-risco');
    if (mapaContainer) {
        inicializarMapaRisco();
    }
}

// Funções auxiliares
function mostrarTooltip(e) {
    const elemento = e.target;
    const texto = elemento.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = texto;
    
    document.body.appendChild(tooltip);
    
    const rect = elemento.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
}

function esconderTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

function filtrarPorCategoria(e) {
    e.preventDefault();
    const categoria = e.target.getAttribute('data-categoria');
    
    // Remover classe ativa de todos os filtros
    document.querySelectorAll('.filtro-categoria').forEach(filtro => {
        filtro.classList.remove('ativo');
    });
    
    // Adicionar classe ativa ao filtro clicado
    e.target.classList.add('ativo');
    
    // Filtrar conteúdo
    const conteudos = document.querySelectorAll('.conteudo-filtravel');
    conteudos.forEach(conteudo => {
        const categoriasConteudo = conteudo.getAttribute('data-categorias').split(' ');
        
        if (categoria === 'todos' || categoriasConteudo.includes(categoria)) {
            conteudo.style.display = 'block';
            setTimeout(() => {
                conteudo.style.opacity = '1';
                conteudo.style.transform = 'translateY(0)';
            }, 10);
        } else {
            conteudo.style.opacity = '0';
            conteudo.style.transform = 'translateY(20px)';
            setTimeout(() => {
                conteudo.style.display = 'none';
            }, 300);
        }
    });
}

function imprimirGuia() {
    const conteudo = document.querySelector('.conteudo-esquerda').innerHTML;
    const janelaImpressao = window.open('', '_blank');
    
    janelaImpressao.document.write(`
        <html>
            <head>
                <title>Guia - ${document.title}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1, h2, h3 { color: #333; }
                    .lista-detalhes li { margin-bottom: 10px; }
                    .passo-item { margin-bottom: 20px; }
                    .no-print { display: none; }
                    @media print {
                        body { font-size: 12pt; }
                        .page-break { page-break-before: always; }
                    }
                </style>
            </head>
            <body>
                <h1>${document.title}</h1>
                ${conteudo}
                <div class="page-break"></div>
                <p><small>Impresso em ${new Date().toLocaleDateString()} - Fonte: A Crise G</small></p>
            </body>
        </html>
    `);
    
    janelaImpressao.document.close();
    janelaImpressao.focus();
    
    setTimeout(() => {
        janelaImpressao.print();
    }, 500);
}

function avaliarConteudo(e) {
    const estrela = e.target;
    const valor = estrela.getAttribute('data-valor');
    const container = estrela.closest('.avaliacao-container');
    
    // Atualizar visualização
    const estrelas = container.querySelectorAll('.estrela-avaliacao');
    estrelas.forEach((estrela, index) => {
        if (index < valor) {
            estrela.classList.add('ativa');
            estrela.innerHTML = '★';
        } else {
            estrela.classList.remove('ativa');
            estrela.innerHTML = '☆';
        }
    });
    
    // Enviar avaliação (simulação)
    fetch('/api/avaliar-desastre/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            desastre_id: container.getAttribute('data-desastre-id'),
            nota: valor,
            comentario: ''
        })
    })
    .then(response => response.json())
    .then(data => {
        mostrarNotificacao('Avaliação enviada com sucesso!', 'sucesso');
    })
    .catch(error => {
        console.error('Erro:', error);
        mostrarNotificacao('Erro ao enviar avaliação', 'erro');
    });
}

function previewAvaliacao(e) {
    const estrela = e.target;
    const valor = estrela.getAttribute('data-valor');
    const container = estrela.closest('.avaliacao-container');
    
    const estrelas = container.querySelectorAll('.estrela-avaliacao');
    estrelas.forEach((estrela, index) => {
        if (index < valor) {
            estrela.classList.add('preview');
        } else {
            estrela.classList.remove('preview');
        }
    });
}

function resetPreviewAvaliacao(e) {
    const container = e.target.closest('.avaliacao-container');
    const estrelas = container.querySelectorAll('.estrela-avaliacao');
    estrelas.forEach(estrela => {
        estrela.classList.remove('preview');
    });
}

function enviarComentario(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const comentario = formData.get('comentario');
    
    if (!comentario.trim()) {
        mostrarNotificacao('Por favor, digite um comentário', 'alerta');
        return;
    }
    
    // Simulação de envio
    mostrarNotificacao('Comentário enviado para moderação', 'info');
    form.reset();
    
    // Atualizar contador de caracteres
    const contador = form.querySelector('.contador-caracteres span');
    if (contador) {
        contador.textContent = '0';
    }
}

function inicializarMapaRisco() {
    // Verificar se o Leaflet está carregado
    if (typeof L === 'undefined') {
        console.error('Leaflet não está carregado');
        return;
    }
    
    const mapa = L.map('mapa-risco').setView([-15, -55], 4);
    
    // Adicionar camada base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(mapa);
    
    // Adicionar marcadores de exemplo
    const marcadores = [
        { lat: -23.55, lng: -46.63, titulo: 'São Paulo', risco: 'alto' },
        { lat: -22.90, lng: -43.17, titulo: 'Rio de Janeiro', risco: 'médio' },
        { lat: -19.92, lng: -43.99, titulo: 'Belo Horizonte', risco: 'baixo' },
        { lat: -30.03, lng: -51.23, titulo: 'Porto Alegre', risco: 'médio' },
        { lat: -3.73, lng: -38.52, titulo: 'Fortaleza', risco: 'alto' }
    ];
    
    marcadores.forEach(local => {
        const cor = local.risco === 'alto' ? '#e74c3c' : local.risco === 'médio' ? '#f39c12' : '#27ae60';
        
        const marcador = L.circleMarker([local.lat, local.lng], {
            radius: 10,
            fillColor: cor,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(mapa);
        
        marcador.bindPopup(`
            <strong>${local.titulo}</strong><br>
            Risco: ${local.risco.toUpperCase()}<br>
            <small>Clique para mais informações</small>
        `);
    });
    
    // Adicionar controle de camadas
    L.control.layers({}, {
        'Áreas de Risco': mapa
    }).addTo(mapa);
}

// Funções utilitárias
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function mostrarNotificacao(mensagem, tipo = 'info') {
    const container = document.getElementById('notificacoes-container');
    if (!container) return;
    
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao ${tipo}`;
    notificacao.innerHTML = `
        <i class="fas fa-${tipo === 'sucesso' ? 'check-circle' : tipo === 'erro' ? 'exclamation-circle' : 'info-circle'}"></i>
        <div class="conteudo">${mensagem}</div>
        <button class="btn-fechar-notificacao">&times;</button>
    `;
    
    container.appendChild(notificacao);
    
    // Animação de entrada
    setTimeout(() => {
        notificacao.classList.add('ativo');
    }, 10);
    
    // Configurar botão de fechar
    notificacao.querySelector('.btn-fechar-notificacao').addEventListener('click', () => {
        notificacao.classList.remove('ativo');
        setTimeout(() => {
            notificacao.remove();
        }, 300);
    });
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (notificacao.parentNode) {
            notificacao.classList.remove('ativo');
            setTimeout(() => {
                if (notificacao.parentNode) {
                    notificacao.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', inicializarDesastre);

// Exportar funções para uso global
window.DesastreUtils = {
    mostrarNotificacao,
    inicializarMapaRisco,
    imprimirGuia
};