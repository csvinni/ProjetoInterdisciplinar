document.addEventListener('DOMContentLoaded', function() {
    const tipoDoacaoSelect = document.getElementById('tipo_doacao');
    const secaoDinheiro = document.getElementById('secao-dinheiro');
    const secaoItens = document.getElementById('secao-itens');

    // Pega todos os campos de cada seção
    const camposDinheiro = secaoDinheiro.querySelectorAll('input, select');
    const camposItens = secaoItens.querySelectorAll('input, select');

    function atualizarSecao() {
        const valorSelecionado = tipoDoacaoSelect.value;

        // Oculta e desabilita todas as seções
        secaoDinheiro.style.display = 'none';
        secaoItens.style.display = 'none';
        camposDinheiro.forEach(campo => campo.disabled = true);
        camposItens.forEach(campo => campo.disabled = true);

        // Mostra e habilita somente a seção correspondente
        if (valorSelecionado === 'dinheiro') {
            secaoDinheiro.style.display = 'block';
            camposDinheiro.forEach(campo => campo.disabled = false);
        } else if (valorSelecionado === 'itens') {
            secaoItens.style.display = 'block';
            camposItens.forEach(campo => campo.disabled = false);
        }
    }

    tipoDoacaoSelect.addEventListener('change', atualizarSecao);
    atualizarSecao(); // Executa na inicialização
});
