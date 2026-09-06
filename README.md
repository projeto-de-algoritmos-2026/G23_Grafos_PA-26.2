# Maze Runner — Comparação de Algoritmos de Busca em Grafos

Visualizador de buscas em labirintos com obstáculos e terrenos de diferentes custos, desenvolvido para a disciplina de **Projeto de Algoritmos**.

**Grupo:** 23 · **Período:** 2026.2 · **Conteúdo:** Grafos e caminhos mínimos

## Alunos

<table>
  <tr><th>Gabriel Ferreira</th><th>Luiz Henrique Tomaz Moreira</th></tr>
  <tr>
    <td align="center"><a href="https://github.com/diangellis"><img src="https://github.com/diangellis.png" width="120" alt="Foto de Gabriel Ferreira no GitHub"></a></td>
    <td align="center"><a href="https://github.com/luizhtmoreira"><img src="https://github.com/luizhtmoreira.png" width="120" alt="Foto de Luiz Henrique Tomaz Moreira no GitHub"></a></td>
  </tr>
  <tr>
    <td align="center">Matrícula: <strong>242004671</strong><br><a href="https://github.com/diangellis">@diangellis</a></td>
    <td align="center">Matrícula: <strong>242028735</strong><br><a href="https://github.com/luizhtmoreira">@luizhtmoreira</a></td>
  </tr>
</table>

## Sobre o projeto

O Maze Runner é uma aplicação gráfica educativa em Python que permite acompanhar como diferentes algoritmos resolvem um labirinto. O usuário escolhe uma busca e observa os nós explorados, a fronteira de busca e o caminho encontrado entre a entrada e a saída.

O objetivo é comparar estratégias de exploração e compreender a diferença entre encontrar uma rota, minimizar a quantidade de movimentos e minimizar o custo acumulado. Uma rota curta por terrenos caros pode custar mais que uma rota longa por terrenos baratos.

É possível executar um algoritmo individualmente ou comparar todas as opções em sequência no mesmo mapa. Ao final do modo comparativo, um ranking apresenta custo, tempo da busca animada, tamanho do caminho e nós expandidos.

## Algoritmos

- **BFS (Busca em Largura):** explora por níveis, usando uma fila. Encontra um caminho com o menor número de movimentos, mas não considera os custos dos terrenos.
- **DFS (Busca em Profundidade):** explora um ramo antes de voltar às alternativas, usando uma pilha. Encontra uma rota, sem garantir menor comprimento ou custo.
- **Dijkstra:** prioriza o menor custo acumulado, usando uma fila de prioridade. Encontra uma rota de custo mínimo nos terrenos do projeto.
- **A* (com diferentes heurísticas):** combina custo acumulado e estimativa do custo restante para orientar a exploração até o destino.

### Heurísticas do A*

O projeto possui **quatro algoritmos** e **seis opções de execução**, pois A* pode ser utilizado com três heurísticas:

| Heurística | Cálculo, com `dx` e `dy` como diferenças absolutas até o destino |
|---|---|
| Manhattan | `dx + dy` |
| Euclidiana | `sqrt(dx² + dy²)` |
| Chebyshev | `max(dx, dy)` |

Essas estimativas não superestimam o custo restante em uma grade com movimentos em quatro direções e custo mínimo de terreno igual a 1. Assim, as variantes utilizadas pelo projeto preservam a busca por um caminho de custo mínimo. Manhattan representa a distância mínima em movimentos sem obstáculos, não o custo exato de uma rota com paredes e terrenos variados.

## Capturas de tela

<table>
  <tr>
    <td align="center"><img src="assets/screenshots/bfs.png" width="420" alt="Execução do BFS resolvendo o labirinto"><br>BFS</td>
    <td align="center"><img src="assets/screenshots/dfs.png" width="420" alt="Execução do DFS resolvendo o labirinto"><br>DFS</td>
  </tr>
  <tr>
    <td align="center"><img src="assets/screenshots/dijkstra.png" width="420" alt="Execução do Dijkstra resolvendo o labirinto"><br>Dijkstra</td>
    <td align="center"><img src="assets/screenshots/astar_manhattan.png" width="420" alt="Execução do A* com heurística Manhattan resolvendo o labirinto"><br>A* (Manhattan)</td>
  </tr>
</table>

## Funcionalidades

- Geração de labirintos com paredes e terrenos de custos variados.
- Verificação de conectividade para garantir uma rota entre início e destino no mapa gerado.
- Animação dos nós visitados, da fronteira e da revelação do caminho encontrado.
- Execução individual ou sequencial das seis opções do menu.
- Comparação dos resultados no mesmo labirinto.
- Painel de métricas durante a execução e ranking ao final do modo comparativo.
- Configuração de tamanho da grade, semente e velocidade de animação pelo código.

## Modelagem em grafos

Cada célula livre representa um vértice. Células adjacentes se conectam por movimentos horizontais e verticais, sem diagonais. Paredes bloqueiam a passagem. O peso de um movimento corresponde ao custo de entrar na próxima célula.

| Elemento | Valor na grade | Efeito |
|---|---:|---|
| Parede | 0 | Bloqueia a passagem |
| Terreno plano | 1 | Menor custo |
| Lama | 3 | Custo intermediário |
| Água | 5 | Maior custo |

O custo do caminho soma os valores das células percorridas, excluindo a célula inicial. A configuração padrão utiliza **40 colunas e 26 linhas**, início em `(0, 0)`, destino em `(39, 25)` e semente `42`. Todas as buscas de uma sessão usam o mesmo mapa.

## Tecnologias e requisitos

- **Python 3.10 ou superior**, devido à sintaxe de anotações de tipos utilizada no código.
- **Pygame Community Edition (`pygame-ce`)**, declarado em [requirements.txt](requirements.txt) e importado como `pygame`.
- Ambiente desktop com suporte a janela gráfica.
- Fontes **IBM Plex Mono**, incluídas em `assets/fonts/`, com licença em [OFL.txt](assets/fonts/OFL.txt).

## Instalação e execução

Clone o projeto e entre na pasta:

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G23_Grafos_PA-26.2.git
cd G23_Grafos_PA-26.2
```

### Windows — PowerShell

Crie um ambiente virtual, instale a dependência e execute a aplicação. Estes comandos não exigem ativar o ambiente virtual:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

### Linux e macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Execute a partir da raiz do projeto e mantenha a pasta `assets/fonts/` junto ao código.

## Uso e controles

1. Abra o programa para acessar o menu de algoritmos.
2. Escolha uma busca pelas teclas numéricas ou pressione **T** para comparar todas.
3. Observe a exploração do labirinto e a revelação do caminho.
4. Após uma execução individual, pressione **Enter** para voltar ao menu.
5. No modo comparativo, aguarde as seis execuções e consulte o ranking final.

| Tecla | Ação |
|---|---|
| **1** | Executar BFS |
| **2** | Executar DFS |
| **3** | Executar Dijkstra |
| **4** | Executar A* com Manhattan |
| **5** | Executar A* com Euclidiana |
| **6** | Executar A* com Chebyshev |
| **T** | Rodar todas as opções em sequência, a partir do menu |
| **Enter** | Voltar ao menu após uma execução individual ou no ranking |
| **Esc** | Encerrar a aplicação |

## Métricas e ranking

| Métrica | Significado na implementação |
|---|---|
| Nós expandidos | Quantidade de posições registradas na ordem de exploração |
| Tempo | Tempo decorrido durante a busca animada, incluindo o ritmo dos frames |
| Passos | Quantidade de células no caminho, incluindo início e destino; os movimentos correspondem a esse valor menos 1 |
| Custo | Soma dos custos de entrada nas células do caminho, excluindo o início |

O ranking ordena por **menor custo**, depois por **menor tempo**, **menor tamanho do caminho** e **menos nós expandidos**, nessa ordem.

> O tempo exibido inclui a animação e depende dos frames e do computador. Não é uma medição isolada da velocidade de processamento dos algoritmos. BFS pode encontrar menos movimentos e, ainda assim, apresentar custo maior que Dijkstra ou A*.

## Configuração

Os parâmetros ficam em [maze_runner/config.py](maze_runner/config.py):

| Parâmetro | Padrão | Finalidade |
|---|---|---|
| `COLS`, `ROWS` | `40`, `26` | Dimensões da grade |
| `MAZE_SEED` | `42` | Semente da geração pseudoaleatória |
| `WALL_PROBABILITY` | `0.22` | Probabilidade de parede na geração |
| `SEARCH_STEPS_PER_FRAME` | `3` | Avanços da busca por frame |
| `SEARCH_FPS` | `40` | Frames por segundo durante a busca |
| `REVEAL_CELLS_PER_FRAME` | `2` | Células reveladas por frame no caminho final |
| `REVEAL_FPS` | `30` | Frames por segundo na revelação |
| `AUTO_ADVANCE_DELAY_S` | `1.5` | Pausa entre algoritmos no modo comparativo |

Para experimentar outro mapa, altere `MAZE_SEED` e reinicie o programa. Os custos e pesos de sorteio dos terrenos ficam em [maze_runner/grid.py](maze_runner/grid.py).

## Estrutura do projeto

```text
G23_Grafos_PA-26.2/
├── README.md
├── main.py                  # Ponto de entrada
├── requirements.txt         # Dependência gráfica
├── assets/fonts/            # Fontes IBM Plex Mono e licença
└── maze_runner/
    ├── __init__.py
    ├── config.py            # Grade e animação
    ├── grid.py              # Geração, conectividade e custo do caminho
    ├── algorithms/
    │   ├── __init__.py      # Registro das seis opções do menu
    │   ├── common.py        # Utilitários compartilhados
    │   ├── bfs.py
    │   ├── dfs.py
    │   ├── dijkstra.py
    │   ├── astar.py
    │   └── heuristics.py
    └── ui/
        ├── __init__.py
        ├── app.py           # Eventos e integração das telas
        ├── run.py           # Busca animada e métricas
        ├── screens.py       # Menu e ranking
        ├── chrome.py        # Componentes visuais
        ├── colors.py       # Paleta da interface
        └── fonts.py        # Carregamento das fontes
```

## 🎥 Apresentação do Projeto

[![Apresentação do Projeto](https://img.youtube.com/vi/p9Ocs_O742g/maxresdefault.jpg)](https://youtu.be/p9Ocs_O742g)
