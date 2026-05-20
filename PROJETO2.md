> **⚠️ NOTA DE FORMATO E WORKFLOW**
> 
> O presente trabalho encontra-se estruturado num **único ficheiro `.md` (Markdown)**. Esta decisão técnica visa otimizar a **portabilidade** do documento, facilitar a **navegação interna** através de âncoras e garantir total **compatibilidade** com plataformas de controlo de versões como o GitHub.
> 
>  **Nota Importante:** Após a validação final da estrutura e conteúdo acadêmico, este ficheiro deve ser migrado para o formato **.docx (Microsoft Word)** conforme os requisitos formais da instituição de ensino superior.

# Otimização de Roteamento em Redes CVNet - Trabalho de Mestrado
---

## Índice
- [1. Introdução ao Problema](#definicao)
- [2. Formulações Matemáticas](#formulacoes)
- [3. Complexidade e Métodos de Resolução](#complexidade-e-metodos)
- [4. Implementação em Python](#python)
- [5. Resultados para CVNet](#resultados)
- [6. Conclusões](#conclusões)
- [7. Referências Bibliográficas](#referencias)

## 1. Definição do Problema<a id="definicao"></a>

O Problema do Caixeiro Viajante (PCV), frequentemente designado na literatura internacional como _Traveling Salesman Problem_ (TSP), é um dos problemas mais emblemáticos e estudados no campo da otimização combinatória e da investigação operacional (Hillier & Lieberman, 2013). Na sua definição clássica, o problema descreve um vendedor que necessita de visitar um conjunto específico de cidades exatamente uma vez, regressando à cidade de origem no final do percurso. O objetivo fundamental é identificar a rota que minimiza a distância total percorrida ou o custo associado à viagem.

Do ponto de vista da teoria dos grafos, o PCV consiste na procura de um **ciclo Hamiltoniano** de custo mínimo num grafo completo (Gutin & Punnen, 2002). Um "ciclo Hamiltoniano" é simplesmente um caminho que permite passar por todos os pontos de uma rede (nós) sem repetir nenhum, voltando exatamente ao ponto onde tudo começou.

Embora a sua formulação pareça simples, o PCV é classificado como um problema **NP-difícil** (_NP-hard_), o que significa que não existe um algoritmo conhecido capaz de encontrar a solução ótima em tempo computacional reduzido à medida que o número de cidades aumenta (Hillier & Lieberman, 2013). Por exemplo, enquanto um problema com 10 cidades apresenta um número gerível de soluções possíveis, um cenário com 50 cidades já ultrapassa as $10^{62}$ rotas viáveis (Hillier & Lieberman, 2013).

### O Contexto CVNet e a Analogia com o PCV

O projeto da **Agência Nacional de Redes de Cabo Verde (CVNet)** enquadra-se perfeitamente na estrutura matemática do PCV. No cenário proposto para o ano 2040, as 10 ilhas de Cabo Verde representam os "nós" (ou cidades) de uma rede de comunicação de alta velocidade. A necessidade de sincronização diária entre os data centers localizados em cada ilha exige a criação de uma rota eficiente que interligue todos os pontos.

A semelhança entre o desafio da CVNet e o PCV clássico é direta:

1. **Nós da Rede:** As 10 ilhas de Cabo Verde (Santo Antão, São Vicente, etc.) equivalem às cidades que o caixeiro deve visitar.
2. **Custo de Ligação:** A matriz de distâncias fornecida pela CVNet representa o "custo" $c\_{ij}$ de transmitir dados entre a ilha $i$ e a ilha $j$ (Gutin & Punnen, 2002).
3. **Objetivo Operacional:** Minimizar a latência ou o custo total de comunicação, garantindo que a "sincronização" passe por todos os centros de dados uma única vez e retorne ao ponto inicial para fechar o ciclo de atualização.

Assim, resolver o problema da CVNet implica modelar a infraestrutura das ilhas como um grafo e aplicar técnicas de otimização para garantir que a transmissão de dados seja feita através da rota Hamiltoniana mais curta possível.

## 2. Formulações Matemáticas<a id="formulacoes"></a>

## 3. Complexidade e Métodos de Resolução<a id="complexidade-e-metodos"></a>

## 4. Implementação em Python<a id="python"></a>

A transição da teoria para a prática exige uma distinção clara entre dois pilares da Investigação Operacional: a **formulação do modelo** (a estrutura lógica do problema) e o **procedimento de resolução** (o motor matemático que encontra a resposta). Para o caso da CVNet, utilizaremos a linguagem **Python** e a biblioteca de modelação **PuLP** para realizar esta ponte.

### 4.1. O Binómio Modelo (MTZ) e Algoritmo (Branch-and-Cut)

É fundamental compreender que o código Python não "adivinha" a rota; ele comunica uma estrutura formal a um solucionador profissional.

* **A Formulação (O Modelo MTZ):** No código, implementamos a técnica de **Miller-Tucker-Zemlin (MTZ)**. Esta formulação é a "receita" que define o que constitui uma rota válida, utilizando variáveis binárias para decidir que ligações activar e variáveis contínuas auxiliares para ordenar a sequência de visita, garantindo a eliminação de _subtours_ de forma compacta.
* **O Algoritmo (Branch-and-Cut):** Quando executamos o comando de resolução, o motor de optimização (como o solver CBC integrado no PuLP) aplica o algoritmo **Branch-and-Cut**. Este algoritmo é o "forno" que processa as equações MTZ, dividindo o problema em subproblemas (ramificação) e adicionando restrições matemáticas dinâmicas (cortes) até encontrar a solução absolutamente óptima para as 10 ilhas.


### 4.2. Tradução do Modelo em Código

A implementação em `tsp_cvnet.py` segue rigorosamente a anatomia de um problema de programação linear inteira.

#### A. Inicialização e Variáveis de Decisão

Primeiro, o problema é instanciado como uma minimização e as variáveis de decisão são criadas. A variável $x_{ij}$ assume valor 1 se a rota incluir o arco entre as ilhas $i$ e $j$, enquanto as variáveis $u_i$ são auxiliares para a ordenação MTZ [1, p. 463; 5, p. 20]:

```python
# Inicialização do Problema como Minimização
prob = pulp.LpProblem("TSP\_CVNet", pulp.LpMinimize)

# x[i,j] é binária: 1 se viaja da ilha i para j, 0 caso contrário
x = pulp.LpVariable.dicts(
    "x",
    ((i, j) for i in range(n) for j in range(n) if i != j),
    cat='Binary'
)

# u[i] são as variáveis contínuas auxiliares para a formulação MTZ
u = pulp.LpVariable.dicts(
    "u",
    (i for i in range(n)),
    lowBound=0,
    upBound=n-1,
    cat='Continuous'
)
```

#### B. Função Objectivo e Restrições de Grau

O objectivo é minimizar o somatório das distâncias das arestas activadas. Para garantir que a rota passa por todas as ilhas, impomos que cada nó tenha exactamente uma ligação de saída e uma de entrada, respeitando a conservação de fluxo:

```python
# Função Objectivo: Minimizar a distância total percorrida
prob += pulp.lpSum(dists\[i]\[j] \* x\[i, j] for i in range(n) for j in range(n) if i != j)

# Restrições de Conservação de Fluxo: cada ilha tem 1 saída e 1 entrada
for i in range(n):
    prob += pulp.lpSum(x\[i, j] for j in range(n) if j != i) == 1 # leaves i
    prob += pulp.lpSum(x\[j, i] for j in range(n) if j != i) == 1 # enters i
```

#### C. Eliminação de Subciclos (MTZ)

Para evitar que o solucionador crie circuitos isolados que não cubram toda a rede, aplicamos as restrições MTZ,. Esta lógica força uma sequência cronológica na visita, impedindo o retorno ao ponto inicial antes de passar por todos os nós:

```python
# Restrições MTZ para impedir subciclos (subtours)
for i in range(n):
    for j in range(n):
        if i != j and i != depot and j != depot:
            prob += u\[i] - u\[j] + n \* x\[i, j] <= n - 1
```
O código actua como um arquitecto e um construtor. O Python (arquitecto) desenha o projecto usando a técnica **MTZ**, que funciona como dar uma "senha de entrada" a cada ilha; para avançarmos na rota, a senha da ilha seguinte tem de ser maior que a anterior, o que impede que o computador se perca em pequenos circuitos isolados. Quando o projecto está pronto, o solucionador (construtor) utiliza o **Branch-and-Cut** para testar milhares de combinações de "interruptores" binários (ligar ou desligar uma estrada entre ilhas). Ele descarta rapidamente as opções impossíveis e garante que, no final, a CVNet tenha a rota de sincronização mais curta e eficiente do ponto de vista matemático.
## 5. Resultados para CVNet<a id="resultados"></a>

## 6. Conclusões<a id="conclusões"></a>

## 7. Referências Bibliográficas<a id="referencias"></a>
