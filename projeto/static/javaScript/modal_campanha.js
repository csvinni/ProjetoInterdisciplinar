// =======================================================
// 1. FUNÇÃO GLOBAL (Para ser acessível pelo onclick do HTML)
// =======================================================
window.openEditModal = (
    id, 
    titulo, 
    descricao, 
    meta_financeira, 
    meta_itens, 
    data_inicio, // Formato YYYY-MM-DD
    data_fim,    // Formato YYYY-MM-DD
    status
) => {
    // Estas variáveis (modal, campanhaForm, etc.) SÓ EXISTIRÃO DEPOIS DO DOMContentLoaded.
    // Usaremos as IDs dos elementos diretamente aqui, pois é uma função global.
    const modal = document.getElementById('cadastroCampanhaModal');
    const campanhaForm = document.getElementById('campanhaForm');
    
    if (!modal || !campanhaForm) {
        console.error("Erro: Elementos do modal não encontrados. Certifique-se de que openEditModal só é chamado após o DOM carregar.");
        return;
    }

    const submitButton = campanhaForm.querySelector('.submit_button');
    
    // 1. Configura o formulário para o MODO EDIÇÃO
    modal.querySelector('.header h2').textContent = `Edição da Campanha #${id}`;
    submitButton.textContent = 'Salvar Edição';
    
    // 2. Altera a URL de ação do formulário para o novo endpoint POST de edição
    campanhaForm.action = `/campanhas/editar/${id}`;
    
    // 3. Preenche os campos do formulário
    document.getElementById('titulo').value = titulo;
    document.getElementById('descricao').value = descricao;
    document.getElementById('meta_financeira').value = meta_financeira;
    document.getElementById('meta_itens').value = meta_itens;
    document.getElementById('data_inicio').value = data_inicio;
    document.getElementById('data_fim').value = data_fim;
    
    // 4. Marca o status correto
    const statusRadios = campanhaForm.querySelectorAll('input[name="status"]');
    statusRadios.forEach(radio => {
        if (radio.value.toLowerCase() === status.toLowerCase()) {
            radio.checked = true;
        } else {
            radio.checked = false;
        }
    });

    // 5. Abre o modal (usando a classe 'visible')
    modal.classList.add('visible');
};

// =======================================================
// 2. LÓGICA DE CONTROLE DO MODAL E SUBMISSÃO (DOM Content Loaded)
// =======================================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Elementos DOM (Estão seguros aqui)
    const modal = document.getElementById('cadastroCampanhaModal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtns = document.querySelectorAll('.close_button');
    const campanhaForm = document.getElementById('campanhaForm');
    const submitButton = campanhaForm.querySelector('.submit_button');
    const cardsContainer = document.querySelector('.cards-container'); 

    if (!modal || !openBtn || !campanhaForm) {
        console.error("Um ou mais elementos essenciais do modal não foram encontrados.");
        return;
    }

    // --- FUNÇÕES INTERNAS (Acesso apenas dentro do DOMContentLoaded) ---

    // Função para limpar e configurar o formulário para MODO CADASTRO
    const resetFormForCadastro = () => {
        campanhaForm.reset(); 
        campanhaForm.action = '/campanhas/cadastro_campanha';
        modal.querySelector('.header h2').textContent = 'Cadastro campanha';
        submitButton.textContent = 'Cadastrar';
    };

    const closeModal = () => {
        modal.classList.remove('visible');
        resetFormForCadastro(); 
    };
    
    // --- LISTENERS ---
    
    // Abrir ao clicar no botão 'Cadastrar Nova Campanha'
    openBtn.addEventListener('click', () => {
        resetFormForCadastro(); 
        modal.classList.add('visible'); // Usa a lógica simples de abrir
    });

    // Fechar listeners
    closeBtns.forEach(btn => {
        btn.addEventListener('click', closeModal);
    });
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('visible')) {
            closeModal();
        }
    });

    // --- FUNÇÃO DE SUBMISSÃO AJAX ---

    campanhaForm.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        const isEditing = campanhaForm.action.includes('/editar/');
        
        submitButton.textContent = isEditing ? 'Salvando...' : 'Cadastrando...';
        submitButton.disabled = true;

        const formData = new FormData(campanhaForm);

        try {
            const response = await fetch(campanhaForm.action, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                const successMsg = isEditing ? "Campanha atualizada com sucesso!" : "Campanha cadastrada com sucesso!";
                alert(successMsg); 
                closeModal();
                window.location.reload(); 
            } else {
                alert(`Erro ao ${isEditing ? 'atualizar' : 'cadastrar'}: ${result.detail || result.message || 'Erro desconhecido'}`);
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            alert("Ocorreu um erro de conexão. Tente novamente.");
        } finally {
            submitButton.disabled = false;
        }
    });
});
