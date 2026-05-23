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

O problema apresentado é uma variante de um problema clássico frequentemente designado na literatura internacional como _Traveling Salesman Problem_ (TSP), é um dos problemas mais emblemáticos e estudados no campo da otimização combinatória e da investigação operacional. Na sua definição clássica, o problema descreve um vendedor que necessita de visitar um conjunto específico de cidades exatamente uma vez, regressando à cidade de origem no final do percurso. O objetivo fundamental é identificar a rota que minimiza a distância total percorrida ou o custo associado à viagem [@gutin2007traveling, p 20].

Embora a sua formulação pareça simples, o TSP é classificado como um problema **NP-difícil** (_NP-hard_), o que significa que não existe um algoritmo conhecido capaz de encontrar a solução ótima em tempo computacional reduzido à medida que o número de cidades aumenta. Por exemplo, enquanto um problema com 10 cidades apresenta um número gerível de soluções possíveis, um cenário com 50 cidades já ultrapassa as $10^{62}$ rotas viáveis [@hillierlieberman, p 604].

### O Contexto CVNet e a Analogia com o PCV

O projeto da **Agência Nacional de Redes de Cabo Verde (CVNet)** enquadra-se perfeitamente na estrutura matemática do PCV. No cenário proposto para o ano 2040, as 10 ilhas de Cabo Verde representam os "nós" (ou cidades) de uma rede de comunicação de alta velocidade. A necessidade de sincronização diária entre os data centers localizados em cada ilha exige a criação de uma rota eficiente que interligue todos os pontos.

A semelhança entre o desafio da CVNet e o PCV clássico é direta:

1. **Nós da Rede:** As 10 ilhas de Cabo Verde (Santo Antão, São Vicente, etc.) equivalem às cidades que o caixeiro deve visitar.
2. **Custo de Ligação:** A matriz de distâncias fornecida pela CVNet representa o "custo" $c\_{ij}$ de transmitir dados entre a ilha $i$ e a ilha $j$.
3. **Objetivo Operacional:** Minimizar a latência ou o custo total de comunicação, garantindo que a "sincronização" passe por todos os centros de dados uma única vez e retorne ao ponto inicial para fechar o ciclo de atualização.

Assim, resolver o problema da CVNet implica modelar a infraestrutura das ilhas como um grafo e aplicar técnicas de otimização para garantir que a transmissão de dados seja feita através da rota Hamiltoniana mais curta possível.

## 2. Formulações Matemáticas<a id="formulacoes"></a>
A modelação matemática é o processo de transformar um problema real (a rede da CVNet) numa linguagem que um computador consiga resolver (Arenales et al., 2007, p. 12). Para o Problema do Caixeiro Viajante (TSP), existem diferentes "mapas matemáticos" possíveis.

### 2.1. Quatro Formas de Ver o Problema

1. **Visão por Sequência (Permutações Lineares):** Imagina o TSP como uma lista ordenada das 10 ilhas. O objectivo é reordenar essa lista de forma a que a soma das distâncias entre ilhas vizinhas na lista seja a menor possível (Gutin & Punnen, 2002, p. 4). É como organizar as músicas numa _playlist_ para que a "viagem" entre elas seja a mais suave.

2. **Visão por Decisões Sim/Não (Programação Linear Inteira - DFJ):** Aqui, olhamos para cada ligação possível entre ilhas e perguntamos: "Usamos esta ligação na nossa rota?". Atribuímos o valor **1** se a resposta for "Sim" e **0** se for "Não" (Arenales et al., 2007, p. 190; Gutin & Punnen, 2002, p. 16).  É como desenhar um traço entre duas ilhas num mapa ou deixar o espaço em branco.

3. **Visão por Interacções (Programação Quadrática):** Nesta abordagem, o custo de escolher uma ligação depende da escolha da ligação anterior. É uma formulação mais complexa, usada quando existem custos extra por "mudar de direcção" (Gutin & Punnen, 2002, p. 22; Hillier & Lieberman, 2006, p. 555).

4. **Visão de Escoamento (Fluxos em Redes):** Imagina que enviamos uma "mercadoria" da primeira ilha. Para garantir que passamos por todas, cada ilha tem de receber uma unidade e passar o resto para a seguinte (Gutin & Punnen, 2002, p. 20; Bazaraa et al., 2009, p. 445).

### 2.2. Modelação do Problema CVNet

Para resolver o caso da CVNet, utilizaremos a **Programação Linear Inteira**, por ser a mais robusta e clara para 10 localizações (Arenales et al., 2007, p. 190).

**As nossas ferramentas matemáticas:**

* **Variáveis ($x\_{ij}$):** O nosso interruptor. $x\_{ij} = 1$ se os dados viajam da ilha $i$ para a ilha $j$, e $0$ caso contrário (Hillier & Lieberman, 2006, p. 463).
* **Objectivo:** Minimizar a soma de todos os custos ($c\_{ij}$) das ligações que "ligamos" (Gutin & Punnen, 2002, p. 30).

**As Regras do Jogo (Restrições):**

1. **Entrada e Saída:** Cada ilha tem de ter exactamente uma ligação de entrada e uma de saída. Ninguém fica isolado (Arenales et al., 2007, p. 190).
2. **Eliminação de Subciclos (Subtours):** Esta é a regra mais importante. Ela impede que o computador crie dois circuitos separados (por exemplo, um ciclo entre 3 ilhas no norte e outro entre 7 ilhas no sul). Queremos uma rota única que ligue as 10 ilhas (Gutin & Punnen, 2002, p. 30; Hillier & Lieberman, 2006, p. 604).

### 2.3. Justificação da Escolha

Escolhemos a **Programação Linear Inteira (Formulação DFJ)** para a CVNet pelos seguintes motivos:

1. **Precisão Total:** Com apenas 10 ilhas, este modelo garante que encontramos a **solução óptima** (a rota absolutamente mais curta), e não apenas uma "boa rota" (Hillier & Lieberman, 2006, p. 604).
2. **Simetria:** Como a distância de Santo Antão para o Sal é a mesma do Sal para Santo Antão, o problema é simétrico. Isto reduz o esforço do computador para metade (Hillier & Lieberman, 2006, p. 603; Gutin & Punnen, 2002, p. 30).
3. **Facilidade em Python:** Esta formulação é traduzida de forma muito directa para bibliotecas de optimização (como o PuLP ou Pyomo), facilitando a implementação prática que faremos na Secção 4 (Arenales et al., 2007, p. 163).

## 3. Complexidade e Métodos de Resolução<a id="complexidade-e-metodos"></a>
A eficiência de um algoritmo de optimização é frequentemente medida pela sua capacidade de encontrar a solução óptima num tempo de processamento razoável (Hillier & Lieberman, 2006, p. 151). No caso do Problema do Caixeiro Viajante (TSP), deparamo-nos com uma das classes de problemas mais desafiantes da computação.

### 3.1. Complexidade Computacional e a Natureza NP-difícil

O TSP é classificado como um problema **NP-difícil** (_NP-hard_) (Hillier & Lieberman, 2006, p. 151; Gutin & Punnen, 2002, p. 476). Isto significa que não existe um algoritmo conhecido que consiga garantir a solução óptima em tempo polinomial à medida que o número de nós ($n$) aumenta.

O desafio reside na **explosão combinatória**: para um problema simétrico com $n$ cidades, existem $(n-1)! / 2$ rotas possíveis (Hillier & Lieberman, 2006, p. 603). Se tivermos apenas 10 cidades (como no caso da CVNet), o número de rotas é gerível (181.440). Contudo, se aumentarmos para 20 cidades, o número de soluções salta para cerca de $10^{16}$, e com 50 cidades ultrapassamos as $10^{62}$ rotas — um número superior à quantidade de átomos em sistemas galácticos (Hillier & Lieberman, 2006, p. 604).
### 3.2. Métodos de Resolução Exata: O Caminho da Perfeição

Os métodos exatos visam encontrar a rota absolutamente mínima, provando matematicamente que nenhuma outra é melhor.

* **Branch-and-Bound (Ramificação e Avaliação):** É uma estratégia de "dividir para conquistar". Como o problema total é demasiado grande, o algoritmo divide-o em subproblemas menores (ramificação). Ao mesmo tempo, ele calcula um limite (_bound_) para cada subproblema; se esse limite indicar que o subproblema não pode conter uma solução melhor do que a que já temos, o computador descarta-o sem precisar de o explorar até ao fim (avaliação). Imagine que procura um objecto numa casa com 10 divisões. Se olhar pela porta de uma divisão e vir que está vazia, não precisa de entrar e abrir todas as gavetas dessa sala. O _Branch-and-Bound_ "espreita pela porta" e descarta o que não interessa.

* **Cortes (Cutting Planes):** São restrições matemáticas adicionais que "limpam" o espaço de procura. O computador começa por resolver uma versão simplificada do problema onde as cidades podem ser visitadas "em fracções" (o que é impossível na realidade). Os cortes são equações que eliminam essas soluções impossíveis (fraccionárias) sem nunca retirar a solução real e inteira do mapa. É como esculpir uma estátua num bloco de pedra. Os cortes são os golpes de cinzel que retiram o excesso de pedra que não faz parte da figura final, aproximando-nos da forma perfeita.

### 3.3. Métodos Heurísticos e Meta-heurísticos: O Caminho da Rapidez

Quando o problema assume dimensões astronómicas, procuramos soluções "suficientemente boas" num tempo curto.

* **Heurísticas Locais:** São procedimentos baseados no senso comum e na intuição. Elas partem de uma solução inicial e tentam melhorá-la olhando apenas para a "vizinhança" imediata, fazendo pequenas trocas na rota até não conseguirem melhorar mais. É como um alpinista num nevoeiro cerrado que decide subir a montanha dando sempre um passo para onde o terreno parece mais inclinado para cima. Ele acabará por chegar ao topo de _uma_ montanha (um pico local), mas pode não ser a montanha mais alta da cordilheira.

* **Meta-heurísticas:** São "estratégias mestras" que guiam as heurísticas locais para que elas não fiquem presas em resultados medianos. Uma meta-heurística orquestra o processo, permitindo que o algoritmo aceite, por vezes, uma solução ligeiramente pior para conseguir "escapar" de um pico menor e encontrar o caminho para a montanha mais alta (o óptimo global). Se o nosso alpinista perceber que está num pico baixo, a meta-heurística é o plano que o obriga a descer um pouco para o vale para que ele possa explorar outra área e encontrar o Evereste.
  ### 3.4. Estratégia Aplicada à CVNet

Apesar da complexidade NP-difícil do TSP, o cenário da CVNet apresenta apenas **10 ilhas**. Para esta dimensão, a utilização de métodos heurísticos não se justifica, uma vez que um método exato (Programação Linear Inteira via _Branch-and-Cut_) consegue encontrar a solução óptima em milissegundos num computador comum (Hillier & Lieberman, 2006, p. 604). Assim, garantimos à CVNet a eficiência máxima teórica necessária para a sua sincronização de dados.


## 4. Implementação em Python<a id="python"></a>

A transição da teoria para a prática exige uma distinção clara entre dois pilares da Investigação Operacional: a **formulação do modelo** (a estrutura lógica do problema) e o **procedimento de resolução** (o motor matemático que encontra a resposta). Para o caso da CVNet, utilizaremos a linguagem **Python** e a biblioteca de modelação **PuLP** [@CoinorPulpPython] para realizar esta ponte.

### 4.1. O Binómio Modelo (MTZ) e Algoritmo (Branch-and-Cut)

É fundamental compreender que o código Python não "adivinha" a rota; ele comunica uma estrutura formal a um solucionador profissional.

* **A Formulação (O Modelo MTZ):** No código, implementamos a técnica de **Miller-Tucker-Zemlin (MTZ)**. Esta formulação é a "receita" que define o que constitui uma rota válida, utilizando variáveis binárias para decidir que ligações activar e variáveis contínuas auxiliares para ordenar a sequência de visita, garantindo a eliminação de _subtours_ de forma compacta [@hillierlieberman, p 36].
* **O Algoritmo (Branch-and-Cut):** Quando executamos o comando de resolução, o motor de optimização (como o solver CBC integrado no PuLP) aplica o algoritmo **Branch-and-Cut**. Este algoritmo é o "forno" que processa as equações MTZ, dividindo o problema em subproblemas (ramificação) e adicionando restrições matemáticas dinâmicas (cortes) até encontrar a solução absolutamente óptima para as 10 ilhas [@arenalesPesquisaOperacional2006, p256].


### 4.2. Tradução do Modelo em Código

A implementação em `tsp_cvnet.py` segue rigorosamente a anatomia de um problema de programação linear inteira.

#### A. Inicialização e Variáveis de Decisão

Primeiro, o problema é instanciado como uma minimização e as variáveis de decisão são criadas. A variável $x_{ij}$ assume valor 1 se a rota incluir o arco entre as ilhas $i$ e $j$, enquanto as variáveis $u_i$ são auxiliares para a ordenação MTZ:

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

Para evitar que o solucionador crie circuitos isolados que não cubram toda a rede, aplicamos as restrições MTZ,. Esta lógica força uma sequência cronológica na visita, impedindo o retorno ao ponto inicial antes de passar por todos os nós [@TechniquesSubtourElimination]
```python
# Restrições MTZ para impedir subciclos (subtours)
for i in range(n):
    for j in range(n):
        if i != j and i != depot and j != depot:
            prob += u\[i] - u\[j] + n \* x\[i, j] <= n - 1
```
O código actua como um arquitecto e um construtor. O Python (arquitecto) desenha o projecto usando a técnica **MTZ**, que funciona como dar uma "senha de entrada" a cada ilha; para avançarmos na rota, a senha da ilha seguinte tem de ser maior que a anterior, o que impede que o computador se perca em pequenos circuitos isolados. Quando o projecto está pronto, o solucionador (construtor) utiliza o **Branch-and-Cut** para testar milhares de combinações de "interruptores" binários (ligar ou desligar uma estrada entre ilhas). Ele descarta rapidamente as opções impossíveis e garante que, no final, a CVNet tenha a rota de sincronização mais curta e eficiente do ponto de vista matemático.
## 5. Resultados para CVNet<a id="resultados"></a>

Nesta secção, detalhamos a solução óptima encontrada para o problema de encaminhamento da CVNet. Utilizando a formulação de Programação Linear Inteira discutida anteriormente, o solucionador identificou a rota Hamiltoniana que minimiza o custo total de sincronização entre os data centers das 10 ilhas.

### 5.1. A Rota Óptima e o Custo Mínimo

Os resultados obtidos através da execução do código `tsp_cvnet.py` demonstram a eficácia dos métodos exatos para instâncias de dimensão controlada ($n=10$). 

**Os indicadores principais da solução são:**
* **Distância Total Percorrida:** 921.00 unidades.
* **Sequência de Sincronização:** 
    **Santiago $\rightarrow$ Maio $\rightarrow$ Boa Vista $\rightarrow$ Sal $\rightarrow$ São Nicolau $\rightarrow$ Santo Antão $\rightarrow$ São Vicente $\rightarrow$ Santa Luzia $\rightarrow$ Brava $\rightarrow$ Fogo $\rightarrow$ Santiago**.

Esta sequência constitui um **ciclo Hamiltoniano**, garantindo que cada ilha é visitada exatamente uma única vez antes de o fluxo de dados regressar ao ponto de origem para fechar o ciclo de actualização da rede.

### 5.2. Interpretação Geográfica e Operacional

A análise da rota revela que o modelo matemático priorizou o agrupamento de ilhas por proximidade geográfica, uma característica típica de soluções óptimas em problemas de optimização combinatória.

1. **Eficiência de Roteamento:** O percurso segue uma lógica de "vizinhança", minimizando os saltos de longa distância que elevariam a latência e o custo de comunicação.
2. **Invariância do Ciclo:** Conforme validado tecnicamente, o custo total de 921.00 unidades é uma propriedade do ciclo. Isto significa que a CVNet pode iniciar a sincronização em qualquer uma das ilhas (por exemplo, começar em São Vicente em vez de Santiago) e, desde que mantenha esta sequência circular, o custo total permanecerá inalterado.
3. **Garantia de Otimalidade:** Ao contrário de uma solução obtida por métodos heurísticos, que poderia fornecer apenas uma "boa rota", este resultado de 921.00 unidades é matematicamente provado como o menor possível, não existindo qualquer outra combinação entre as 181.440 rotas viáveis que seja superior em termos de custo.


## 6. Conclusões<a id="conclusões"></a>

## 7. Referências Bibliográficas<a id="referencias"></a>
