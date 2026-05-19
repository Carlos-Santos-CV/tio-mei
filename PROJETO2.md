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

## 5. Resultados para CVNet<a id="resultados"></a>

## 6. Conclusões<a id="conclusões"></a>

## 7. Referências Bibliográficas<a id="referencias"></a>
