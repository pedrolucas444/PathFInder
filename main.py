import heapq
import math
import sys

pygame_disponivel = False
try:
    import pygame
    pygame_disponivel = True
    TAMANHO_CELULA = 30
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERMELHO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AZUL = (0, 0, 255)
    AMARELO = (255, 255, 0)
    CIANO = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    CINZA = (200, 200, 200)
    LARANJA = (255, 165, 0)
except ImportError:
    print("Aviso: Pygame não encontrado. Visualização desativada.", file=sys.stderr)

class No:
    def __init__(self, posicao, pai=None):
        self.posicao = posicao
        self.pai = pai
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, outro):
        return self.posicao == outro.posicao
    def __lt__(self, outro):
        if self.f == outro.f:
            return self.h < outro.h
        return self.f < outro.f
    def __hash__(self):
        return hash(self.posicao)

def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def distancia_diagonal(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def ler_labirinto(linhas):
    grade = []
    inicio = None
    fim = None
    linhas_total = len(linhas)
    colunas = 0
    for r, linha in enumerate(linhas):
        linha_grade = []
        elementos = linha.split()
        if r == 0:
            colunas = len(elementos)
        elif len(elementos) != colunas:
            raise ValueError(f"Linha {r+1} tem número diferente de colunas.")
        for c, char in enumerate(elementos):
            if char == 'S':
                inicio = (r, c)
                linha_grade.append(1)
            elif char == 'E':
                fim = (r, c)
                linha_grade.append(1)
            elif char == '1':
                linha_grade.append(math.inf)
            else:
                try:
                    custo = int(char)
                    if custo < 0:
                        raise ValueError(f"Custo negativo '{char}' na linha {r+1}, coluna {c+1}")
                    linha_grade.append(max(1, custo))
                except ValueError:
                    raise ValueError(f"Caractere inválido '{char}' na linha {r+1}, coluna {c+1}")
        grade.append(linha_grade)
    if inicio is None:
        raise ValueError("Ponto inicial 'S' não encontrado.")
    if fim is None:
        raise ValueError("Ponto final 'E' não encontrado.")
    return grade, inicio, fim

def posicao_valida(posicao, grade):
    linhas, colunas = len(grade), len(grade[0])
    r, c = posicao
    return 0 <= r < linhas and 0 <= c < colunas and grade[r][c] != math.inf

def busca_a_estrela(grade, inicio, fim, permitir_diagonal=True, heuristica=distancia_diagonal, visualizar=False):
    if visualizar and not pygame_disponivel:
        print("Aviso: Visualização desativada (pygame ausente).", file=sys.stderr)
        visualizar = False

    no_inicio = No(inicio)
    no_fim = No(fim)
    lista_aberta = []
    heapq.heappush(lista_aberta, no_inicio)
    conjunto_aberto = {no_inicio.posicao}
    historico_aberto = []
    conjunto_fechado = set()
    origem = {}
    g_score = {(r, c): math.inf for r in range(len(grade)) for c in range(len(grade[0]))}
    g_score[inicio] = 0
    no_inicio.g = 0
    no_inicio.h = heuristica(inicio, fim)
    no_inicio.f = no_inicio.g + no_inicio.h
    tela = None
    relogio = None
    if visualizar:
        pygame.init()
        linhas, colunas = len(grade), len(grade[0])
        largura = colunas * TAMANHO_CELULA
        altura = linhas * TAMANHO_CELULA
        tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Busca A* - Visualização")
        relogio = pygame.time.Clock()
        historico_aberto.append(set(conjunto_aberto))
    caminho_encontrado = False
    no_atual = None
    while lista_aberta:
        if visualizar:
            try:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return None, set(), set()
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return None, set(), set()
            except pygame.error:
                visualizar = False
        no_atual = heapq.heappop(lista_aberta)
        if no_atual.posicao in conjunto_fechado:
            continue
        conjunto_fechado.add(no_atual.posicao)
        if no_atual.posicao in conjunto_aberto:
            conjunto_aberto.remove(no_atual.posicao)
        if no_atual.posicao == no_fim.posicao:
            caminho_encontrado = True
            break
        dados_vizinhos = []
        r, c = no_atual.posicao
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            viz = (r + dr, c + dc)
            if posicao_valida(viz, grade):
                movimento = 1
                custo = grade[viz[0]][viz[1]]
                dados_vizinhos.append((viz, movimento, custo))
        if permitir_diagonal:
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                viz = (r + dr, c + dc)
                if posicao_valida(viz, grade):
                    if grade[r + dr][c] == math.inf and grade[r][c + dc] == math.inf:
                        continue
                    movimento = math.sqrt(2)
                    custo = grade[viz[0]][viz[1]]
                    dados_vizinhos.append((viz, movimento, custo))
        for viz, movimento, custo in dados_vizinhos:
            if viz in conjunto_fechado:
                continue
            custo_total = movimento * custo
            tentativo_g = g_score[no_atual.posicao] + custo_total
            if tentativo_g < g_score.get(viz, math.inf):
                origem[viz] = no_atual.posicao
                g_score[viz] = tentativo_g
                h = heuristica(viz, fim)
                f = tentativo_g + h
                no_viz = No(viz, pai=no_atual)
                no_viz.g = tentativo_g
                no_viz.h = h
                no_viz.f = f
                heapq.heappush(lista_aberta, no_viz)
                conjunto_aberto.add(viz)
        if visualizar:
            try:
                historico_aberto.append(set(p for p in conjunto_aberto))
                desenhar_grade(tela, grade, None, inicio, fim, historico_aberto, conjunto_fechado, no_atual.posicao)
                pygame.display.flip()
                relogio.tick(15)
            except pygame.error:
                visualizar = False
    if caminho_encontrado and no_atual is not None:
        caminho = reconstruir(origem, no_atual)
        if visualizar:
            try:
                historico_aberto.append(set(p for p in conjunto_aberto))
                desenhar_grade(tela, grade, caminho, inicio, fim, historico_aberto, conjunto_fechado, no_atual.posicao)
                pygame.display.flip()
                esperar_saida()
                pygame.quit()
            except pygame.error:
                pass
        return caminho, historico_aberto, conjunto_fechado
    else:
        if visualizar:
            try:
                desenhar_grade(tela, grade, None, inicio, fim, historico_aberto, conjunto_fechado, None)
                pygame.display.flip()
                esperar_saida()
                pygame.quit()
            except pygame.error:
                pass
        return None, historico_aberto, conjunto_fechado

def reconstruir(origem, no_atual):
    caminho = []
    pos = no_atual.posicao
    while pos in origem:
        caminho.append(pos)
        if origem[pos] is None:
            break
        pos = origem[pos]
    if not caminho or caminho[-1] != pos:
        caminho.append(pos)
    return caminho[::-1]

def mostrar_caminho(caminho):
    if caminho:
        print("Caminho encontrado:")
        print(" -> ".join([f"({r},{c})" for r, c in caminho]))
    else:
        print("Sem solução")

def mostrar_labirinto(grade, caminho, inicio, fim):
    if not caminho:
        print("\nLabirinto sem solução:")
    else:
        print("\nLabirinto com caminho:")
    caminho_set = set(caminho) if caminho else set()
    for r in range(len(grade)):
        linha = []
        for c in range(len(grade[0])):
            pos = (r, c)
            if pos == inicio:
                linha.append('S')
            elif pos == fim:
                linha.append('E')
            elif pos in caminho_set:
                linha.append('*')
            elif grade[r][c] == math.inf:
                linha.append('█')
            else:
                custo = grade[r][c]
                linha.append(str(int(custo)) if custo > 1 else '.')
        print(" ".join(linha))

def desenhar_grade(tela, grade, caminho, inicio, fim, historico_aberto, conjunto_fechado, atual=None):
    if not pygame_disponivel or tela is None:
        return
    try:
        tela.fill(BRANCO)
        linhas, colunas = len(grade), len(grade[0])
        aberto_atual = historico_aberto[-1] if historico_aberto else set()
        for r in range(linhas):
            for c in range(colunas):
                cor = BRANCO
                pos = (r, c)
                custo = grade[r][c]
                if custo == math.inf:
                    cor = VERMELHO
                elif pos in conjunto_fechado:
                    cor = MAGENTA
                elif pos in aberto_atual:
                    cor = CIANO
                elif custo > 1:
                    intensidade = max(50, 255 - int(custo) * 15)
                    cor = (255, intensidade, 0)
                pygame.draw.rect(tela, cor, (c * TAMANHO_CELULA, r * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
                if custo != math.inf and custo > 1:
                    fonte = pygame.font.Font(None, 18)
                    texto = fonte.render(str(int(custo)), True, PRETO)
                    tela.blit(texto, (c * TAMANHO_CELULA + 5, r * TAMANHO_CELULA + 5))
                pygame.draw.rect(tela, CINZA, (c * TAMANHO_CELULA, r * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 1)
        if caminho:
            for i in range(len(caminho) - 1):
                p1 = (caminho[i][1] * TAMANHO_CELULA + TAMANHO_CELULA // 2, caminho[i][0] * TAMANHO_CELULA + TAMANHO_CELULA // 2)
                p2 = (caminho[i+1][1] * TAMANHO_CELULA + TAMANHO_CELULA // 2, caminho[i+1][0] * TAMANHO_CELULA + TAMANHO_CELULA // 2)
                pygame.draw.line(tela, AMARELO, p1, p2, 3)
        pygame.draw.rect(tela, AZUL, (inicio[1] * TAMANHO_CELULA, inicio[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
        pygame.draw.rect(tela, VERDE, (fim[1] * TAMANHO_CELULA, fim[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    except pygame.error:
        pass

def esperar_saida():
    if not pygame_disponivel:
        return
    esperando = True
    while esperando:
        try:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    esperando = False
        except pygame.error:
            esperando = False

def principal():
    print("Digite o labirinto. Use S para início, E para fim, 0 livre, 1 obstáculo, 2-9 custo. Digite 'fim' para encerrar.")
    linhas = []
    while True:
        linha = input().strip()
        if linha.lower() == 'fim':
            break
        linhas.append(linha)
    try:
        grade, inicio, fim = ler_labirinto(linhas)
        caminho, _, _ = busca_a_estrela(grade, inicio, fim, visualizar=True)
        if caminho:
            mostrar_caminho(caminho)
            mostrar_labirinto(grade, caminho, inicio, fim)
        else:
            print("Nenhum caminho encontrado.")
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    principal()