#------- Bancos de dados ---------------------------------------
data_Bank =  open("cadastro.txt", "r+")
leitor = data_Bank.readlines()
dtB_temp = {}

#------- MSG's -------------------------------------------------
tchau = "Obrigado.\nVolte sempre!"
erro_dig = "Digite \"s\" para sim ou \"n\" para não."
erro_num = "Utilize apenas números e \".\" para separar os centavos."
#------- Verificações ------------------------------------------
ver_cad = " "
ver_mont = False
ação = " "
valor = ""
#------- Variaveis ----------------------------------------------
nome = " "
saldo = " "

#------- Funções-------------------------------------------------
def reader_dtB(lista):
    dtB_temp.clear()

    for l in lista:
        cut = l.split(",")
        n = cut[0]
        v = cut[1]

        if v.find("\n") > -1:
            v = v[:v.find("\n")]
        
        dtB_temp.update({n:v})
       
def ver_numerico(inp):
     
    entrada = inp
    num = "0123456789."
    x = True

    for i in entrada:
        if i in num:
            continue
        else:
            x = False
        break               
    
    if x == True:
        return True
    else:
        print(erro_num)
        return False

print(f"{"=" * 50}\n\n{"\033[4mBANCO PTS\033[m":^54}\n\n{"=" * 50}")

reader_dtB(leitor)

#------- Inicio --------------------------------------------------
while True:
    ver_cad = input("Já possi cadastro no nosso banco? [S/N] ").lower()

    if ver_cad == "s" or ver_cad == "n":
        break
    else:
        print(erro_dig)

if ver_cad == "n": #------- Cadastro ------------------------------------
    while True:   
            cad_ = input("Deseja se cadastrar? [S/N] ")

            if cad_ == "s":
                nome = input("Qual é o seu nome? ").strip().title()
                if nome in dtB_temp:
                    print("Nome já cadastrado.")
                    break

                print(f"Olá, {nome}. Obrigado por se cadastar.")
                while ver_mont == False:
                    saldo = input("Quanto você gostaria de depositar inicialmente? R$ ").strip()
                    ver_mont = ver_numerico(saldo)

                data_Bank.write(f"{nome},{saldo}\n")

                print("Cadastro concluído. "+tchau)
                break

            elif cad_ == "n":
                print(tchau)
                break

            else:
                print(erro_dig)

else: 
    while True:
        nome = input("Digite seu nome. ").title().strip()
        if nome in dtB_temp:
            break
        else:
            print("Nome não registrado.")

if nome in dtB_temp:
    while True:
        ação = input(f"Olá, {nome}. Você gostarias de realizar um saque ou um deposito? [S/D] ").lower()
        if ação == "s" or ação == "d":
            break
        else:
            print("Use S para saque e D para deposito.")

if ação == "s":
    while ver_mont == False:
        valor = (input("Quanto você quer sacar? R$ ").strip())
        ver_mont = ver_numerico(valor)

    valor = int(valor)
    saldo_ = int(dtB_temp[nome])
    print(f"Notas de R$50,00: {valor // 50}")
    print(f"Notas de R$20,00: {(valor % 50) // 20}")
    print(f"Notas de R$05,00: {((valor % 50) % 20) // 5}")
    print(f"Total  : R${valor},00")
    print(f"Saldo  : R${saldo_ - valor},00")
data_Bank.close()