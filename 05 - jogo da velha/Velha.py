import pygame,sys,math
pygame.init()  # iniciando o pygamae

HEIGHT, WIDTH = 630, 630
BG = pygame.image.load("bgJogoDaVelha.png") # importando imagem
BG = pygame.transform.scale(BG,(HEIGHT,WIDTH)) # arrumando a escala da imagem para encaixar na janela

# ----- CORES ----------------
vermelho = 235,72,69
verde = 161,211,114
azul = 126,167,216
bege = 255,247,154
cinza = 170,179,171

# ----- VARIÁVEIS ------------
board = [["v", "v", "v"],
         ["v", "v", "v"],
         ["v", "v", "v"]]
mouse_posX = 0
mouse_posY = 0
click_posX = -1
click_posY = -1
click_mem = False
click_switch = False
ver_turn = False
turn = "o"
the_end = False

# ----- FUNÇÕES --------------
def clicando(mouse_posX, mouse_posY, click_switch, click_posX,click_posY):
    if click == False and click_mem == True:
        click_switch = True
        x = math.ceil(mouse_posX/210) -1
        y = math.ceil(mouse_posY/210) -1
        click_posX = x
        click_posY = y
        print(f"clicou x,y: ({click_posX},{click_posY}) + clcsw = {click_switch}")
    elif click == False and click_mem == False:
        click_switch = False
        click_posX = -1
        click_posY = -1
    return click_switch, click_posX, click_posY

def xo(win,turn,click_posX,click_posY):
    xOUo = "o" if turn == "o" else "x"
    corXO = verde if xOUo == "o" else vermelho
    txtXO = fonte.render(xOUo, True, corXO)
    marca_posX = (click_posX * 210) + 45
    marca_posY = (click_posY * 210) - 40

    win.blit(txtXO,(marca_posX, marca_posY))

def marcador(click_posX, click_posY, board, turn, ver_turn, click_switch, the_end):
    if click_switch == True and board[click_posY][click_posX] == "v" and the_end == False:
        if turn == "o":
            board[click_posY][click_posX] = "o"
            ver_turn = not ver_turn
            xo(win,turn,click_posX,click_posY)
        if turn == "x":
            board[click_posY][click_posX] = "x"
            ver_turn = not ver_turn
            xo(win,turn,click_posX,click_posY)
    return board, ver_turn

def finish(board,the_end,win,):
    coluna0 = [board[0][0], board[1][0], board[2][0]] 
    coluna1 = [board[0][1], board[1][1], board[2][1]] 
    coluna2 = [board[0][2], board[1][2], board[2][2]] 
    diag0 = [board[0][0], board[1][1], board[2][2]] 
    diag1 = [board[2][0], board[1][1], board[0][2]] 

    if all(l == "x" for l in board[0]) or all(l == "o" for l in board[0]):
        pygame.draw.line(win, azul,(20,110),(610,110),20)
        the_end = True
    if all(l == "x" for l in board[1]) or all(l == "o" for l in board[1]):
        pygame.draw.line(win, azul,(20,320),(610,320),20)
        the_end = True
    if all(l == "x" for l in board[2]) or all(l == "o" for l in board[2]):
        pygame.draw.line(win, azul,(20,530),(610,530),20)
        the_end = True

    if all(l == "x" for l in coluna0) or all(l == "o" for l in coluna0):
        pygame.draw.line(win, azul,(105,20),(105,610),20)
        the_end = True
    if all(l == "x" for l in coluna1) or all(l == "o" for l in coluna1):
        pygame.draw.line(win, azul,(315,20),(315,610),20)
        the_end = True
    if all(l == "x" for l in coluna2) or all(l == "o" for l in coluna2):
        pygame.draw.line(win, azul,(520,20),(520,610),20)
        the_end = True

    if all(l == "x" for l in diag0) or all(l == "o" for l in diag0):
        pygame.draw.line(win, azul,(50,50),(580,580),20)
        the_end = True
    if all(l == "x" for l in diag1) or all(l == "o" for l in diag1):
        pygame.draw.line(win, azul,(50,580),(580,50),20)
        the_end = True

    if any(l == "v" for l in board[0]) == False and \
       any(l == "v" for l in board[1]) == False and \
       any(l == "v" for l in board[2]) == False:
            pygame.draw.line(win, azul,(50,50),(580,580),20)
            pygame.draw.line(win, azul,(50,580),(580,50),20)
            the_end = True

    
    return the_end


win = pygame.display.set_mode((HEIGHT,WIDTH)) # iniciando a janela
pygame.display.set_caption("Jogo da Velha 1") # dando um titulo pra janela
win.fill(bege) # define a cor de fundo da janela
pygame.font.init() # iniciando a fonte dentro do jogo
fonte = pygame.font.SysFont("Verdana", 200)
clock = pygame.time.Clock() ### ???? ###

while True:
    for event in pygame.event.get(): # verifica se ocorreu algum evento
        if event.type == pygame.QUIT: # no caso o evento vai ser apertar o X pra fechar
            pygame.quit() # encerra o ccódigo
            sys.exit() # fecha a janela

    turn = "x" if ver_turn == True else "o"
    mouse_pos = pygame.mouse.get_pos() # verifica a posição do mouse (x,y) na janela
    mouse_posX = mouse_pos[0]
    mouse_posY = mouse_pos[1]
    click = pygame.mouse.get_pressed()[0] # verifica se algum botão do mouse foi clicado (esq, roll, dir)
    click_switch, click_posX, click_posY = clicando(mouse_posX,mouse_posY,click_switch,click_posX,click_posY)
    board, ver_turn = marcador(click_posX,click_posY,board,turn,ver_turn,click_switch,the_end)
    the_end = finish(board, the_end, win)

    if click == True:
        click_mem = True
    else:
        click_mem = False

    win.blit(BG,(-1,0)) # colocando a imagem na janela (na posição -1,0)
    pygame.display.update() # mantém a janela atualizando contantemente
    clock.tick(30) # define o frame rate (um sleep a cada atualização no jogo)