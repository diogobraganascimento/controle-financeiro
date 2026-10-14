# 100 Exercícios Práticos de POO e Lógica — Projeto Controle Financeiro
Este material usa código real do projeto Controle Financeiro para ensinar Programação Orientada a Objetos e lógica de programação de forma progressiva.

## Pré-requisitos
Antes de começar, você deve saber o básico de Python: variáveis, tipos primitivos, if/else, laços (for, while), funções e listas. Este material não ensina sintaxe de Python do zero — ele ensina POO e arquitetura de software usando Python como ferramenta.

### Como usar este material
Cada exercício referencia um arquivo real do projeto. Tenha o código aberto ao lado.
Os exercícios têm cinco tipos, marcados entre colchetes:
[Preveja a saída] — leia o código e raciocine sobre o resultado antes de rodar.
[Encontre o bug] — há um erro proposital no trecho; identifique e corrija.
[Complete o código] — uma lacuna (___) precisa ser preenchida.
[Implemente] — crie algo novo, seguindo o padrão já usado no projeto.
[Explique o porquê] — pergunta conceitual sobre uma decisão de arquitetura.
O gabarito está em gabarito.md, em arquivo separado — resolva antes de consultar.
A dificuldade cresce dentro de cada bloco e entre os blocos.

### Sumário
| Bloco | Tema | Questões |
| :--- | :--- | :--- |
| A | Fundamentos de Python aplicados | 1–12 |
| B | POO básica | 13–30 |
| C |	Herança e polimorfismo | 31–45 |
| D |	Composição e tratamento de exceções | 46–58 |
| E |	Padrões de arquitetura | 59–70 |
| F |	Persistência, SQL e ORM | 71–82 |
| G |	Flask e desenvolvimento web | 83–93 |
| H |	Testes automatizados e depuração | 94–100 |

## Bloco A — Fundamentos de Python aplicados (1–12)
### 1. [Preveja a saída] Em `app/domain/transacao.py`, o valor de uma transação é um Decimal. O que acontece ao executar:

```python
from decimal import Decimal
print(Decimal("10.10") + Decimal("0.20"))
print(0.10 + 0.20)
```
Por que os dois resultados são diferentes?

### 2. [Encontre o bug]
```python
valor = Decimal(5000.00)
```
Esse código roda sem erro, mas é considerado um bug no contexto deste projeto. Qual é o problema, e como deveria ser escrito?

### 3. [Complete o código] Em `app/domain/categoria.py`, o setter de nome remove espaços extras:
```python
@nome.setter
def nome(self, nome: str):
    self._validar_nome(nome)
    self._nome = nome.____()
```
Qual método completa a lacuna?

### 4. [Explique o porquê] Por que o projeto usa Decimal para representar dinheiro, em vez de float?

### 5. [Preveja a saída] Em `app/mappers/transacao_mapper.py`:
```python
return [to_domain(modelo) for modelo in modelos]
```
Supondo que modelos tenha 3 elementos, quantos elementos terá a lista retornada? O que essa construção substitui, se fosse escrita com um laço for tradicional?

### 6. [Complete o código] Reescreva a linha abaixo usando list comprehension:
```python
nomes = []
for categoria in categorias:
    nomes.append(categoria.nome)
```

### 7. [Encontre o bug]
```python
descricao = f"Categoria {categoria.nome} do tipo {categoria.tpo}"
```
Qual é o erro, e que tipo de exceção o Python levantaria ao executar essa linha?

### 8. [Preveja a saída] Em `app/domain/emprestimo.py`:

```python
return "quitado" if self.parcelas_restantes == 0 else "ativo"
```
Se parcelas_restantes for 0, o que a propriedade situacao retorna? E se for 3?

### 9. [Complete o código] Complete a assinatura de um parâmetro opcional que aceita string ou None, seguindo o padrão do projeto:
```python
def __init__(self, comprovante: ____ = None):
```

### 10. [Explique o porquê] Em app/domain/emprestimo.py:
```python
return sum(
    (parcela.valor for parcela in self.parcelas if not parcela.paga),
    start=Decimal("0"),
)
```
Por que o start=Decimal("0") é importante aqui? O que aconteceria de diferente (ou não) sem ele?

### 11. [Encontre o bug]
```python
if transacao.data == "2026-09-05":
    print("Mesma data")
```
Sabendo que transacao.data é um objeto date, por que essa comparação nunca será verdadeira, mesmo que a data seja "setembro de 2026"?

### 12. [Implemente] Escreva uma função nomes_categorias_credito(categorias) que recebe uma lista de objetos Categoria e retorna, usando list comprehension, uma lista só com os nomes das categorias cujo tipo é "credito".

## Bloco B — POO básica (13–30)
### 13. [Explique o porquê] O que é uma classe, e o que é um objeto? Dê um exemplo usando Categoria e uma instância concreta dela (ex: a categoria "Salário").

### 14. [Preveja a saída]

```python
categoria1 = Categoria(nome="Salário", tipo="credito")
categoria2 = Categoria(nome="Salário", tipo="credito")
print(categoria1 == categoria2)
```
O resultado é True ou False? Por quê?

### 15. [Complete o código] Complete o construtor de uma classe simples Pessoa, com atributos nome e idade:
```python
class Pessoa:
    def __init__(self, nome, idade):
        ____.nome = nome
        ____.idade = idade
```

### 16. [Explique o porquê] Em app/domain/categoria.py, por que os atributos reais são guardados como `self._nome` (com underscore) em vez de `self.nome` diretamente?

### 17. [Preveja a saída]

```python
categoria = Categoria(nome="  Lazer  ", tipo="debito")
print(categoria.nome)
```
O que é impresso? Por quê?

### 18. [Encontre o bug]

```python
class Categoria:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

    @property
    def nome(self):
        return self.nome
```
Esse código, ao ser executado, trava o programa. Qual é o problema e por quê?

### 19. [Complete o código] Complete o decorator que transforma um método em "somente leitura calculada":

```python
def tipo(self) -> str:
    return "credito"
```
### 20. [Explique o porquê] Qual é a diferença entre um atributo normal (`self.nome = nome`) e uma @property? Por que Transacao.categoria usa `@property` com validação, em vez de um atributo público simples?

### 21. [Preveja a saída]

```python
from decimal import Decimal
Categoria(nome="Teste", tipo="invalido")
```
O que acontece ao executar essa linha? Que tipo de exceção é levantada, e onde ela é levantada dentro da classe?

### 22. [Complete o código] Complete a validação que rejeita valores vazios:
```python
def _validar_nome(self, nome: str):
    if not isinstance(nome, str):
        raise TypeError("O nome deve ser uma string.")
    if not nome.____():
        raise ValueError("O nome é obrigatório.")
```
### 23. [Encontre o bug]
```python
class Parcela:
    def __init__(self, numero, valor, data_vencimento):
        self.numero = numero
        self.valor = valor
        self.data_vencimento = data_vencimento
        paga = False
```
Depois de criar uma `Parcela`, `parcela.paga` levanta `AttributeError`. Por quê?

### 24. [Explique o porquê] O que é encapsulamento? Dê um exemplo concreto de como Transacao usa encapsulamento para impedir que o valor de uma transação seja negativo.

### 25. [Preveja a saída]
```python
parcela = Parcela(numero=1, valor=Decimal("450.00"), data_vencimento=date(2026, 10, 5))
print(parcela.paga)
parcela.pagar()
print(parcela.paga)
```
Quais são as duas saídas?

### 26. [Complete o código] Complete o método que marca uma parcela como paga:
```python
def pagar(self):
    self.____ = True
```
### 27. [Implemente] Crie uma classe Produto, com atributos nome (string, obrigatório) e preco (Decimal, deve ser maior que zero), seguindo exatamente o mesmo padrão de validação com @property usado em Categoria.

### 28. [Encontre o bug]
```python
class Categoria:
    TIPOS_VALIDOS = ("credito", "debito")

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

    @tipo.setter
    def tipo(self, tipo):
        ...
```
Esse código não executa — dá erro antes mesmo de instanciar a classe. O que falta?

### 29. [Explique o porquê] Por que Categoria.TIPOS_VALIDOS é definido como um atributo de classe (fora do `__init__`), em vez de ser recriado dentro de cada validação?

### 30. [Preveja a saída]
```python
print(Categoria.TIPOS_VALIDOS)
categoria = Categoria(nome="Salário", tipo="credito")
print(categoria.TIPOS_VALIDOS)
```
As duas linhas imprimem a mesma coisa? Por quê isso é possível, já que TIPOS_VALIDOS nunca foi definido dentro de __init__?

## Bloco C — Herança e polimorfismo (31–45)
### 31. [Explique o porquê] O que é herança? No projeto, qual classe é a "classe-mãe" de Credito e Debito?

### 32. [Preveja a saída]
```python
credito = Credito(descricao="Salário", valor=Decimal("5000.00"), data=date(2026, 9, 5), categoria="Salário")
print(isinstance(credito, Transacao))
print(isinstance(credito, Debito))
```
Quais são os dois resultados?

### 33. [Complete o código] Complete a chamada ao construtor da classe-mãe:
```python
class Credito(Transacao):
    def __init__(self, descricao, valor, data, categoria, comprovante=None):
        ____.__init__(
            descricao=descricao, valor=valor, data=data,
            categoria=categoria, comprovante=comprovante,
        )
```
### 34. [Explique o porquê] O que é polimorfismo? Explique como o método `impacto_saldo()` demonstra polimorfismo entre Credito e Debito.

### 35. [Preveja a saída]
```python
credito = Credito(descricao="Salário", valor=Decimal("5000.00"), data=date(2026, 9, 5), categoria="Salário")
debito = Debito(descricao="Aluguel", valor=Decimal("1800.00"), data=date(2026, 9, 10), categoria="Moradia")
print(credito.impacto_saldo())
print(debito.impacto_saldo())
```
Quais são os dois resultados, e por que são diferentes mesmo chamando o "mesmo" método?

### 36. [Encontre o bug]
```python
class Debito(Transacao):
    def impacto_saldo(self):
        return self.valor
```
Esse código roda sem erro de sintaxe, mas quebra uma regra de negócio importante do projeto. Qual?

### 37. [Explique o porquê] Em `app/domain/transacao.py`:
```python
def impacto_saldo(self) -> Decimal:
    raise NotImplementedError(
        "As subclasses devem implementar impacto_saldo()."
    )
```
Por que Transacao define esse método só para levantar uma exceção, em vez de não defini-lo?

### 38. [Preveja a saída]
```python
transacao = Transacao(descricao="Teste", valor=Decimal("100.00"), data=date(2026, 1, 1), categoria="Teste")
transacao.impacto_saldo()
```
O que acontece ao executar a última linha?

### 39. [Complete o código] Complete a propriedade polimórfica tipo em Debito:
```python
@property
def tipo(self) -> str:
    return "____"
```
### 40. [Implemente] Crie uma terceira subclasse de Transacao chamada Estorno, cujo impacto_saldo() sempre retorna `Decimal("0")` (um estorno não afeta o saldo, só fica registrado). Lembre-se de sobrescrever tipo também.

### 41. [Explique o porquê] Em `app/mappers/transacao_mapper.py`, a função to_domain() usa `if transacao.tipo == "credito"`: ... `elif transacao.tipo == "debito"`: ... para decidir qual classe instanciar. Isso é polimorfismo? Por que sim ou por que não?

### 42. [Encontre o bug]
```python
class Credito(Transacao):
    def __init__(self, descricao, valor, data, categoria, comprovante=None, id=None):
        super().__init__(
            descricao=descricao, valor=valor, data=data,
            categoria=categoria, comprovante=comprovante,
        )
```
Depois que Transacao ganhou um parâmetro id, esse código de Credito passou a falhar ao tentar reconstruir uma transação vinda do banco. Por quê?

### 43. [Explique o porquê] Em `app/routes/transacao_routes.py`, a fábrica criar_blueprint_transacao recebe um parâmetro classe (que pode ser Credito ou Debito) e depois faz classe(descricao=..., valor=..., ...). Que conceito de POO permite que a mesma linha de código funcione para as duas classes?

### 44. [Preveja a saída]
```python
def descrever(transacao):
    print(f"{transacao.tipo}: {transacao.impacto_saldo()}")

descrever(Credito(descricao="Salário", valor=Decimal("1000"), data=date(2026,1,1), categoria="Salário"))
descrever(Debito(descricao="Conta", valor=Decimal("200"), data=date(2026,1,1), categoria="Contas"))
```
Quais são as duas saídas? A função descrever precisou saber, em algum momento, se recebeu um Credito ou um Debito?

### 45. [Implemente] Em `app/domain/emprestimo.py`, juros_anual é calculado a partir de taxa_juros_mensal. Implemente, seguindo o mesmo estilo de `@property`, uma propriedade taxa_juros_mensal_percentual em Emprestimo que retorna a taxa mensal multiplicada por 100 (ex: 0.02 vira 2).

## Bloco D — Composição e tratamento de exceções (46–58)
### 46. [Explique o porquê] O que é composição? Por que Emprestimo usa composição com Parcela em vez de herança?

### 47. [Preveja a saída]
```python
emprestimo = Emprestimo(
    descricao="Pessoal", valor_retirado=Decimal("5000.00"),
    taxa_juros_mensal=Decimal("0.02"), quantidade_parcelas=3,
    data_contratacao=date(2026, 9, 1),
)
print(len(emprestimo.parcelas))
print(type(emprestimo.parcelas[0]))
```
Quais são as duas saídas?

### 48. [Complete o código] Complete a geração da lista de parcelas de um empréstimo:
```python
def _gerar_parcelas(self) -> list[Parcela]:
    return [
        Parcela(numero=numero, valor=self.valor_parcela, data_vencimento=...)
        for numero in range(1, self.quantidade_parcelas ____ 1)
    ]
```
### 49. [Explique o porquê] Por que Emprestimo não armazena diretamente um campo parcelas_pagas como um número, calculando-o sempre a partir da lista de parcelas `(sum(1 for parcela in self.parcelas if parcela.paga))`?

### 50. [Encontre o bug]
```python
@property
def parcelas_pagas(self) -> int:
    return self.quantidade_parcelas - self.parcelas_pagas
```
Esse código "roda", mas nunca termina (ou estoura um erro de recursão). Por quê?

### 51. [Implemente] Crie uma classe customizada de exceção chamada `SaldoInsuficienteError`, herdando de Exception, com uma docstring explicando quando ela deveria ser levantada.

52. [Preveja a saída]
```python
try:
    raise ValueError("Taxa inválida")
except (ValueError, TypeError) as erro:
    print(f"Capturado: {erro}")
```
O que é impresso?

### 53. [Explique o porquê] Em app/mappers/transacao_mapper.py, existe a classe CategoriaDaTransacaoNaoEncontradaError. Por que o projeto cria uma exceção específica para esse caso, em vez de usar Exception genérica ou ValueError?

### 54. [Encontre o bug]
```python
def obter_categoria(categoria_id):
    modelo = db.session.get(CategoriaModel, categoria_id)
    if modelo is None:
        CategoriaNaoEncontradaError(f"Categoria {categoria_id} não encontrada.")
    return to_domain(modelo)
```
Esse código não lança nenhuma exceção quando a categoria não existe, e quebra de outro jeito logo depois. Qual é o erro, e como corrigir?

### 55. [Complete o código] Complete o bloco que trata uma falha de integridade do banco ao criar uma categoria duplicada:
```python
try:
    db.session.commit()
except IntegrityError:
    db.session.____()
    raise CategoriaJaExisteError(f"Já existe uma categoria '{nome}'.")
```

### 56. [Explique o porquê] Qual é a diferença entre `raise ValueError(...)` `e raise CategoriaJaExisteError(...) from err`? Por que o projeto às vezes usa from err?

### 57. [Implemente] Adicione, à classe Emprestimo, um método `adicionar_parcela_extra(valor, data_vencimento)` que cria e adiciona uma nova Parcela à lista `self.parcelas`, com numero igual a `len(self.parcelas) + 1`.

### 58. [Preveja a saída]
```python
try:
    Categoria(nome="", tipo="credito")
except ValueError as erro:
    print("Erro de valor:", erro)
except TypeError as erro:
    print("Erro de tipo:", erro)
```
Qual bloco except captura o erro, e o que é impresso?

## Bloco E — Padrões de arquitetura (59–70)

### 59. [Explique o porquê] O que é o padrão Data Mapper? Por que o projeto separa `app/domain/categoria.py` de `app/models/categoria.py`, em vez de colocar tudo em uma única classe?

### 60. [Preveja a saída] Dado que Categoria (domínio) não tem nenhum import do SQLAlchemy, o que acontece se você tentar rodar `tests/test_categoria.py` sem nenhum banco de dados configurado?

### 61. [Explique o porquê] Qual é a diferença de responsabilidade entre `app/mappers/categoria_mapper.py` e `app/services/categoria_service.py`?

### 62. [Complete o código] Complete a função que converte um modelo de persistência para uma entidade de domínio:
```python
def to_domain(categoria: CategoriaModel) -> CategoriaDomain:
    return CategoriaDomain(
        nome=categoria.nome,
        tipo=categoria.____,
        id=categoria.id,
    )
````

### 63. [Explique o porquê] Em `app/routes/transacao_routes.py`, existe uma função criar_blueprint_transacao que constrói e retorna um Blueprint. Esse é um exemplo de qual padrão de projeto (dica: ela "fabrica" blueprints)?

### 64. [Encontre o bug]
```python
@categoria_bp.route("/nova", methods=["GET", "POST"])
def nova():
    categoria = Categoria(nome=request.form["nome"], tipo=request.form["tipo"])
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for("categoria.listar"))
```
Esse código mistura duas responsabilidades que o projeto normalmente mantém separadas. Quais, e por que isso é considerado um problema de arquitetura (mesmo que o código "funcione")?

### 65. [Explique o porquê] O que significa "Single Responsibility" (Responsabilidade Única)? Dê um exemplo de uma classe do projeto que segue bem esse princípio.

### 66. [Preveja a saída] Em `app/__init__.py`, existe:
```python
@app.before_request
def proteger_rotas():
    if request.blueprint in (None, "auth"):
        return None
    return _verificar_login()
```
Se um usuário não autenticado tentar acessar /categorias/, o que acontece antes mesmo da função listar() (da rota de categorias) começar a executar?

### 67. [Implemente] Siga o padrão de criar_blueprint_transacao e escreva (em pseudocódigo ou Python real) o esqueleto de uma fábrica criar_blueprint_categoria_generica(nome, tipo_permitido) — não precisa ser funcional, só precisa demonstrar que você entendeu o padrão de "função que retorna um Blueprint configurado".

### 68. [Explique o porquê] Por que as rotas Flask do projeto nunca chamam db.session diretamente, sempre passando por uma função de app/services/?

### 69. [Encontre o bug]
```python
def to_model(categoria):
    modelo = CategoriaModel(nome=categoria.nome, tipo=categoria.tipo)
    db.session.add(modelo)
    db.session.commit()
    return modelo
```
Esse to_model mistura duas responsabilidades que, no projeto real, ficam separadas entre `mappers/` e `services/`. Reescreva separando as duas.

### 70. [Explique o porquê] O projeto decidiu não usar base.html (herança de template Jinja2), preferindo repetir a barra de navegação em cada arquivo HTML. Isso viola o princípio DRY (Don't Repeat Yourself)? Avalie os dois lados.

## Bloco F — Persistência, SQL e ORM (71–82)

### 71. [Explique o porquê] O que é uma chave estrangeira (`Foreign Key`)? Onde ela aparece na relação entre Transacao e Categoria?

### 72. [Preveja a saída]
```python
transacao_salva = db.session.get(Transacao, 1)
print(transacao_salva.categoria.nome)
```
Supondo que a transação de id=1 existe e está ligada a uma categoria chamada "Salário", o que é impresso? Que recurso do SQLAlchemy permite acessar .categoria.nome sem escrever uma consulta SQL manual?

### 73. [Complete o código] Complete a declaração da relação um-para-muitos em Emprestimo:
```python
parcelas: Mapped[list["Parcela"]] = ____(
    back_populates="emprestimo",
    cascade="all, delete-orphan",
)
````

### 74. [Explique o porquê] O que cascade="all, delete-orphan" faz, na prática, quando um Emprestimo é excluído do banco?

### 75. [Encontre o bug]
```python
class Categoria(db.Model):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20))
```
Depois de criar duas categorias com o mesmo nome e tipo, o banco aceita as duas sem reclamar — mas o projeto real não permite isso. O que falta nesse modelo?

### 76. [Explique o porquê] Qual é a diferença entre CheckConstraint e UniqueConstraint? Dê um exemplo de cada, usados no projeto.

### 77. [Preveja a saída]
```python
resultado = db.session.query(func.sum(TransacaoModel.valor)).filter_by(tipo="credito").scalar()
```
Se não existir nenhuma transação do tipo "credito" no banco, o que resultado vale? 0, None, ou um erro?

### 78. [Complete o código] Complete a consulta que soma débitos agrupados por categoria:
```python
db.session.query(CategoriaModel.nome, func.sum(TransacaoModel.valor)) \
    .join(TransacaoModel, TransacaoModel.categoria_id == CategoriaModel.id) \
    .filter(TransacaoModel.tipo == "debito") \
    .____(CategoriaModel.nome)
````

### 79. [Explique o porquê] Por que a consulta de totais por categoria precisa de um JOIN explícito com Categoria, enquanto a consulta de "total de créditos" (sem agrupar por categoria) não precisa?

### 80. [Preveja a saída]
```python
from sqlalchemy import extract
db.session.query(TransacaoModel).filter(extract("month", TransacaoModel.data) == 9)
```
O que essa consulta filtra? O que aconteceria se, por engano, comparássemos com a string "09" em vez do número 9?

### 81. [Implemente] Escreva (em texto, pseudocódigo próximo de SQLAlchemy real) uma consulta que retorna a quantidade de empréstimos com situacao "ativo" — lembrando que situacao é uma propriedade calculada no domínio, não uma coluna do banco. Isso muda a forma de fazer essa consulta?

### 82. [Explique o porquê] Por que db.session.add(objeto) sozinho não grava nada no banco — é preciso também chamar db.session.commit()? O que aconteceria se você chamasse add() várias vezes e só desse commit() no final?

## Bloco G — Flask e desenvolvimento web (83–93)

### 83. [Explique o porquê] O que é um Blueprint no Flask? Por que o projeto usa um blueprint por módulo (categoria_bp, credito_bp, etc.) em vez de todas as rotas em um único arquivo?

### 84. [Preveja a saída]
```python
@categoria_bp.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        return "Processando formulário"
    return "Mostrando formulário"
```
O que esse código retorna quando o usuário abre a página `/categorias/nova` pela primeira vez? E quando ele envia o formulário?

### 85. [Encontre o bug]
```python
@categoria_bp.route("/nova", method=["GET", "POST"])
def nova():
    ...
```
Esse código quebra a aplicação inteira, não só essa rota. Qual é o erro, e por que ele afeta até rotas de outros módulos?

### 86. [Explique o porquê] Qual é a diferença entre `request.form.get("nome")` e `request.args.get("nome")`? Em quais situações o projeto usa cada um?

### 87. [Preveja a saída]
```python
return redirect(url_for("categoria.listar"))
```
O que url_for("categoria.listar") retorna? Por que o projeto usa url_for em vez de escrever a URL diretamente ("/categorias/")?

### 88. [Complete o código] Complete a rota de exclusão de categoria:
```python
@categoria_bp.route("/<int:categoria_id>/excluir", methods=["____"])
def excluir(categoria_id):
    excluir_categoria(categoria_id)
    return redirect(url_for("categoria.listar"))
````

### 89. [Explique o porquê] Por que a exclusão de uma categoria é feita com um `<form method="POST">` e um botão, em vez de um simples `link <a href="...">Excluir</a>`?

### 90. [Encontre o bug]
```html
<a href="{{ url_for('categoria.editar', categoria.id) }}">Editar</a>
```
Esse trecho de template Jinja2 quebra a renderização da página. Qual é o erro de sintaxe?

### 91. [Explique o porquê] Como o `@login_required` (do Flask-Login) sabe se o usuário está autenticado ou não? O que acontece, no código do projeto, quando um usuário não autenticado acessa uma rota protegida?

### 92. [Preveja a saída] Em modo de teste (TESTING=True), o projeto desabilita a autenticação por padrão (LOGIN_DISABLED). O que aconteceria com os testes de test_rotas_categoria.py se essa configuração não existisse?

### 93. [Implemente] Escreva o esqueleto de uma rota Flask `GET /categorias/<int:categoria_id>` que busca uma categoria pelo id e retorna uma página de detalhe — seguindo o padrão de tratamento de erro (`try/except CategoriaNaoEncontradaError`) já usado em outras rotas do projeto.

## Bloco H — Testes automatizados e depuração (94–100)

### 94. [Explique o porquê] O que é uma fixture do pytest? Por que `tests/test_persistencia.py` usa uma fixture app que cria um banco SQLite em memória, em vez de usar o banco real do projeto?

### 95. [Preveja a saída]
```python
def test_exemplo():
    categoria = Categoria(nome="Teste", tipo="credito")
    assert categoria.nome = "Teste"
```
Esse teste nem chega a rodar. Por quê? (Atenção ao operador usado.)

### 96. [Encontre o bug]
```python
def test_deve_rejeitar_valor_zero():
    with pytest.raises(ValueError):
        Credito(descricao="Teste", valor=Decimal("100.00"), data=date(2026,1,1), categoria="Teste")
```
Esse teste tem o nome "deve rejeitar valor zero", mas o valor passado é 100.00, não 0. O teste passa mesmo assim? O que esse teste está realmente verificando (e por que isso é um problema)?

### 97. [Explique o porquê] No projeto, vários erros em cascata (um único erro de digitação derrubando dezenas de testes de módulos completamente diferentes) foram investigados e corrigidos. Qual é a estratégia geral para encontrar a causa raiz quando isso acontece?

### 98. [Implemente] Escreva um teste test_debito_deve_ser_tipo_debito() que verifica se Debito(...).tipo == "debito", seguindo o padrão de nomes e estrutura (docstring, assert) já usado no projeto.

### 99. [Preveja a saída]
```python
assert "Valor inválido" in "o valor informado é inválido."
```
Esse assert passa ou falha? Por que maiúsculas e minúsculas importam aqui?

### 100. [Explique o porquê] Ao longo da construção deste projeto, muitos bugs vieram de nomes quase certos (percelas em vez de parcelas, db.seesion em vez de db.session, auth_login em vez de auth.login). Por que o Python não detecta esse tipo de erro antes de você rodar o código? Que prática de desenvolvimento ajuda a pegar esses erros mais cedo?

### Fim dos 100 exercícios. Gabarito completo em gabarito.md.


