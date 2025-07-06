import random
import os
import time
import copy

# Constantes do jogo
VAZIO = ' '
PAREDE = '#'
FRUTA = '*'
PORTAL = '@'

# Constantes de retorno das funções
MOV_INVALIDO = 0
MOV_VALIDO   = 1
VITORIA      = 2
MORTE        = 3

# Variáveis globais para manter o estado (necessário após remover a classe)
# Estas variáveis simulam os atributos da classe SnakeFalls.
# Elas serão passadas como parâmetros para as funções.
pontos_globais = 0
portais_abertos_globais = False


def copia_estado(T, S, pontos, portais_abertos):
    """Cria uma cópia do estado atual para o histórico"""
    return {
        'T': [linha.copy() for linha in T],
        'S': S.copy(),
        'pontos': pontos,
        'portais_abertos': portais_abertos
    }

def criar_fruta(T, S):
    """Cria uma fruta em posição aleatória no tabuleiro T,
    evitando posições ocupadas pela cobra ou por outros elementos fixos.
    """
    posicoes_vazias = []
    for y in range(len(T)):
        for x in range(len(T[y])):
            # Verifica se a posição é vazia e não está ocupada por nenhum segmento da cobra
            if T[y][x] == VAZIO and (x, y) not in S:
                posicoes_vazias.append((x, y))

    if posicoes_vazias:
        x, y = random.choice(posicoes_vazias)
        T[y][x] = FRUTA
        return True # Fruta criada
    return False # Não foi possível criar fruta


def LeNivel(nome_arquivo):
    """Carrega um nível a partir de um arquivo e retorna o tabuleiro (T) e a cobra (S)."""
    global pontos_globais, portais_abertos_globais
    T = []
    S = []
    pontos_globais = 0 # Reinicia pontos ao carregar novo nível
    portais_abertos_globais = False # Reinicia portais

    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()

    for y, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha:
            continue

        linha_tabuleiro = []
        for x, char in enumerate(linha):
            if char.isdigit():
                idx = int(char)
                # Garante que a lista S tenha o tamanho certo
                while len(S) <= idx:
                    S.append(None)
                S[idx] = (x, y)
                linha_tabuleiro.append(VAZIO)
            else:
                linha_tabuleiro.append(char)

        T.append(linha_tabuleiro)

    # Verifica se tem fruta, senão cria uma
    if not any(FRUTA in linha for linha in T):
        criar_fruta(T, S)
            
    # O histórico (H) será gerenciado na função main, ou na primeira chamada de MoveCobra

    return T, S


def ImprimeEstadoDoJogo(T, S):
    """Imprime o estado atual do jogo."""
    os.system('cls' if os.name == 'nt' else 'clear')

    # Copia do tabuleiro para não modificar o original
    tabuleiro_impressao = [linha.copy() for linha in T]

    # Adiciona a cobra ao tabuleiro de impressão
    for i, (x, y) in enumerate(S):
        # Verifica se as coordenadas são válidas antes de tentar acessar
        for i, (x, y) in enumerate(S):
            if (x, y) is None:
                continue
            if 0 <= y < len(tabuleiro_impressao) and 0 <= x < len(tabuleiro_impressao[0]):
                tabuleiro_impressao[y][x] = str(i)
            else:
            # Se alguma parte da cobra está fora dos limites visíveis, isso pode indicar um problema
            # ou que a cobra está caindo para fora da tela.
            pass # Não faz nada, a parte fora da tela não é impressa

    # Imprime o tabuleiro
    print(len(T[0]))
    for linha in tabuleiro_impressao:
        print("".join(linha))   # Corrigido aqui o uso do join
    print(len(T[0]))

    # Informações do jogo
    print(f"Pontos: {pontos_globais}")
    print(f"Tamanho da cobra: {len(S)}")
    if portais_abertos_globais:
        print("Portais ativos!")


def AbrePortal(T):
    """Abre portais no tabuleiro se não existirem."""
    global portais_abertos_globais

    # Verifica se já existem portais no tabuleiro
    if any(PORTAL in linha for linha in T):
        return False # Já existem portais, não abre novos
            
    posicoes_vazias = []
    for y in range(len(T)):
        for x in range(len(T[y])):
            # Garante que a posição esteja vazia e não seja parte da cobra
            if T[y][x] == VAZIO and (x, y) not in S:
                posicoes_vazias.append((x, y))

    if len(posicoes_vazias) >= 2:
        portal1, portal2 = random.sample(posicoes_vazias, 2)
        T[portal1[1]][portal1[0]] = PORTAL
        T[portal2[1]][portal2[0]] = PORTAL
        portais_abertos_globais = True
        return True
    return False

def PosicaoCobra(S, parte):
    """Devolve a posição [x,y] de uma parte do corpo da cobra."""
    if parte == 'cabeca':
        return list(S[0]) if S else None
    elif parte == 'cauda':
        return list(S[-1]) if S else None
    elif isinstance(parte, int) and 0 <= parte < len(S):
        return list(S[parte])
    else:
        return None

def copia_estado(obj):
    return copy.deepcopy(obj)

def MoveCobra(c, T, S, H):
    """
    Move a cobra na direção especificada.
    Retorna MOV_VALIDO, MOV_INVALIDO, VITORIA ou MORTE.
    """
    global pontos_globais, portais_abertos_globais

    # Salva o estado atual no histórico antes de mover
    H.append((copia_estado(S), copia_estado(pontos_globais), copia_estado(portais_abertos_globais)))
    if len(H) > 10:  # Limita o histórico
        H.pop(0)
    
    # Obtém posição da cabeça
    if not S:
        return MORTE
    cabeca_x, cabeca_y = S[0]
    nova_x, nova_y = cabeca_x, cabeca_y

    # Calcula nova posição da cabeça
    if c == 'c':  # Cima
        nova_y -= 1
    elif c == 'b':  # Baixo
        nova_y += 1
    elif c == 'e':  # Esquerda
        nova_x -= 1
    elif c == 'd':  # Direita
        nova_x += 1
    else:
        return MOV_INVALIDO # Comando não reconhecido

    # Verifica se saiu do tabuleiro (bordas)
    if not (0 <= nova_y < len(T) and 0 <= nova_x < len(T[0])):
        return MORTE

    # Verifica colisão com paredes
    if T[nova_y][nova_x] == PAREDE:
        return MORTE

    # Verifica colisão com próprio corpo (exceto cauda que vai sair se não comer fruta)
    if (nova_x, nova_y) in S[:-1]:
        return MORTE

    # Verifica portal
    if T[nova_y][nova_x] == PORTAL and portais_abertos_globais:
        # Encontra o outro portal
        outros_portais = []
        for y in range(len(T)):
            for x in range(len(T[y])):
                if T[y][x] == PORTAL and (x, y) != (nova_x, nova_y):
                    outros_portais.append((x, y))
        if outros_portais:
            nova_x, nova_y = random.choice(outros_portais)
            if T[nova_y][nova_x] == PAREDE:
                return MORTE

    # Move a cobra: Adiciona nova cabeça
    S.insert(0, (nova_x, nova_y))

    comeu_fruta = False
    # Verifica se comeu fruta
    if T[nova_y][nova_x] == FRUTA:
        T[nova_y][nova_x] = VAZIO # Remove a fruta do tabuleiro
        pontos_globais += 1
        comeu_fruta = True
        criar_fruta(T, S) # Cria nova fruta
        # A cada 5 pontos, abre portais (se ainda não abertos)
        if pontos_globais > 0 and pontos_globais % 5 == 0:
            AbrePortal(T)
    
    if not comeu_fruta:
        S.pop()  # Remove cauda se não comeu fruta (mantém o mesmo tamanho)

    # Você pode adicionar uma condição de vitória aqui, se desejar.
    # Exemplo: vitória se todos os espaços livres forem ocupados pela cobra.
    # if ...: return VITORIA

    return MOV_VALIDO


def VerificaSuporte(T, S):
    """Verifica se a cobra tem suporte para não cair."""
    if not S:
        return True # Cobra vazia não cai

    # A cobra como um todo tem suporte se pelo menos um de seus segmentos tiver suporte.
    # Ou se a cabeça estiver na última linha.
    for x, y in S:
        # Se a parte da cobra está na última linha, ela tem suporte
        if y == len(T) - 1:
            return True
        # Se a posição abaixo da parte da cobra não é VAZIO, ela tem suporte
        if T[y+1][x] != VAZIO:
            return True
        # Note: Se a posição abaixo for ocupada por OUTRA PARTE da cobra, isso também é suporte.
        # Mas a forma como a queda funciona no Snake Falls é que a cobra cai como um todo se não houver NADA embaixo.
        # Portanto, se T[y+1][x] for VAZIO, mas S contém (x, y+1), isso é um suporte.
        # Precisamos verificar isso explicitamente:
        if (x, y+1) in S:
            return True # O segmento abaixo é parte da própria cobra, então há suporte.
            
    return False


def QuedaCobra(T, S, H):
    """
    Faz a cobra cair se não tiver suporte.
    Retorna MOV_VALIDO ou MORTE.
    """
    global pontos_globais, portais_abertos_globais
    
    if VerificaSuporte(T, S):
        return MOV_VALIDO # Não há queda, então o movimento é válido

    # Salva estado no histórico antes da queda
    H.append(copia_estado(T, S, pontos_globais, portais_abertos_globais))
    if len(H) > 10:
        H.pop(0)

    # Move cada segmento para baixo
    for i in range(len(S)):
        x, y = S[i]
        S[i] = (x, y + 1)
        
        # Verifica se algum segmento caiu para fora do tabuleiro durante a queda
        if S[i][1] >= len(T):
            return MORTE
            
    # Verifica colisões da cabeça após a queda
    cabeca_x, cabeca_y = S[0]
    
    # Colisão com parede após a queda
    if T[cabeca_y][cabeca_x] == PAREDE:
        return MORTE
            
    # Colisão consigo mesma após a queda
    if (cabeca_x, cabeca_y) in S[1:]: # Verifica se a cabeça colidiu com o corpo (exceto ela mesma)
        return MORTE

    # Colisão com fruta após a queda
    comeu_fruta = False
    if T[cabeca_y][cabeca_x] == FRUTA:
        T[cabeca_y][cabeca_x] = VAZIO
        pontos_globais += 1
        comeu_fruta = True
        criar_fruta(T, S)
        
        # A cada 5 pontos, abre portais (se ainda não abertos)
        if pontos_globais > 0 and pontos_globais % 5 == 0:
            AbrePortal(T)

    if not comeu_fruta:
        # Se a cobra não comeu fruta, mas caiu, e se ela não encolher na queda,
        # ela precisa "empurrar" o rabo para a nova posição.
        # No entanto, a regra original do seu código era remover a cauda se não comeu.
        # Aqui, a queda significa que a cobra efetivamente "alongou" para baixo.
        # Para manter o tamanho, se não comeu, a cauda é removida.
        # Mas para a queda, o tamanho é mantido até o próximo movimento explícito ou comida de fruta.
        # A forma como a queda é tratada aqui é que a cobra inteira "desce", então o comprimento se mantém.
        # Se a lógica é que ela só encolhe com um 'MoveCobra' sem comer, então S.pop() não é chamado aqui.
        # Para o propósito do EP, geralmente a queda não altera o comprimento.
        pass # Não remove a cauda na queda se não comeu.

    return MOV_VALIDO


def Desfaz(T, S, H):
    """Desfaz o último movimento usando o histórico."""
    global pontos_globais, portais_abertos_globais
    if not H:
        return False
        
    estado_anterior = H.pop()
    T.clear()
    T.extend(estado_anterior['T'])
    S.clear()
    S.extend(estado_anterior['S'])
    pontos_globais = estado_anterior['pontos']
    portais_abertos_globais = estado_anterior['portais_abertos']
    return True
    
# A função main é fornecida pronta e não deve ser alterada:

def main():
    game_name = r"""
 __             _            ___     _ _     
/ _\_ __   __ _| | _____    / __\_ _| | |___ 
\ \| '_ \ / _` | |/ / _ \  / _\/ _` | | / __|
_\ \ | | | (_| |   <  __/ / / | (_| | | \__ \
\__/_| |_|\__,_|_|\_\___| \/   \__,_|_|_|___/
                                             
"""
    print(game_name)
    print("*** Snake Falls - versão 1.0 ***")
    falha_leitura = True
    while falha_leitura:
        nivel_input = input("Escolha a fase [1-24]: ")
        try:
            nivel = int(nivel_input)
            if not (1 <= nivel <= 24): # Adicionado para garantir que o nível esteja dentro de um alcance razoável de arquivos
                raise ValueError
            nome_arquivo = f"level{nivel:02d}.txt" # Formato alterado para f-string para consistência
            T,S = LeNivel(nome_arquivo)
            falha_leitura = False
        except ValueError:
            print("Número de fase inválido. Por favor, digite um número entre 1 e 24.")
            falha_leitura = True
        except FileNotFoundError: # Adicionado para lidar com o erro de arquivo não encontrado
            print(f"Fase '{nome_arquivo}' não disponível.")
            falha_leitura = True
        except Exception as e: # Captura outros erros inesperados na leitura
            print(f"Ocorreu um erro ao carregar a fase: {e}")
            falha_leitura = True

    H = [] # Histórico, agora gerenciado pelo main
    continua = True
    ImprimeEstadoDoJogo(T, S)
    while continua: #laço principal
        print("Opções: e (esquerda), d (direita),")
        print("\tc (cima), b (baixo),")
        print("\tv (voltar/desfazer), s (sair).")
        c = input("Escolha um comando: ")
        
        # Normaliza o input para as funções
        if c == 's':
            continua = False
        elif c == 'v':
            r = Desfaz(T, S, H)
            if not r:
                print("Não há movimentos anteriores.")
            ImprimeEstadoDoJogo(T, S)
        else: # Movimentos de cobra
            # Adapta as entradas para 'w', 's', 'a', 'd' que sua função MoveCobra esperava
            # para 'c', 'b', 'e', 'd' que o main espera.
            if c == 'c': cmd_move = 'c' # Cima
            elif c == 'b': cmd_move = 'b' # Baixo
            elif c == 'e': cmd_move = 'e' # Esquerda
            elif c == 'd': cmd_move = 'd' # Direita
            else:
                cmd_move = 'X' # Força MOV_INVALIDO para comando desconhecido
            
            r = MoveCobra(cmd_move, T, S, H)
            
            if r == MOV_INVALIDO:
                print("Movimento inválido")
            elif r == VITORIA:
                print("Vitória! Parabéns!")
                continua = False
            elif r == MORTE:
                print("GAME OVER")
                continua = False
            else: # MOV_VALIDO, então verifica a queda
                r = QuedaCobra(T, S, H)
                if r == MORTE:
                    print("GAME OVER")
                    continua = False
            ImprimeEstadoDoJogo(T, S)


# Não altere o código abaixo:
if __name__ == "__main__":
    main()
