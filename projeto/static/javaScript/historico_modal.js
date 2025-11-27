document.addEventListener("DOMContentLoaded", () => {

    // 🔹 Seleciona o modal
    const historicoModal = document.getElementById("historicoModal");
    const closeHistorico = document.getElementById("closeHistorico");
    const historicoContent = document.getElementById("historicoContent");

    console.log("Modal encontrado?", historicoModal);
    console.log("Botão fechar?", closeHistorico);
    console.log("Conteúdo?", historicoContent);

    // Se algum elemento não existe → PARA TUDO
    if (!historicoModal || !closeHistorico || !historicoContent) {
        console.error("❌ ERRO: Elementos do modal não foram encontrados no HTML!");
        return;
    }

    // 🔹 Abre o modal quando clicar no botão de visualizar
    document.querySelectorAll(".btn-visualizar").forEach(button => {
        button.addEventListener("click", async () => {
            const campanhaId = button.getAttribute("data-id");

            try {
                const response = await fetch(`/doacoes/campanha/${campanhaId}`);

                if (!response.ok) {
                    throw new Error("Erro ao buscar doações");
                }

                const dados = await response.json();

                if (dados.length === 0) {
                    historicoContent.innerHTML = `
                        <p style="text-align: center; padding: 10px;">
                            Nenhuma doação registrada para esta campanha.
                        </p>
                    `;
                } else {
                    historicoContent.innerHTML = dados.map(item => `
                        <div class="doacao-item">
                            <p><strong>Doador:</strong> ${item.doador}</p>
                            <p><strong>Tipo:</strong> ${item.tipo}</p>
                            <p><strong>Quantidade:</strong> ${item.quantidade}</p>
                            <p><strong>Valor:</strong> R$ ${item.valor ?? "0,00"}</p>
                            <hr>
                        </div>
                    `).join("");
                }

                historicoModal.classList.remove("hidden");

            } catch (error) {
                historicoContent.innerHTML = `
                    <p style="color: red; text-align: center;">
                        Erro ao carregar histórico.
                    </p>
                `;
            }
        });
    });

    // 🔹 Fechar modal
    closeHistorico.addEventListener("click", () => {
        historicoModal.classList.add("hidden");
    });
});
