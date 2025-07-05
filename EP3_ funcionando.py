
import random
import os
import time

# Constantes do jogo
VAZIO = ' '
PAREDE = '#'
FRUTA = '*'
CORPO = 'o'
CABECA = 'O'
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
    pontos_globais = 0  # Reinicia pontos ao carregar novo nível
    portais_abertos_globais = False  # Reinicia portais
    
    # Abre o arquivo manualmente
    f = open(nome_arquivo, 'r')
    linhas = f.readlines()
    f.close()  # Fecha o arquivo manualmente

    for y, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha:
            continue

        linha_tabuleiro = []
        for x, char in enumerate(linha):
            if char == CABECA:
                S.insert(0, (x, y))  # Cabeça no início da lista
                linha_tabuleiro.append(VAZIO)
            elif char == CORPO:
                S.append((x, y))  # Partes do corpo
                linha_tabuleiro.append(VAZIO)
            else:
                linha_tabuleiro.append(char)
        T.append(linha_tabuleiro)

    # Verifica se tem fruta, senão cria uma
    if not any(FRUTA in linha for linha in T):
        criar_fruta(T, S)    
    return T, S


'''
def ImprimeEstadoDoJogo(T, S):
    print()
'''


def ImprimeEstadoDoJogo(T, S): #Imprime o estado atual do jogo
    os.system('cls' if os.name == 'nt' else 'clear')
    tabuleiro_impressao = [linha.copy() for linha in T]# Copia do tabuleiro para não modificar o original

    for i, (x, y) in enumerate(S): # Adiciona a cobra ao tabuleiro de impressão
        # Verifica se as coordenadas são válidas antes de tentar acessar
        if 0 <= y < len(tabuleiro_impressao) and 0 <= x < len(tabuleiro_impressao[0]):
            tabuleiro_impressao[y][x] = CABECA if i == 0 else CORPO
        else:
            # Se alguma parte da cobra está fora dos limites visíveis, isso pode indicar um problema
            # ou que a cobra está caindo para fora da tela.
            pass # Não faz nada, a parte fora da tela não é impressa
    # Imprime o tabuleiro
    print('+' + '-' * len(T[0]) + '+')
    for linha in tabuleiro_impressao:
        print('|' + ''.join(linha) + '|')
    print('+' + '-' * len(T[0]) + '+')

    # Informações do jogo
    print(f"Pontos: {pontos_globais}")
    print(f"Tamanho da cobra: {len(S)}")
    if portais_abertos_globais:
        print("Portais ativos!")


def AbrePortal(T):
    T[0][0] = 'P'


def PosicaoCobra(S, parte):
    """Devolve a posição [x,y] de uma parte
    do corpo da cobra.
    """
    return [0,0]


def MoveCobra(c, T, S, H):
    return MOV_INVALIDO


def VerificaSuporte(T, S):
    return True


def QuedaCobra(T, S, H):
    return MOV_VALIDO


def Desfaz(T, S, H):
    return False
    

#A função main é fornecida pronta e não deve ser alterada:
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
        nivel = int(input("Escolha a fase [1-24]: "))
        nome_arquivo = "level%02d.txt"%nivel
        try:
            T,S = LeNivel(nome_arquivo)
            falha_leitura = False
        except:
            print("Fase não disponível")
            falha_leitura = True
    H = []
    continua = True
    ImprimeEstadoDoJogo(T, S)
    while continua: #laço principal
        print("Opções: e (esquerda), d (direita),")
        print("\tc (cima), b (baixo),")
        print("\tv (voltar/desfazer), s (sair).")
        c = input("Escolha um comando: ")
        if c == 's':
            continua = False
        elif c == 'v':
            r = Desfaz(T, S, H)
            if not r:
                print("Não há movimentos anteriores.")
            ImprimeEstadoDoJogo(T, S)
        else:
            r = MoveCobra(c, T, S, H)
            if r == MOV_INVALIDO:
                print("Movimento inválido")
            elif r == VITORIA:
                print("Vitória! Parabéns!")
                continua = False
            elif r == MORTE:
                print("GAME OVER")
                continua = False
            else:
                r = QuedaCobra(T, S, H)
                if r == MORTE:
                    print("GAME OVER")
                    continua = False
            ImprimeEstadoDoJogo(T, S)


#Não altere o código abaixo:
if __name__ == "__main__":
    main()

