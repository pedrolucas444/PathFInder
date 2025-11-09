# PathFinder - Resolvendo o Labirinto 2D com o Algoritmo A*

## Sobre o Projeto
O **PathFinder** é um projeto educativo desenvolvido para demonstrar a aplicação prática do **Algoritmo A\*** (A-Star) na resolução de labirintos bidimensionais (2D).  
O programa encontra o **menor caminho entre dois pontos (S e E)** em um labirinto, evitando obstáculos e utilizando uma **função heurística** para otimizar a busca.

Este projeto tem como objetivo ilustrar como algoritmos de busca informada funcionam na prática, sendo amplamente utilizados em **robótica, jogos e sistemas de navegação**.

---

## Contexto
Imagine um **robô de resgate** posicionado em um ponto inicial `S`, que precisa chegar ao ponto final `E` dentro de um labirinto cheio de obstáculos (`1`).  
O **Algoritmo A\*** ajuda o robô a **planejar a rota mais curta possível**, considerando tanto o custo do caminho já percorrido quanto uma **estimativa da distância restante** até o destino.

---

## Objetivo
Implementar o **Algoritmo A\*** para encontrar o **menor caminho em um labirinto 2D**, considerando:

- Movimentos válidos (cima, baixo, esquerda, direita e diagonais opcionais).  
- Células livres e obstáculos.  
- Custos de movimento uniformes (ou ponderados).  
- Heurística baseada na **distância de Manhattan** (ou diagonal).  
- Visualização opcional do processo com **Pygame**.

---

## Regras do Labirinto

- O labirinto é representado por uma **matriz 2D**, onde:
  - `S`: ponto inicial (**Start**).  
  - `E`: ponto final (**End**).  
  - `0`: célula livre.  
  - `1`: obstáculo (impassável).  
  - `2–9`: célula com custo adicional de movimento.  

### Exemplo de entrada:
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```

---

## O que é o Algoritmo A*?

O **A\*** é um algoritmo de busca heurística que encontra o **menor caminho** entre dois pontos em um grafo ou grade.  
Ele combina duas informações:

- **g(n)**: o custo do caminho percorrido até o nó atual.  
- **h(n)**: a estimativa da distância até o destino (heurística).  

A função de avaliação é definida por:

\[
f(n) = g(n) + h(n)
\]

A cada iteração, o algoritmo escolhe o nó com o menor valor de `f(n)`, equilibrando **eficiência (heurística)** e **segurança (caminho real percorrido)**.

---

## Heurística Utilizada

O projeto utiliza a **Distância de Manhattan**, definida como:

\[
h(n) = |x_{atual} - x_{final}| + |y_{atual} - y_{final}|
\]

Essa heurística é ideal para movimentos em **quatro direções**.  
Quando o movimento diagonal é permitido, também é possível usar a **Distância Diagonal**:

\[
h(n) = \max(|x_{atual} - x_{final}|, |y_{atual} - y_{final}|)
\]

---

## Passos do Algoritmo

1. **Inicialização:** o nó inicial é adicionado à lista aberta.  
2. **Seleção:** escolhe-se o nó com o menor valor `f(n)`.  
3. **Expansão:** gera-se os vizinhos válidos (cima, baixo, esquerda, direita, e diagonais se habilitadas).  
4. **Cálculo:** atualiza-se o custo `g(n)` e estima-se `h(n)` para cada vizinho.  
5. **Verificação:** se o destino for alcançado, o caminho é reconstruído.  
6. **Encerramento:** se a lista aberta estiver vazia e o destino não for encontrado, o labirinto não possui solução.

---

## Estrutura do Código

### `main.py`
Contém toda a lógica principal do projeto:

- **ler_labirinto(linhas)**  
  Lê as linhas do labirinto e converte em uma matriz 2D.  
  Valida os pontos de início (`S`) e fim (`E`).

- **busca_a_estrela(grade, inicio, fim, heuristica, visualizar)**  
  Implementa o **Algoritmo A\***, utilizando filas de prioridade (`heapq`) para determinar a ordem de exploração.

- **distancia_manhattan(a, b)**  
  Calcula a distância heurística entre dois pontos.

- **mostrar_caminho(caminho)**  
  Exibe a lista de coordenadas do caminho encontrado.

- **mostrar_labirinto(grade, caminho, inicio, fim)**  
  Exibe o labirinto no terminal com o caminho marcado por `*`.

- **desenhar_grade(...)** *(opcional)*  
  Mostra a execução passo a passo do algoritmo em tempo real usando **Pygame**.

---

## 🖥️ Execução

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

Ativar o ambiente:

- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

---

### 2. Executar o script principal

```bash
python main.py
```

Durante a execução, insira as linhas do labirinto manualmente e digite `fim` para encerrar a entrada.

---

### 3. Exemplo de uso

#### Entrada:
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
fim
```

#### Saída:
```
Caminho encontrado:
(0,0) -> (1,0) -> (1,1) -> (2,1) -> (3,1) -> (3,2) -> (3,3)

Labirinto com caminho:
S . 1 . .
* * 1 . 1
1 * 1 . .
1 * * E 1
```

Se **Pygame** estiver instalado, será aberta uma janela mostrando o progresso do algoritmo em tempo real.

---

##  Requisitos

- **Python 3.13.0** (ou superior)  
- **Bibliotecas padrão** do Python  
- **Pygame (opcional)** para visualização gráfica:
  ```bash
  pip install pygame
  ```

---

## Validações

O programa verifica:
- Se o ponto inicial `S` e o final `E` estão presentes.  
- Se todas as linhas têm o mesmo número de colunas.  
- Se há um caminho possível entre `S` e `E`.  
- Se há caracteres inválidos no labirinto.

Caso não exista solução, a mensagem `"Sem solução"` será exibida.

---

## Exemplo de Labirinto Sem Solução

Entrada:
```
S 1 1
1 0 1
1 1 E
fim
```

Saída:
```
Sem solução
```

---

## Visualização (opcional com Pygame)

As cores utilizadas são:

| Cor | Significado |
|------|--------------|
| 🔵 Azul | Ponto inicial (S) |
| 🟢 Verde | Ponto final (E) |
| 🟥 Vermelho | Obstáculos |
| 🟣 Magenta | Células já exploradas |
| 🟦 Ciano | Células na lista aberta |
| 🟨 Amarelo | Caminho final encontrado |

---

## 📜 Licença

Este projeto está licenciado sob a **Licença MIT**.

---

## ✍️ Autores

- Gustavo Ceolin Silva Veloso
- Henrique Pinto Santos
- Pedro Araújo Franco
- Pedro Lucas Sousa e Silva
