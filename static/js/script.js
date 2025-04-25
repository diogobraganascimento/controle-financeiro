/**
 * Exibe ou oculta o campo de data agendada com base na opção selecionada em um select.
 *
 * Se o valor selecionado for "Agendado", o campo de data será exibido.
 * Caso contrário, ele será ocultado e seu valor será limpo.
 *
 * @param {HTMLSelectElement} selectElement - O elemento <select> que acionou a mudança.
 * @param {number|string} id - O identificador único do item, usado para localizar o campo de data correspondente.
 */
function toggleDataAgendada(selectElement, id) {
    const input = document.getElementById(`dataAgendada${id}`);
    if (!input) return;

    const isAgendado = selectElement.value === "Agendado";
    input.style.display = isAgendado ? "block" : "none";
    if (!isAgendado) {
        input.value = ""; // Limpa a data se não for "Agendado"
    }
}


/**
 * Plugin Chart.js: textoCentral
 *
 * Exibe um texto centralizado no meio de gráficos do tipo pizza ou doughnut.
 * Mostra a palavra "Total" e o valor total formatado como moeda.
 *
 * @property {string} id - Identificador único do plugin.
 * @property {Function} beforeDraw - Executado antes do desenho do gráfico.
 *                                   Responsável por renderizar os textos centralizados.
 */
const textoCentral = {
    id: 'textoCentral',
    beforeDraw(chart, arg, options) {
        const { width, height, ctx } = chart;
        const centerX = width / 2;
        const centerY = height / 2;
        const total = options.total || 0;

        ctx.restore();

        // Texto superior ("Total")
        ctx.font = `bold 18px sans-serif`;
        ctx.fillStyle = '#555';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Total', centerX, centerY - 12);

        // Texto inferior (valor formatado)
        ctx.font = 'bold 20px sans-serif';
        ctx.fillStyle = '#000';

        ctx.fillText(`R$ ${total.toFixed(2)}`, centerX, centerY + 16);
        ctx.save();
    }
};

/**
 * Inicializa os gráficos de Créditos, Débitos e o gráfico comparativo entre Créditos e Débitos quando o DOM estiver completamente carregado.
 *
 * - Cria dois gráficos do tipo "doughnut": um para os Créditos e outro para os Débitos, usando os dados fornecidos.
 * - O gráfico de Créditos exibe a distribuição dos valores de crédito com diferentes cores.
 * - O gráfico de Débitos exibe a distribuição dos valores de débito com diferentes cores.
 * - Ambos os gráficos possuem um plugin customizado (textoCentral) para exibir o total correspondente no centro do gráfico.
 *
 * Além disso, a função calcula a porcentagem de Créditos e Débitos em relação ao total combinado e exibe um gráfico de barras horizontal
 * (comparativo entre os Créditos e Débitos), com as porcentagens e valores totais.
 *
 * A função é executada apenas após o carregamento completo do DOM, garantindo que todos os elementos HTML necessários estejam disponíveis.
 *
 * @event DOMContentLoaded - Dispara após o carregamento completo do HTML.
 */
document.addEventListener('DOMContentLoaded', function () {
    const dadosCredito = {
        labels: creditosLabels,
        datasets: [{
            data: creditosValores,
            backgroundColor: ['#4caf50', '#81c784', '#a5d6a7', '#c8e6c9']
        }]
    };

    const dadosDebito = {
        labels: debitosLabels,
        datasets: [{
            data: debitosValores,
            backgroundColor: ['#f44336', '#e57373', '#ef9a9a', '#ffcdd2']
        }]
    };

    new Chart(document.getElementById('graficoCredito'), {
        type: 'doughnut',
        data: dadosCredito,
        options: {
            plugins: {
                textoCentral: { total: totalCreditos }
            }
        },
        plugins: [textoCentral]
    });

    new Chart(document.getElementById('graficoDebito'), {
        type: 'doughnut',
        data: dadosDebito,
        options: {
            plugins: {
                textoCentral: { total: totalDebitos }
            }
        },
        plugins: [textoCentral]
    });

    // Gráfico Comparativo de Créditos x Débitos
    const total = totalCreditos + totalDebitos;
    const porcentagemCredito = (totalCreditos / total) * 100;
    const porcentagemDebito = (totalDebitos / total) * 100;

    const ctxComparacao = document.getElementById('graficoComparativo');
    if (ctxComparacao) {
        new Chart(ctxComparacao, {
            type: 'bar',
            data: {
                labels: [''],
                datasets: [
                    {
                        label: 'Créditos',
                        data: [porcentagemCredito],
                        backgroundColor: '#4caf50',
                        stack: 'stack1'
                    },
                    {
                        label: 'Débitos',
                        data: [porcentagemDebito],
                        backgroundColor: '#f44336',
                        stack: 'stack1'
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                elements: {
                    bar: {
                        barThickness: 100
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const valor = context.dataset.label === 'Créditos' ? totalCreditos : totalDebitos;
                                return `${context.dataset.label}: R$ ${valor.toFixed(2)}`;
                            }
                        }
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        ticks: {
                            callback: function (value) {
                                return value + '%';
                            },
                            max: 100
                        }
                    },
                    y: {
                        stacked: true
                    }
                }
            }
        });
    }
});

/**
* Validação do formulário de cadastro de usuário
*
* - Verifica se as senhas coincidem
* - Confere se os termos de uso foram aceitos
* - Garante que o e-mail contém "@"
* - Impede envio se houver erros
*/
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formCadastro");

    if(form) {
        form.addEventListener("submit", function (event) {
            const senha = form.querySelector('input[name="senha"]').value;
            const comfirmarSenha = form.querySelector('input[name="confirmar_senha"]').value;
            const termosAceitos = form.querySelector('input[name="termos"]').checked;
            const email = form.querySelector('input[name="email"]').value;

            if (senha != confirmarSenha) {
                alert("As senhas não coincidem!");
                event.preventDefault();
                return;
            }

            if (!termosAceitos) {
                alert("Você deve aceitar os termos de uso para continuar.");
                event.preventDefault();
                return;
            }

            if (!email.includes('@')) {
                alert("Digite um e-mail válido.");
                event.preventDefault();
                return;
            }
        });
    }
});