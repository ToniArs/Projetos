MOV_INVALIDO = 0
MOV_VALIDO   = 1
VITORIA      = 2
MORTE        = 3


def LeNivel(nome_arquivo):
    return [],[]


def ImprimeEstadoDoJogo(T, S):
    print()


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

