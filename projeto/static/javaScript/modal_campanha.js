document.addEventListener('DOMContentLoaded', () => {
    // 1. Elementos DOM
    const modal = document.getElementById('cadastroCampanhaModal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtns = document.querySelectorAll('.close_button');
    const campanhaForm = document.getElementById('campanhaForm');
    const submitButton = campanhaForm.querySelector('.submit_button');
    const cardsContainer = document.querySelector('.cards-container'); // Onde as campanhas são listadas

    if (!modal || !openBtn || !campanhaForm) {
        console.error("Um ou mais elementos essenciais do modal não foram encontrados.");
        return;
    }

    // --- FUNÇÕES DE CONTROLE DO MODAL ---

    const openModal = () => {
        modal.classList.add('visible');
    };

    const closeModal = () => {
        modal.classList.remove('visible');
        // Opcional: Limpar o formulário ao fechar
        campanhaForm.reset(); 
    };

    // --- LISTENERS DE ABERTURA E FECHAMENTO ---
    
    // Abrir ao clicar no botão 'Cadastrar Nova Campanha'
    openBtn.addEventListener('click', openModal);

    // Fechar ao clicar nos botões de fechar (X)
    closeBtns.forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    // Fechar ao clicar fora do modal (no overlay)
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Fechar ao pressionar a tecla ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('visible')) {
            closeModal();
        }
    });

    // --- FUNÇÃO DE SUBMISSÃO AJAX ---

    campanhaForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Impede a submissão padrão (recarregamento de página)

        // Desabilita o botão para evitar cliques duplicados e mostra feedback de carregamento
        submitButton.textContent = 'Cadastrando...';
        submitButton.disabled = true;

        // Cria o FormData a partir do formulário
        const formData = new FormData(campanhaForm);

        try {
            const response = await fetch(campanhaForm.action, {
                method: 'POST',
                body: formData, // Envia os dados do formulário
            });

            const result = await response.json();

            if (response.ok) {
                // SUCESSO
                alert("Campanha cadastrada com sucesso!"); // Use um modal customizado se possível!
                closeModal();
                
                // Opcional: Atualizar a lista de campanhas no dashboard.
                // Como não temos a função de renderizar um novo card aqui,
                // a solução mais simples é RECARREGAR a página para ver o novo item.
                window.location.reload(); 
                
                // Se o seu app for mais complexo, você deveria chamar uma função
                // para renderizar o 'result.campanha' dentro de 'cardsContainer'.
            } else {
                // ERRO do servidor (ex: validação do FastAPI falhou)
                alert(`Erro ao cadastrar: ${result.detail || result.message || 'Erro desconhecido'}`);
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            alert("Ocorreu um erro de conexão. Tente novamente.");
        } finally {
            // Reabilita o botão
            submitButton.textContent = 'Cadastrar';
            submitButton.disabled = false;
        }
    });

    // Se você usa a função alert() no JavaScript, seria melhor substituí-la
    // por uma função que exibe uma mensagem na tela (como um toast ou um modal 
    // de aviso), já que o `alert()` bloqueia a interface.
});