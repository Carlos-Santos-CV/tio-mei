# TSP_CVNet – Otimização de Roteamento para as Ilhas de Cabo Verde

Este projeto resolve o **Problema do Caixeiro Viajante (TSP)** aplicado à rede de data centers da CVNet, que interliga as 10 ilhas de Cabo Verde.  
O objetivo é encontrar a rota cíclica de menor distância total que visita cada ilha exatamente uma vez, garantindo a sincronização diária mais eficiente.

---

## Contexto

A Agência Nacional de Redes de Cabo Verde (CVNet) procura minimizar o custo total de comunicação associado à sincronização diária dos seus 10 data centers (um em cada ilha).  
A distância entre as ilhas é conhecida e fornecida pela matriz de distâncias.

A abordagem utilizada é a **formulação de Miller–Tucker–Zemlin (MTZ)**, uma técnica de programação linear inteira mista (MILP) compacta para o TSP, implementada em Python com a biblioteca **PuLP** e resolvida pelo *solver* **CBC** (Branch‑and‑Cut).

---

## Requisitos

- Python 3.11 (ou superior)
- PuLP 2.7.0

As dependências exatas estão listadas no ficheiro `requirements.txt`.

---

## Instalação

1. Clone o repositório ou copie os ficheiros para uma pasta local.
2. Crie e ative um ambiente virtual (opcional mas recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## Como executar

Por omissão, o script usa o ficheiro `input_data.json` que se encontra na mesma pasta.  
Para correr o programa:

```bash
python tsp_cvnet.py
```

Também pode especificar um ficheiro JSON diferente:

```bash
python tsp_cvnet.py caminho/para/outro_ficheiro.json
```

---

## Estrutura do ficheiro JSON de entrada

O ficheiro deve conter:

- **`islands`** – lista de strings com os nomes das ilhas.
- **`distances`** – matriz quadrada de distâncias (lista de listas de números).  
  A entrada `distances[i][j]` representa a distância da ilha `i` para a ilha `j`.
- **`start_island`** (opcional) – nome da ilha a usar como ponto de partida/chegada da rota.  
  Se omitido, assume a primeira ilha da lista.

Exemplo (`input_data.json`):

```json
{
    "islands": [
        "Santo Antão", "São Vicente", "São Nicolau", "Sal",
        "Boa Vista", "Maio", "Santiago", "Fogo", "Brava", "Santa Luzia"
    ],
    "distances": [
        [0, 36, 115, 255, 362, 413, 370, 319, 300, 97],
        [36, 0, 86, 228, 340, 401, 360, 305, 287, 44],
        ...
    ],
    "start_island": "Santo Antão"
}
```

> **Nota:** A matriz deve ser quadrada e simétrica. A distância de uma ilha a ela própria é sempre 0.

---

## Descrição do algoritmo (MTZ)

O modelo matemático é construído com as seguintes componentes:

- **Variáveis binárias** `x[i,j]`: 1 se a aresta da ilha `i` para a ilha `j` é usada, 0 caso contrário.
- **Variáveis auxiliares contínuas** `u[i]`: número de ordem da ilha `i` na rota (0 ≤ `u[i]` ≤ n‑1).  
  Ajudam a eliminar subciclos: para cada par `(i,j)` com `i ≠ j` e nenhum deles sendo o depósito, impõe‑se  
  `u[i] - u[j] + n * x[i,j] ≤ n - 1`.
- **Função objetivo:** minimizar a soma das distâncias das arestas ativas.
- **Restrições de grau:** cada ilha tem exatamente uma entrada e uma saída.
- **Fixação do depósito:** `u[depot] = 0` para remover simetrias.

O *solver* CBC resolve a formulação usando **Branch‑and‑Cut**, garantindo a solução ótima global para as 10 ilhas.

---

## Exemplo de saída

```
--- Optimal Route for CVNet (TSP) ---
Santo Antão -> São Vicente -> Santa Luzia -> São Nicolau -> Sal -> Boa Vista -> Maio -> Santiago -> Fogo -> Brava -> Santo Antão
Total distance: 921.00 units
```

A distância total é **921 unidades** e a rota é sempre um ciclo fechado.  
Qualquer rotação ou inversão deste ciclo (obtida alterando `start_island`) produz o mesmo custo total.

---

## Estrutura dos ficheiros

```
.
├── tsp_cvnet.py          # Script principal com o modelo TSP (MTZ)
├── input_data.json       # Dados das ilhas e distâncias (parametrizável)
├── requirements.txt      # Dependências Python
└── README.md             # Este ficheiro
```

---

## Licença

Projeto desenvolvido para fins académicos (Investigação Operacional).  
Sinta‑se livre para usar e adaptar de acordo com as suas necessidades.
