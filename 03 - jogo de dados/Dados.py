import random

pScore = {}
players = []
up = 0
placar = []
q = 0
pnts = 0
def dado(lados = ""):
    if lados != "":
        l = int(lados) +1
        d = random.randrange(1,l)
    else:
        d = random.randrange(1,7)
    return d

def testaLetras(txt):
    letras = "avr"
    c = 0
    for l in txt:
        if l not in letras:
            c += 1
    if c > 0:
        return False
    else:
        return True



d1 = (dado())
d2 = (dado())
d3 = (dado())

def pontua():
    z = d1 * d2 * d3
    if d1 == d2 and d1 == d3:
        z *= 3
    elif d1 == d2 or d1 == d3 or d3 == d2:
        z *= 2
    return z

while True:
    try:
        q = int(input("Quantos jogadores? "))
        break
    except:
        print("Utilize apenas numeros inteiros.")

for i in range(q):
    nom = input("Nickname: ")
    players.append([nom, 3])
random.shuffle(players)

jogador = players[up][0]

def atualiza():
    print("\033[2;34m" + "=-"*40 + "=\033[m")
    print(f"{'\033[34mVez de: ' + '\033[4m' + jogador.upper() + '\033[m':>30}", end='' )
    print(f"{'\033[34m' + 'Score: ':>60}  {'\033[4m' + str(pnts) + '\033[m':>5}", end="\n\n\n")
    print(f"{' '*15}{'\033[41m[  ' + str(d1) + '  ]\033[m'}" 
          f"{' '*15}{'\033[44m[  ' + str(d2) + '  ]\033[m'}"
          f"{' '*15}{'\033[45m[  ' + str(d3) + '  ]\033[m'}"
            )
    print("\033[30m" + " "*18 + "v" + " "*21 + "a" + " "*21 + "r" + "\033[m\n")
    print(f"{'\033[30;2mRolar novamente:'+ str(players[up][1]) +'\033[m':^85}")
    print("\033[2;34m" + "=-"*40 + "=\033[m")


for n in range(q):
    up = n -1
    jogador = players[up][0]
    d1 = (dado())
    d2 = (dado())
    d3 = (dado())
    pnts = pontua()
    atualiza()

    while players[up][1] > 0:
        reroll = input("Gostaria de rerolar algum dado? \033[30;2m[S/N]\033[m").lower()
        if reroll == "s":
            dadoRe = input("Quais? \033[30;2m[V / A / R]\033[m").lower()
            if testaLetras(dadoRe) == False:
                print("V, A ou R")
                continue
            else:
                if "v" in dadoRe:
                    d1 = (dado())
                    players[up][1] -= 1
                if "a" in dadoRe:
                    d2 = (dado())
                    players[up][1] -= 1
                if "r" in dadoRe:
                    d3 = (dado())
                    players[up][1] -= 1
                pnts = pontua()
                atualiza()
                pScore.update({jogador:pnts})
                input()
                continue
        elif reroll == "n":
            pScore.update({jogador:pnts})
            break
        else: 
            print("S ou N")
            continue
        input()


# placar = list([pScore.items()])
# print(placar)
for i in pScore.items():
    if i[1] == max(pScore.values()):
        print("*"*50)
        txt = f"\033[42m{i[0]}: {str(i[1])}\033[m"
        print(f"{txt:^58}")
        
for i in pScore.items():
    if i[1] != max(pScore.values()):
        print(f"{i[0] + ': ' + str(i[1]):^50}")
for i in pScore.items():
    if i[1] == max(pScore.values()):
        vict = f"vitória de {i[0]}!!!"
        print()
        print(f"{vict.upper():^50}")
        print("*"*50)

    