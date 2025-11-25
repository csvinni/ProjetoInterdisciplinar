// doacoes.js
function initDoacoesForm() {
    const tipoDoacaoSelect = document.getElementById('tipo_doacao');
    const secaoDinheiro = document.getElementById('secao-dinheiro');
    const secaoItens = document.getElementById('secao-itens');

    if (!tipoDoacaoSelect) return; // evita erros se o modal não tiver carregado ainda

    const camposDinheiro = secaoDinheiro.querySelectorAll('input, select');
    const camposItens = secaoItens.querySelectorAll('input, select');

    function atualizarSecao() {
        const valorSelecionado = tipoDoacaoSelect.value;

        secaoDinheiro.style.display = 'none';
        secaoItens.style.display = 'none';
        camposDinheiro.forEach(campo => campo.disabled = true);
        camposItens.forEach(campo => campo.disabled = true);

        if (valorSelecionado === 'dinheiro') {
            secaoDinheiro.style.display = 'block';
            camposDinheiro.forEach(campo => campo.disabled = false);
        } else if (valorSelecionado === 'itens') {
            secaoItens.style.display = 'block';
            camposItens.forEach(campo => campo.disabled = false);
        }
    }

    tipoDoacaoSelect.addEventListener('change', atualizarSecao);
    atualizarSecao();
}
