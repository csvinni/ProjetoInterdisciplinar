document.addEventListener('DOMContentLoaded', function() {
    // 1. Obter referências para os elementos principais
    const tipoDoacaoSelect = document.getElementById('tipo_doacao');
    const secaoDinheiro = document.getElementById('secao-dinheiro');
    const secaoItens = document.getElementById('secao-itens');

    // 2. Função que decide qual seção mostrar
    function atualizarSecao() {
        const valorSelecionado = tipoDoacaoSelect.value;
        
        // Esconde ambas por padrão antes de mostrar a correta
        secaoDinheiro.style.display = 'none';
        secaoItens.style.display = 'none';

        if (valorSelecionado === 'dinheiro') {
            secaoDinheiro.style.display = 'block';
        } else if (valorSelecionado === 'itens') {
            secaoItens.style.display = 'block';
        }
    }

    // 3. Adicionar um "ouvinte" de evento (listener) no select
    tipoDoacaoSelect.addEventListener('change', atualizarSecao);

    // 4. Executar a função na primeira vez que a página carrega 
    // (útil se o usuário recarregar com uma opção já selecionada, ou para manter escondido inicialmente)
    atualizarSecao();
});