import colorama
import time
import os

colorama.init(autoreset=True)

cadastros = {}
temp = []
sim = f"{colorama.Fore.GREEN}S{colorama.Fore.RESET}"
não = f"{colorama.Fore.RED}N{colorama.Fore.RESET}"
sn = f"{colorama.Style.DIM}[{sim}/{não}]{colorama.Style.RESET_ALL}"

def cadastrador(nome, senha, saldo): 
    cadastros.update({nome:[senha,saldo]})
    temp.clear()
def upload(): 
    txtsave = ""   
    for i in cadastros:
        txtsave += f"{i},{cadastros.get(i)[0]},{cadastros.get(i)[1]}\n"
    with open("cadastros.txt","w") as salva:
        salva.write(txtsave)
def erro(txt):
    print(colorama.Fore.RED + "[Erro: " + txt + "]")
    time.sleep(1.3)  
def loading():
    print(colorama.Style.BRIGHT + ".", end="")
    time.sleep(0.1)
    print(colorama.Style.BRIGHT + ".", end="")
    time.sleep(0.2)
    print(colorama.Style.BRIGHT +  ".", end="")
    time.sleep(0.4)
    print(colorama.Style.BRIGHT + ".", end="")
    time.sleep(0.2)
    print(colorama.Style.BRIGHT + "." + colorama.Style.RESET_ALL, end="\n")
    time.sleep(0.1)
def att_saldo():
    cadastros.pop(temp[0])
    cadastros.update({temp[0]:[temp[1],temp[2]]})
def limpa():
    os.system("cls")
def tela_logado():
    print("="*60)
    print(f"\n{temp[0]:^60}")
    print(f"{'Saldo: R$' + temp[2]:^60}\n")
    print("="*60)
def tela_cadastro():
    if len(temp) == 0:
        print("="*60)
        print(f"\n{'CADASTRO':^60}")
        print(f"Nome  : ")
        print(f"Senha : ")
        print(f"Saldo : ")
        print("\n" + "="*60)    
    if len(temp) == 1:
        print("="*60)
        print(f"\n{'CADASTRO':^60}")
        print(f"Nome  : {temp[0]}")
        print(f"Senha : ")
        print(f"Saldo : ")
        print("\n" + "="*60)
    if len(temp) == 2:
        print("="*60)
        print(f"\n{'CADASTRO':^60}")
        print(f"Nome  : {temp[0]}")
        print(f"Senha : {temp[1]}")
        print(f"Saldo : ")
        print("\n" + "="*60)
    if len(temp) == 3:
        print("="*60)
        print(f"\n{'CADASTRO':^60}")
        print(f"Nome  : {temp[0]}")
        print(f"Senha : {temp[1]}")
        print(f"Saldo : {temp[2]}")
        print("\n" + "="*60)

with open("cadastros.txt","r+") as leitor: # Download (leitor do banco de dados)
    for l in leitor.readlines():
        corte = l.split(",")
        nom = corte[0]
        sen = corte[1]
        sal = corte[2]

        if sal.find("\n") > -1:
            sal = sal[:sal.find("\n")]

        cadastros.update({nom:[sen,sal]})

limpa()
print("="*60)
print(f"\n{'BANCO PTS':^60}\n")
print(f"{'seja bem vindo!':^60}")
print("="*60)

while True:  # Tem cadastro?
    verifica_cad = input(f"Você já tem cadastro? {sn}").lower()
    if verifica_cad == "s":
        break
    elif verifica_cad == "n":
        break
    else:
        erro("Responda apenas com 'S' ou 'N'.")
        continue

if verifica_cad == "s": # Cadastrados
    while True: # Login
        log_nome = input("Nome: ").title()
        if log_nome in cadastros.keys():
            log_senha = input("Senha: ")
            if log_senha == cadastros[log_nome][0]:
                temp = [log_nome, cadastros[log_nome][0], cadastros[log_nome][1]]
                loading()
                print(colorama.Fore.GREEN + colorama.Style.DIM + "LOGADO" + colorama.Style.RESET_ALL)
                time.sleep(1)
                limpa()
                break
            else:
                erro("Senha incorreta.")
                continue
        else:
            erro("Nome não cadastrado.")
            continue

    if log_senha == cadastros[log_nome][0]:  # Logado
        tela_logado()

        while True: # Qual operação?
            print("Qual operação você quer realizar?") 
            print(colorama.Style.BRIGHT + 'Saque  ' + colorama.Style.DIM + '[ S ]'
                  + colorama.Style.RESET_ALL + ' '*10 
                  + colorama.Style.BRIGHT + 'Depósito  ' + colorama.Style.DIM + '[ D ]'
                  + colorama.Style.RESET_ALL)
            saq_dep = input()
            if saq_dep == "s": # Saque
                while True:
                    val_saq = input("Quanto você quer sacar? ")
                    try: 
                        vs = int(val_saq)             
                        loading()
                        if vs <= int(temp[2]):
                            temp[2] = str(int(temp[2]) - vs)  

                            if (((vs % 50) % 20) % 5) % 2 !=  0:
                                vs -= (((vs % 50) % 20) % 5) % 2
                                temp[2] = str(int(temp[2]) - vs)
                                erro(f"Será sacado R$ {vs} por conta das notas disponíveis")
                                time.sleep(0.2)
                                
                            limpa()
                            tela_logado()

                            if vs // 50 > 0:
                                print(f"Notas de R$50,00: {vs // 50}")
                                time.sleep(0.2)
                            if (vs % 50) // 20 > 0 :
                                print(f"Notas de R$20,00: {(vs % 50) // 20}")
                                time.sleep(0.2)
                            if ((vs % 50) % 20) // 5 > 0:
                                print(f"Notas de R$ 5,00: {((vs % 50) % 20) // 5}")
                                time.sleep(0.2)
                            if (((vs % 50) % 20) % 5) // 2 > 0:
                                print(f"Notas de R$ 2,00: {(((vs % 50) % 20) % 5) // 2 }")
                                time.sleep(0.2)
                            att_saldo()
                            print("Saque concluído.")
                            break
                        else:
                            erro("Saldo insuficiente.")
                            continue
                    except:
                        erro("Utilize apenas números.")
                        continue

            elif saq_dep == "d": # Deposito
                 while True:
                    val_dep = input("Quanto você quer depositar? ")
                    try: 
                        vd = int(val_dep)
                        temp[2] = str(int(temp[2]) + vd)
                        att_saldo()
                        loading()
                        limpa()
                        tela_logado()
                        print("Depositado com sucesso!")
                        break
                    except:
                        erro("Utilize apenas números.")
                        continue
            else:
                erro("S ou D")
            break

else: # Quer se cadastrar?
    while True:
        quer_cad = input(f"Gostaria de se cadastrar? {sn}").lower()
        if quer_cad == "s":
            break
        elif quer_cad == "n":
            break
        else:
            erro("Responda apenas com 'S' ou 'N'.") 
            continue

    if quer_cad == "s": # Cadastrando
        limpa()
        tela_cadastro()
        while True: # Qual é o seu nome? cadastro
            cad_nome = input("Qual é o neu nome? ").title()
            if cad_nome in cadastros.keys():
                erro("Nome já cadastrado.")
                continue
            else:
                temp.append(cad_nome)
                loading()
                limpa()
                tela_cadastro()
                break

        while True: # Qual é a senha? cadastro
            cad_senha = input("Escolha uma senha: " + colorama.Style.DIM + "[5 dígitos]" + colorama.Style.RESET_ALL)
            if len(cad_senha) != 5:
                erro("[5 dígitos]")
                continue
            else:
                temp.append(cad_senha)
                loading()
                limpa()
                tela_cadastro()
                break

        if len(cad_senha) == 5: # Quanto vai depositar? cadastro
            while True: 
                cad_saldo = input("Quanto quer depositar? ")
                if cad_saldo.isnumeric() == False:
                    erro("Utilize apenas números.")
                    continue
                else:
                    temp.append(cad_saldo)
                    loading()
                    limpa()
                    tela_cadastro()
                    cadastrador(temp[0],temp[1],temp[2])
                    upload()
                    print("Cadastro concluído.")
                    break

    elif quer_cad == "n":
        print("Volte sempre!")

upload()