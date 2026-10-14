# Gabarito — 100 Exercícios Práticos de POO e Lógica

Respostas e explicações para `exercicios.md`. Tente resolver cada questão antes de consultar.

---

## Bloco A — Fundamentos de Python aplicados

**1.** `Decimal("10.10") + Decimal("0.20")` imprime `10.30`, exato. `0.10 + 0.20` imprime algo como `0.30000000000000004`, porque `float` representa números em binário, e frações decimais como `0.1` não têm representação binária exata — o erro de arredondamento se acumula. Por isso dinheiro nunca deve usar `float`.

**2.** O bug é construir `Decimal` a partir de um `float` (`5000.00`), em vez de uma `string` (`"5000.00"`). Para valores "redondos" o resultado parece certo, mas para outros (ex: `Decimal(19.99)`) o resultado carrega imprecisão binária herdada do `float`. O correto é `Decimal("5000.00")`.

**3.** `strip()`. Remove espaços em branco do início e do fim da string.

**4.** `float` tem imprecisão de representação binária para frações decimais, o que é inaceitável ao lidar com dinheiro (um centavo "perdido" por arredondamento é um bug real). `Decimal` representa os números exatamente como escritos, desde que construído a partir de `string`.

**5.** 3 elementos (um para cada `modelo` em `modelos`). Isso substitui:
```python
resultado = []
for modelo in modelos:
    resultado.append(to_domain(modelo))
```

**6.**
```python
nomes = [categoria.nome for categoria in categorias]
```

**7.** O erro é `categoria.tpo` (faltam letras: deveria ser `categoria.tipo`). Python levantaria `AttributeError: 'Categoria' object has no attribute 'tpo'`.

**8.** Se `parcelas_restantes == 0`, retorna `"quitado"`. Se for `3` (qualquer valor diferente de zero), retorna `"ativo"`. É um operador ternário: `valor_se_verdadeiro if condição else valor_se_falso`.

**9.** `str | None` — a sintaxe moderna de type hints para "string ou None" (união de tipos).

**10.** Sem `start=Decimal("0")`, o `sum()` usaria `0` (um `int`) como valor inicial. Somar `int + Decimal` funciona no Python (resulta em `Decimal`), então nesse caso específico não haveria erro — mas `start=Decimal("0")` deixa explícito que o resultado é sempre `Decimal`, e evita ambiguidade de tipo caso o gerador esteja vazio.

**11.** `transacao.data` é um objeto `date` do Python, e `"2026-09-05"` é uma `string`. Um objeto `date` nunca é igual a uma string, mesmo que a "representação visual" pareça a mesma — são tipos diferentes. A comparação correta seria `transacao.data == date(2026, 9, 5)`.

**12.**
```python
def nomes_categorias_credito(categorias):
    return [c.nome for c in categorias if c.tipo == "credito"]
```

---

## Bloco B — POO básica

**13.** Uma classe é um "molde"/template que define quais atributos e métodos um tipo de objeto terá. Um objeto é uma instância concreta criada a partir desse molde. `Categoria` é a classe; `Categoria(nome="Salário", tipo="credito")` cria um objeto específico.

**14.** `False`. Por padrão, o Python compara objetos por **identidade** (se são o mesmo objeto na memória), não por igualdade de atributos, a menos que a classe implemente `__eq__`. `Categoria` não implementa `__eq__`, então dois objetos com os mesmos dados ainda são considerados diferentes.

**15.**
```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
```

**16.** O underscore (`_nome`) é uma convenção em Python que sinaliza "atributo interno/privado, não deveria ser acessado diretamente de fora da classe". O acesso externo deve passar pela `@property` (`categoria.nome`), que pode incluir validação — acessar `_nome` diretamente pularia essa proteção.

**17.** Imprime `Lazer` (sem os espaços). O setter de `nome` chama `.strip()` antes de guardar o valor.

**18.** Recursão infinita: `return self.nome` dentro do próprio getter `nome` chama a si mesmo indefinidamente, até estourar `RecursionError`. O correto seria `return self._nome` (o atributo interno, não a property).

**19.** `@property`

**20.** Um atributo normal é só um valor guardado, sem controle sobre o que é atribuído. Uma `@property` permite executar código (validação, transformação) toda vez que o valor é lido ou escrito, mantendo a sintaxe de acesso simples (`objeto.atributo`). `Transacao.categoria` usa isso para garantir que a categoria nunca fique vazia.

**21.** Levanta `ValueError`, dentro do método `_validar_tipo` (chamado pelo setter de `tipo`), porque `"invalido"` não está em `TIPOS_VALIDOS`.

**22.** `strip()` — `if not nome.strip():`

**23.** `paga = False` (sem `self.`) cria uma variável **local** dentro do `__init__`, que é descartada assim que o método termina — nunca vira um atributo do objeto. O correto é `self.paga = False`.

**24.** Encapsulamento é esconder os detalhes internos de uma classe, expondo só uma interface controlada. `Transacao.valor` usa um setter que valida `valor > 0` antes de aceitar a atribuição — é impossível criar uma transação com valor negativo ou zero através da interface pública da classe.

**25.** Primeiro `False` (parcela nasce não paga), depois `True` (após chamar `pagar()`).

**26.** `self.paga = True`

**27.**
```python
from decimal import Decimal

class Produto:
    def __init__(self, nome: str, preco: Decimal):
        self.nome = nome
        self.preco = preco

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome deve ser uma string.")
        if not nome.strip():
            raise ValueError("O nome é obrigatório.")
        self._nome = nome.strip()

    @property
    def preco(self) -> Decimal:
        return self._preco

    @preco.setter
    def preco(self, preco: Decimal):
        if not isinstance(preco, Decimal):
            raise TypeError("O preço deve ser um Decimal.")
        if preco <= Decimal("0"):
            raise ValueError("O preço deve ser maior que zero.")
        self._preco = preco
```

**28.** Falta o getter (`@property`) correspondente antes do setter (`@tipo.setter`). O decorator `@tipo.setter` só existe depois que `@property def tipo(self): ...` já foi definido — sem ele, o nome `tipo` não existe ainda para receber `.setter`.

**29.** Porque `TIPOS_VALIDOS` é o mesmo valor para **todas** as instâncias da classe — não faz sentido recriar essa tupla toda vez que uma categoria é validada. Como atributo de classe, ela é criada uma única vez e compartilhada por todas as instâncias, economizando memória e deixando a intenção clara ("isso pertence ao conceito de Categoria, não a uma categoria específica").

**30.** Sim, imprimem a mesma coisa: `('credito', 'debito')`. Atributos de classe podem ser acessados tanto pelo nome da classe (`Categoria.TIPOS_VALIDOS`) quanto por qualquer instância dela (`categoria.TIPOS_VALIDOS`) — o Python busca primeiro no objeto, e se não encontrar, busca na classe.

---

## Bloco C — Herança e polimorfismo

**31.** Herança é quando uma classe ("filha") reaproveita atributos e comportamentos de outra ("mãe"), podendo adicionar ou sobrescrever partes. `Transacao` é a classe-mãe de `Credito` e `Debito`.

**32.** `True` (um `Credito` é uma `Transacao`, por herança) e `False` (um `Credito` não é um `Debito` — são classes irmãs, não relacionadas entre si por herança direta).

**33.** `super()` — chama o `__init__` da classe-mãe.

**34.** Polimorfismo é a capacidade de objetos de classes diferentes responderem de forma diferente ao "mesmo" método chamado. `Credito.impacto_saldo()` retorna o valor positivo; `Debito.impacto_saldo()` retorna o valor negativo — o chamador não precisa saber qual é qual, só chama `.impacto_saldo()`.

**35.** `5000.00` e `-1800.00`. São diferentes porque cada classe sobrescreve `impacto_saldo()` com sua própria lógica, mesmo compartilhando o mesmo nome de método (herdado de `Transacao`).

**36.** Isso faz o `Debito` ter impacto **positivo** no saldo, igual a um `Credito` — quebra a regra de negócio central do domínio (um débito deveria reduzir o saldo, não aumentá-lo). O correto é `return -self.valor`.

**37.** Para forçar que toda subclasse concreta (`Credito`, `Debito`) implemente seu próprio `impacto_saldo()`. Se alguém esquecer de sobrescrever esse método em uma nova subclasse, o erro aparece imediatamente e de forma explícita (`NotImplementedError`), em vez de silenciosamente usar um comportamento padrão errado.

**38.** Levanta `NotImplementedError`, porque `Transacao` (a classe-mãe, instanciada diretamente) nunca sobrescreveu `impacto_saldo()` — ela só define o "contrato" que as subclasses devem cumprir.

**39.** `"debito"`

**40.**
```python
class Estorno(Transacao):
    def impacto_saldo(self) -> Decimal:
        return Decimal("0")

    @property
    def tipo(self) -> str:
        return "estorno"
```

**41.** Não é polimorfismo — é o oposto: um `if/elif` que verifica explicitamente o tipo para decidir o que fazer, exatamente o tipo de código que o polimorfismo existe para evitar. É necessário aqui porque o mapper precisa **criar** o objeto certo a partir de um dado cru (`tipo`, uma string vinda do banco) — nesse ponto específico, ainda não existe um objeto polimórfico para "perguntar" o que ele é.

**42.** `Transacao.__init__` passou a aceitar e usar um parâmetro `id`, mas `Credito.__init__` não foi atualizado para aceitar `id` nem repassá-lo via `super().__init__(..., id=id)`. Herança não propaga automaticamente novos parâmetros para subclasses que sobrescrevem `__init__` — cada uma precisa ser atualizada manualmente.

**43.** Polimorfismo (mais especificamente, o fato de que `Credito` e `Debito` têm construtores com a mesma assinatura, por herdarem de `Transacao`). Como `classe` é só uma referência à classe (não uma string com o nome dela), `classe(descricao=..., ...)` funciona da mesma forma independentemente de `classe` ser `Credito` ou `Debito`.

**44.** `"credito: 1000"` e `"debito: -200"`. A função `descrever` nunca verifica o tipo do objeto — ela só chama `.tipo` e `.impacto_saldo()`, confiando que qualquer objeto passado saiba responder a essas chamadas (isso também é chamado de "duck typing").

**45.**
```python
@property
def taxa_juros_mensal_percentual(self) -> Decimal:
    return self.taxa_juros_mensal * Decimal("100")
```

---

## Bloco D — Composição e tratamento de exceções

**46.** Composição é quando uma classe "tem" instâncias de outra como parte de si (em vez de "ser" um tipo dela). `Emprestimo` "tem" uma lista de `Parcela` — um empréstimo não é um tipo de parcela, nem o contrário; a relação é de posse/agregação, não de hierarquia.

**47.** `3` e `<class 'app.domain.parcela.Parcela'>`.

**48.** `+` — `range(1, self.quantidade_parcelas + 1)`.

**49.** Para evitar duplicação de estado: se `parcelas_pagas` fosse um número guardado separadamente, ele poderia ficar dessincronizado da realidade (ex: alguém marca uma parcela como paga sem atualizar esse contador). Calcular sempre a partir da lista de parcelas garante que o valor é sempre a verdade atual, sem risco de inconsistência.

**50.** A propriedade chama a si mesma (`self.parcelas_pagas` dentro de `parcelas_pagas`), em vez de contar as parcelas pagas de fato. Isso é uma recursão infinita — cada chamada gera outra chamada idêntica, sem nunca parar.

**51.**
```python
class SaldoInsuficienteError(Exception):
    """
    Levantada quando uma operação exigiria um saldo maior do
    que o disponível atualmente.
    """
```

**52.** `Capturado: Taxa inválida`. O `except` com uma tupla `(ValueError, TypeError)` captura qualquer uma das duas exceções listadas; como foi levantada uma `ValueError`, ela é capturada.

**53.** Uma exceção específica (`CategoriaDaTransacaoNaoEncontradaError`) permite que o código que chama a função decida tratar **esse erro exato** de forma diferente de outros erros (por exemplo, capturando só esse tipo em uma rota, sem engolir acidentalmente outros bugs). Com `Exception` genérica, você teria que capturar (e potencialmente esconder) qualquer tipo de erro.

**54.** Falta a palavra `raise` antes de `CategoriaNaoEncontradaError(...)`. Sem ela, o Python só **cria** o objeto de exceção, mas nunca o levanta — o código continua executando normalmente e quebra logo depois, ao tentar chamar `to_domain(None)`.

**55.** `rollback` — `db.session.rollback()`.

**56.** `raise Erro(...)` simplesmente levanta uma nova exceção. `raise Erro(...) from err` levanta a nova exceção **encadeando** a exceção original (`err`) como causa — isso preserva o contexto completo no traceback (útil para depuração), deixando claro que o novo erro aconteceu "por causa" do erro original capturado.

**57.**
```python
def adicionar_parcela_extra(self, valor: Decimal, data_vencimento: date):
    nova_parcela = Parcela(
        numero=len(self.parcelas) + 1,
        valor=valor,
        data_vencimento=data_vencimento,
    )
    self.parcelas.append(nova_parcela)
```

**58.** O bloco `except ValueError` captura o erro (porque `nome=""` falha na validação de string vazia, que levanta `ValueError`, não `TypeError`). É impresso: `Erro de valor: O nome da categoria é obrigatório.`

---

## Bloco E — Padrões de arquitetura

**59.** Data Mapper é um padrão onde as entidades de domínio (regras de negócio) ficam completamente separadas de como os dados são persistidos, com uma camada intermediária (o "mapper") convertendo entre as duas. O projeto separa isso para que as regras de negócio possam ser testadas sem depender de banco de dados, e para que uma mudança na persistência nunca force mudanças na lógica de negócio.

**60.** Roda normalmente, sem nenhum erro — porque `Categoria` (em `app/domain/categoria.py`) é Python puro, sem nenhuma dependência do SQLAlchemy ou de qualquer banco de dados.

**61.** O mapper só converte dados de um formato para outro (`to_model`/`to_domain`), sem decidir nada nem acessar o banco diretamente para gravar. O service orquestra um caso de uso completo: valida, chama o mapper, interage com `db.session`, trata exceções de integridade — é quem decide "o que fazer", enquanto o mapper só sabe "como converter".

**62.** `tipo` — `tipo=categoria.tipo`.

**63.** Padrão Factory (Fábrica). A função recebe parâmetros de configuração e retorna um objeto pronto para uso (nesse caso, um `Blueprint` já configurado com rotas), encapsulando a lógica de construção.

**64.** Mistura a camada de **rota** (HTTP) com a camada de **persistência** (banco de dados) diretamente, pulando o service. Isso é um problema porque a rota passa a conhecer detalhes de implementação do banco (como `db.session`), tornando-a mais difícil de testar isoladamente e duplicando lógica que deveria estar centralizada em um único lugar (o service), caso outra rota precise criar uma categoria também.

**65.** Significa que uma classe deve ter um único motivo para mudar — uma única responsabilidade bem definida. `Parcela`, por exemplo, só sabe representar uma parcela e seu estado de pagamento; ela não sabe nada sobre banco de dados, HTTP, ou cálculo de juros (isso é responsabilidade de `Emprestimo`).

**66.** O `before_request` intercepta a requisição antes de qualquer função de rota rodar. Como o blueprint da requisição não é `None` nem `"auth"`, `_verificar_login()` é chamado, que (via `@login_required`) redireciona imediatamente para a página de login — a função `listar()` nunca chega a ser executada.

**67.**
```python
def criar_blueprint_categoria_generica(nome: str, tipo_permitido: str) -> Blueprint:
    bp = Blueprint(nome, __name__, url_prefix=f"/{nome}")

    @bp.route("/", methods=["GET"])
    def listar():
        # filtraria categorias por tipo_permitido
        ...

    return bp
```

**68.** Para manter a Responsabilidade Única: rotas lidam com HTTP (request/response), services lidam com regras de orquestração e acesso a dados. Isso também evita duplicar lógica de negócio em múltiplas rotas que precisem da mesma operação, e torna os services testáveis sem precisar simular uma requisição HTTP.

**69.**
```python
# em mappers/categoria_mapper.py — só converte, não persiste
def to_model(categoria):
    return CategoriaModel(nome=categoria.nome, tipo=categoria.tipo)

# em services/categoria_service.py — orquestra a persistência
def criar_categoria(nome, tipo):
    categoria = CategoriaDomain(nome=nome, tipo=tipo)
    modelo = to_model(categoria)
    db.session.add(modelo)
    db.session.commit()
    return to_domain(modelo)
```

**70.** Em certo sentido sim — a navbar é repetida literalmente em cada arquivo HTML. Mas o projeto prioriza simplicidade e independência de cada template (cada página é um arquivo completo e autocontido, mais fácil de entender isoladamente para quem está aprendendo) sobre a eliminação total de repetição visual. É uma troca consciente: menos DRY, mais simples de seguir sem entender o mecanismo de herança de template.

---

## Bloco F — Persistência, SQL e ORM

**71.** Uma chave estrangeira é uma coluna que guarda o `id` de uma linha de outra tabela, criando um vínculo real entre elas. Aparece como `transacoes.categoria_id`, que referencia `categorias.id`.

**72.** Imprime `"Salário"`. O recurso é `relationship()` do SQLAlchemy, que permite acessar o objeto relacionado inteiro (`transacao.categoria`) a partir da chave estrangeira, sem escrever a consulta SQL manualmente.

**73.** `relationship`

**74.** Ao excluir um `Emprestimo`, todas as `Parcela` associadas a ele são excluídas automaticamente pelo banco, evitando que fiquem "órfãs" (parcelas apontando para um `emprestimo_id` que não existe mais).

**75.** Falta uma `UniqueConstraint` sobre as colunas `nome` e `tipo` juntas, em `__table_args__`, para que o próprio banco rejeite duas linhas com a mesma combinação.

**76.** `CheckConstraint` valida uma condição sobre o **valor** de uma coluna (ex: `tipo IN ('credito', 'debito')` em `Transacao`). `UniqueConstraint` garante que a combinação de valores de uma ou mais colunas nunca se repita entre linhas (ex: `nome` + `tipo` em `Categoria`).

**77.** `None`. `SUM()` em SQL retorna `NULL` (que vira `None` em Python) quando não há nenhuma linha para somar — por isso o código do projeto sempre verifica `if resultado is not None else Decimal("0")`.

**78.** `group_by` — `.group_by(CategoriaModel.nome)`.

**79.** Porque "total de créditos" soma uma única coluna (`TransacaoModel.valor`) de uma única tabela, sem precisar de dados de nenhuma outra. "Total por categoria" precisa do **nome** da categoria, que não existe na tabela `transacoes` (só existe `categoria_id`) — por isso é necessário buscar (via `JOIN`) a tabela `categorias` para obter esse dado.

**80.** Filtra transações cuja data caia no mês de setembro (mês número 9), de qualquer ano. Se comparássemos com a string `"09"`, a comparação provavelmente falharia silenciosamente ou geraria erro, porque `extract("month", ...)` retorna um número inteiro, não uma string formatada com zero à esquerda.

**81.** Como `situacao` é calculada em Python (a partir da lista de parcelas), não existe como coluna no banco — não é possível fazer `WHERE situacao = 'ativo'` diretamente em SQL. A consulta precisaria trazer todos os empréstimos (ou usar uma subconsulta contando parcelas não pagas) e filtrar em Python, ou reformular a lógica em termos de dados que o banco realmente possui (ex: contar empréstimos com pelo menos uma parcela não paga).

**82.** `add()` só marca o objeto como "pendente para ser salvo" na sessão atual, em memória. `commit()` é quem de fato grava essa transação no banco de dados de forma permanente. Chamar `add()` várias vezes e `commit()` uma única vez no final grava todos os objetos adicionados de uma só vez, de forma atômica (tudo é salvo junto, ou nada é, em caso de erro).

---

## Bloco G — Flask e desenvolvimento web

**83.** Um Blueprint é uma forma de organizar um grupo relacionado de rotas em um módulo separado, que depois é registrado na aplicação principal. O projeto usa um blueprint por módulo para manter cada arquivo de rotas pequeno, focado, e fácil de entender isoladamente — em vez de um único arquivo gigante com todas as rotas da aplicação.

**84.** Na primeira visita (GET), retorna `"Mostrando formulário"`. Ao enviar o formulário (POST), retorna `"Processando formulário"`.

**85.** O parâmetro correto é `methods` (plural), não `method` (singular). Isso quebra a aplicação inteira porque o erro acontece durante o **registro** do blueprint (que roda dentro de `create_app()`), e se esse registro falha, nenhuma rota de nenhum módulo consegue ser criada.

**86.** `request.form` lê dados enviados no **corpo** de uma requisição `POST` (ex: um formulário HTML submetido). `request.args` lê parâmetros da **URL** (ex: `?ano=2026&mes=9`), usados em requisições `GET`. O projeto usa `request.form` em formulários de cadastro/edição, e `request.args` nos filtros de relatório.

**87.** Retorna a URL correspondente à rota `listar()` do blueprint `categoria` (ex: `/categorias/`). O projeto usa `url_for` em vez de strings fixas porque, se o prefixo da URL mudar um dia, todo o código que usa `url_for` continua funcionando sem precisar ser editado manualmente.

**88.** `"POST"` — `methods=["POST"]`.

**89.** Porque um link comum (`<a href>`) dispara uma requisição `GET`, que pode ser acionada acidentalmente (por um crawler, por exemplo, ou por um usuário dando duplo-clique sem querer). Um formulário com `POST` exige uma ação explícita e intencional do usuário (clicar em um botão de submit), o que é mais seguro para uma ação destrutiva como excluir.

**90.** `url_for` espera argumentos **nomeados** (`categoria_id=categoria.id`), não posicionais. O correto seria `url_for('categoria.editar', categoria_id=categoria.id)`.

**91.** O Flask-Login mantém o id do usuário logado guardado na sessão (um cookie assinado pelo servidor). `@login_required` verifica se existe um usuário carregado na sessão atual; se não houver, ele intercepta a requisição e redireciona automaticamente para a rota configurada em `login_manager.login_view` (no projeto, `"auth.login"`).

**92.** Todos os testes de rota falhariam com redirecionamentos (`302`) para `/login`, em vez dos códigos de status e conteúdos esperados (`200`, textos específicos) — porque, sem `LOGIN_DISABLED`, toda rota protegida exigiria um login real antes de responder, e os testes não fazem login por padrão.

**93.**
```python
@categoria_bp.route("/<int:categoria_id>", methods=["GET"])
def detalhe(categoria_id):
    try:
        categoria = obter_categoria(categoria_id)
    except CategoriaNaoEncontradaError as erro:
        return render_template(
            "categorias/listar.html",
            categorias=listar_categorias(),
            erro=str(erro),
        )
    return render_template("categorias/detalhe.html", categoria=categoria)
```

---

## Bloco H — Testes automatizados e depuração

**94.** Uma fixture é uma função que prepara um contexto reutilizável para os testes (ex: criar a aplicação, o banco, dados iniciais), evitando repetir esse código em cada teste. O projeto usa um banco **em memória** nos testes para garantir isolamento total (cada teste começa com um banco limpo) e velocidade (não grava nada em disco, nem interfere no banco real de desenvolvimento).

**95.** `=` é o operador de **atribuição**, não de comparação (que seria `==`). `assert categoria.nome = "Teste"` é um erro de sintaxe — o Python nem chega a executar o teste, ele falha ao tentar interpretar o arquivo.

**96.** Sim, o teste passa — mas por um motivo errado. Como `valor=Decimal("100.00")` é válido (maior que zero), nenhuma exceção é levantada dentro do bloco `with pytest.raises(ValueError)`, e o pytest reporta esse `with` como **falho**, não como sucesso — na verdade esse teste específico **falharia**, mas por um motivo diferente do que o nome sugere ("deveria testar valor zero, mas testou valor válido"). O problema geral ilustrado aqui: o nome do teste promete uma coisa, mas os dados testam outra — uma armadilha comum em testes mal escritos.

**97.** Ler o traceback (a pilha de chamadas) de baixo para cima, procurando a **primeira** linha do próprio código do projeto (não de bibliotecas externas) onde o erro realmente se origina — geralmente a causa raiz. Quando um erro afeta múltiplos módulos não relacionados, ele costuma estar em algo carregado cedo e por todos (configuração, inicialização, um import no topo do `__init__.py`), não espalhado em vários lugares.

**98.**
```python
def test_debito_deve_ser_tipo_debito():
    """
    Verifica se o tipo do débito é identificado corretamente.
    """
    debito = Debito(
        descricao="Aluguel",
        valor=Decimal("1800.00"),
        data=date(2026, 9, 10),
        categoria="Moradia",
    )
    assert debito.tipo == "debito"
```

**99.** Falha. A comparação `in` do Python é sensível a maiúsculas/minúsculas (*case-sensitive*): `"Valor inválido"` (com "V" maiúsculo) é uma string diferente de qualquer substring dentro de `"o valor informado..."` (com "v" minúsculo) — não há correspondência exata de caracteres.

**100.** O Python é uma linguagem de tipagem dinâmica e não verifica a existência de atributos, métodos ou nomes de variáveis antes de **executar** aquela linha específica — ele só descobre o erro no momento em que o código tenta de fato usar esse nome. Práticas que ajudam a pegar isso mais cedo: ferramentas de análise estática (linters, verificadores de tipo como Pylance/mypy), testes automatizados cobrindo cada caminho do código, e revisão cuidadosa linha por linha ao transcrever ou editar código manualmente.

---

*Fim do gabarito.*