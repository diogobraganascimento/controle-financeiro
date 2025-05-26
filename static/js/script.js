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
        const total = options.total ?? 0; // ✅ Nullish coalescing operator para segurança

        ctx.save(); // ✅ Sempre começa com save

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

        ctx.restore(); // ✅ Sempre termina com restore
    }
};


/**
 * Inicializa os gráficos de Créditos, Débitos e o gráfico comparativo após o carregamento completo do DOM.
 *
 * - Cria dois gráficos do tipo "doughnut": um para os Créditos e outro para os Débitos.
 * - Utiliza o plugin personalizado textoCentral para exibir o total no centro.
 * - Exibe um gráfico de barras horizontal para comparação percentual.
 *
 * @event DOMContentLoaded - Dispara após o carregamento completo do HTML.
 */
document.addEventListener('DOMContentLoaded', () => {
    const elementosDefinidos = [
        typeof creditosLabels !== 'undefined',
        typeof creditosValores !== 'undefined',
        typeof debitosLabels !== 'undefined',
        typeof debitosValores !== 'undefined',
        typeof totalCreditos !== 'undefined',
        typeof totalDebitos !== 'undefined'
    ].every(Boolean);

    if (!elementosDefinidos) return;

    const criarGraficosDoughnut = (elementID, labels, valores, cores, total) => {
        const ctx = document.getElementById(elementID);
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels,
                datasets: [{
                    data: valores,
                    backgroundColor: cores,
                }]
            },
            options: {
                plugins: {
                    textoCentral: { total }
                }
            },
            plugins: [textoCentral]
        });
    };

    criarGraficosDoughnut('graficoCredito', creditosLabels, creditosValores,
                          ['#4caf50', '#81c784', '#a5d6a7', '#c8e6c9'], totalCreditos);
    criarGraficosDoughnut('graficoDebito', debitosLabels, debitosValores,
                          ['#f44336', '#e57373', '#ef9a9a', '#ffcdd2'], totalDebitos);


    // Gráfico comparativo de Créditos x Débitos
    const total = totalCreditos + totalDebitos || 1; // Evita divisão por zero
    const porcentagemCredito = (totalCreditos / total) * 100;
    const porcentagemDebito = (totalDebitos / total) * 100;

    const ctxComparacao = document.getElementById('graficoComparativo');
    if (!ctxComparacao) return;

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
                        label(context) {
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
                        callback: value => `${value}%`,
                        max: 100
                    }
                },
                y: {
                    stacked: true
                }
            }
        }
    });
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

    if (!form) return

    form.addEventListener("submit", (event) => {
        const senha = form.querySelector('input[name="senha"]').value.trim();
        const confirmarSenha = form.querySelector('input[name="confirmar_senha"]').value.trim();
        const termosAceito = form.querySelector('input[name="termos"]').checked;
        const email = form.querySelector('input[name="email"]').value.trim();

        if (senha !== confirmarSenha) {
            alert("As senhas não coincidem!");
            event.preventDefault();
            return;
        }

        if (!termosAceito) {
            alert("Você deve aceitar os termos de uso para continuar.");
            event.preventDefault();
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            alert("Digite um e-mail válido.");
            event.preventDefault();
            return
        }
    });
});


/**
 * Gerador e exibidor automático de nome de usuário
 *
 * Ao digitar o e-mail, o campo de nome de usuário aparece e é preenchido automaticamente
 * com o prefixo do e-mail (parte antes do "@"). O campo permanece somente leitura
 * e oculto até que o e-mail comece a ser preenchido.
 *
 * @event input - Escuta o input do e-mail e atualiza o username.
 * @function DOMContentLoaded - Garante que o script será executado após o DOM estar carregado.
 */
document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email');
    const usernameGroup = document.getElementById('username-group');
    const usernameInput = document.getElementById('username');

    if (!emailInput || !usernameGroup || !usernameInput) return;

    // Oculta inicialmente o grupo do usurname
    usernameGroup.style.heigth = '0';
    usernameGroup.style.overflow = 'hidden';
    usernameGroup.style.transition = 'height 0.3s ease';

    emailInput.addEventListener('input', () => {
        const prefix = emailInput.value.trim().split('@')[0];

        if (prefix) {
            usernameInput.value = prefix;

            // Exibe com transição suave
            const scrollHeight = usernameGroup.scrollHeight + 'px';
            usernameGroup.style.height = scrollHeight;
        } else {
            // Oculta suavemente
            usernameInput.value = '';
            usernameGroup.style.height = '0';
        }
    });
});


/**
 * Valida a senha do formulário de cadastro após o carregamento completo do DOM.
 *
 * - Verifica se a senha inserida atende aos critérios de segurança definidos:
 *   - Mínimo de 8 caracteres
 *   - Pelo menos uma letra maiúscula
 *   - Pelo menos uma letra minúscula
 *   - Pelo menos um número
 *   - Pelo menos um caractere especial
 * - Verifica se a confirmação de senha é igual à senha informada.
 * - Em caso de erro, impede o envio do formulário e exibe uma mensagem de alerta em um modal Bootstrap.
 * - Utiliza um modal (`#modalErro`) com um campo (`#modalErroMensagem`) para exibir mensagens dinâmicas.
 *
 * Observação: Esta função é executada apenas após o evento de carregamento completo do DOM, garantindo que todos os elementos HTML estejam disponíveis.
 *
 * @event DOMContentLoaded - Dispara após o carregamento completo do HTML.
 * @listens submit - Intercepta o envio do formulário para realizar as validações.
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const modalErroEl = document.getElementById('modalErro');
    const modalErroMensagem = document.getElementById('modalErroMensagem');

    if (!form || !modalErroEl || !modalErroMensagem) return;

    const modalErro = new bootstrap.Modal(modalErroEl);

    form.addEventListener('submit', (event) => {
        const password = document.getElementById('password')?.value.trim();
        const confirmPassword = document.getElementById('confirm_password')?.value.trim();

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (!passwordRegex.test(password)) {
            event.preventDefault();
            modalErroMensagem.textContent = 'A senha deve ter no mínimo 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial.';
            modalErro.show();
            return;
        }

        if (password !== confirmPassword) {
            event.preventDefault();
            modalErroMensagem.textContent = 'As senhas não coincidem.';
            modalErro.show();
        }
    });
});


/**
 * Ativa o modo de edição do formulário de perfil.
 *
 * Este script é executado quando o botão "Editar" é clicado. Ele percorre todos
 * os campos de entrada do formulário e remove o atributo "disabled", permitindo
 * que sejam editados. Os campos "cpf", "email" e "username" permanecem desabilitados
 * por questões de integridade dos dados. Ao final, o botão "Salvar" é habilitado
 * para permitir o envio do formulário.
 *
 * @event click - Escutado no botão "Editar" para ativar o modo de edição.
 */
document.addEventListener('DOMContentLoaded', () => {
    const editarBtn = document.getElementById('editarBtn');
    const salvarBtn = document.getElementById('salvarBtn');

    if (!editarBtn || !salvarBtn) return;

    editarBtn.addEventListener('click', () => {
        const inputs = document.querySelectorAll('input.form-control');

        inputs.forEach(input => {
            const campoProtegido = ['cpf', 'email', 'username'];
            if (!campoProtegido.includes(input.name)) {
                input.removeAttribute('disabled');
            }
        });

        salvarBtn.removeAttribute('disabled');
    });
});