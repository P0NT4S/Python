import tkinter as tk
import sqlite3 as sql
from sqlite3 import Error
import ttkbootstrap as ttkb
from PIL import Image
Image.CUBIC = Image.BICUBIC #it's necessary because meter widget from ttkbootstrap is a piece of shit

class User:
    def __init__(self):
        self.login = None
        self.nome = None
        self.saldo = None

        self.con = sql.connect("BancoPTS_DB.db")
        self.cur = self.con.cursor()
        self.tb = "user_data"
        try:
            self.cur.execute(f"CREATE TABLE {self.tb}(login PRIMARY KEY, senha, nome, valor)")
        except: 
            print("tabela já existente")

    def login_user(self, login, senha):
        try:
            lista_tb = self.cur.execute(f"SELECT nome, valor, login, senha FROM {self.tb} WHERE login='{login}'")
            useruario = lista_tb.fetchone()
            if useruario[3] == senha:
                self.nome = useruario[0]
                self.saldo = useruario[1]
                self.login = useruario[2]
                print(self.nome, self.saldo, self.login)
                return True
            else:
                inicio.erro("Senha incorreta.")
                return False
        except:
            inicio.erro("Login inexistente.")
            return False

    def cad_user(self, nome, login, senha, valor):
        try:
            self.cur.execute(f"""INSERT INTO {self.tb}(login, senha, nome, valor) VALUES('{login}', '{senha}', '{nome}', {valor})""")
            self.con.commit()
            cadastro.erro("Cadastro concluído.", cor = "success")
        except Error as ex:
            cadastro.erro("Login indisponível.")
            print(ex)
            
    def saldo_update(self, valor):
        user_saldo = self.cur.execute(f"SELECT valor FROM {self.tb} WHERE login='{self.login}'")
        saldo = user_saldo.fetchone()
        new_saldo = saldo[0] + int(valor)
        att = self.cur.execute(f"UPDATE {self.tb} SET valor={int(new_saldo)} WHERE login='{self.login}'")
        new_saldo_select = self.cur.execute(f"SELECT valor FROM {self.tb} WHERE login='{self.login}'")
        new_saldo_att = new_saldo_select.fetchone()
        self.con.commit()
        self.saldo = new_saldo_att[0]

class Janela:
    _len_x, _len_y = 450,500

    def __init__(self, tema):
        self.tema = tema
        self.titulo = "Titulo"
        self.aba_aberta = None

        win = ttkb.Window(themename= self.tema)
        self.win = win

        centro = win.winfo_screenmmwidth()//2
        win.geometry(f"{Janela._len_x}x{Janela._len_y}+{str((Janela._len_x // 2) + centro)}+50")
        win.title(self.titulo)

        def ver_num(txt):
                if txt.isdigit() or txt == "":
                    return True
                else:
                    return False
                
        validate_num = (self.win.register(ver_num))
        self.validate_num = validate_num

    def abre(self, aba):
        if self.aba_aberta != None:
            for i in self.aba_aberta.widgets.keys():
                i.destroy()

        aba.gera_aba()

        self.aba_aberta = aba
        wgts = aba.widgets
        for i in wgts.keys():
            i.place(relx = wgts.get(i)[0], rely = wgts.get(i)[1], anchor = wgts.get(i)[2])

class Abas:
    def __init__(self, titulo):
        main.titulo = titulo
        self.widgets = {}

    def addWidget(self, wgt, relx, rely, anchor):
        new_widget = {wgt:[relx, rely, anchor]}
        self.widgets.update(new_widget)

    def frame_func(self, volta=True):
        self.widgets.clear()
        self.frame = ttkb.Frame(main.win, width = main._len_x, height = main._len_y)
        self.addWidget(self.frame, 0.5, 0.5, "center")

        if volta:
            go_back = tk.Label(self.frame, text="<", font="Helvetica 25 bold")
            go_back.place(x=15, y=15)
            go_back.bind("<Enter>", lambda e:go_back.config(fg="gray"))
            go_back.bind("<Leave>", lambda e:go_back.config(fg="white"))
            go_back.bind("<Button>", lambda e:main.abre(inicio))

    def erro(self, txt, cor = "warning"):
        msg_erro = ttkb.Label(self.frame,
                                text=txt,
                                font="verdana 10",
                                style=cor,
                                anchor="center")
        msg_erro.place(relx=0.5, rely=0.93, anchor="center",width=350)
        self.frame.after(3000, msg_erro.destroy)

class Inicio(Abas):
    def __init__(self, titulo):
        super().__init__(titulo)

    def logar(self, login, senha):
        if login != "" and senha != "":
            if usuario.login_user(login, senha):
                main.abre(logado)
        else:
            self.erro("Preencha todos os campos")

    def gera_aba(self):
        self.frame_func(volta = False)

        bem_vindo = tk.Label(self.frame,
                     text="Bem vindo ao",
                     font="verdana 15")
        banco_pts_ini = tk.Label(self.frame,
                            text="BANCO PTS",
                            font="verdana 25 bold")

        login_txt = tk.Label(self.frame, 
                            text="Login: ", 
                            font="verdana 10")
        self.login = ttkb.Entry(self.frame, 
                           style="secondary")
        self.login.bind("<Return>", lambda e:self.senha.focus())

        senha_txt = tk.Label(self.frame, 
                            text="Senha: ", 
                            font="verdana 10")
        self.senha = ttkb.Entry(self.frame, 
                           style="secondary", 
                           show="*")
        self.senha.bind("<Return>", lambda e:self.logar(self.login.get(), self.senha.get()))
        
        entra_bt = ttkb.Button(self.frame, 
                               text="entrar", 
                               style="success-outline",
                               width=20,
                               command=lambda: self.logar(self.login.get(), self.senha.get()))

        cad_link = ttkb.Button(self.frame,
                                text="Quer se cadastrar?",
                                style="primary-link",
                                command=lambda: main.abre(cadastro))

        
        self.addWidget(bem_vindo, 0.5, 0.2, "center")
        self.addWidget(banco_pts_ini, 0.5, 0.3, "center")
        self.addWidget(login_txt, 0.4, 0.505, "e")
        self.addWidget(self.login, 0.4, 0.5, "w")
        self.addWidget(senha_txt, 0.4, 0.605, "e")
        self.addWidget(self.senha, 0.4, 0.6, "w")
        self.addWidget(entra_bt, 0.5, 0.7, "center")
        self.addWidget(cad_link, 0.5, 0.8, "center")

class Cadastro(Abas):
    def __init__(self, titulo):
        super().__init__(titulo)
        self.user_data = {"login": "", "senha": "", "nome": "", "valor": ""}

        self.aba_ant = inicio
        self.progresso = 0
        self.done_entrys = []

    def gera_aba(self):
        self.__init__("PTS Cadastro")
        self.frame_func()
        my_style = ttkb.Style()
        my_style.configure("light.TLabelframe.Label", font=("Verdana", 15))

        banco_pts_cad = tk.Label(self.frame,
                                text="BANCO PTS",
                                font="verdana 25 bold")

        cad_frame = ttkb.Labelframe(self.frame, 
                                    text="  cadastro  ", 
                                    width=300, height=300, 
                                    style="light")

        nome_txt = tk.Label(cad_frame, 
                            text="Nome:", 
                            font="verdana 10")
        self.nome = ttkb.Entry(cad_frame,
                               style="secondary")

        self.nome.bind("<Return>",lambda e:self.ver_entradas("nome", "return"))
        self.nome.bind("<FocusOut>",lambda e:self.ver_entradas("nome", "focus"))

        login_txt = tk.Label(cad_frame, 
                             text="Login:", 
                             font="verdana 10")
        self.login = ttkb.Entry(cad_frame, 
                           style="secondary")

        self.login.bind("<Return>",lambda e:self.ver_entradas("login", "return"))
        self.login.bind("<FocusOut>",lambda e:self.ver_entradas("login", "focus"))

        senha_txt = tk.Label(cad_frame, 
                             text="Senha:", 
                             font="verdana 10")
        self.senha = ttkb.Entry(cad_frame, 
                                style="secondary")

        self.senha.bind("<Return>",lambda e:self.ver_entradas("senha", "return"))
        self.senha.bind("<FocusOut>",lambda e:self.ver_entradas("senha", "focus"))

        valor_txt = tk.Label(cad_frame, 
                             text="Valor inicial:", 
                             font="verdana 10")
        self.valor = ttkb.Entry(cad_frame,
                                validate="key",
                                validatecommand=(main.validate_num, "%P"), 
                                style="secondary")

        self.valor.bind("<Return>",lambda e:self.ver_entradas("valor", "return"))
        self.valor.bind("<FocusOut>",lambda e:self.ver_entradas("valor", "focus"))

        self.loading = ttkb.Progressbar(cad_frame,
                                   style="success striped",
                                   maximum=100,
                                   length=200,
                                   value=0)

        self.cad_bt = ttkb.Button(cad_frame, 
                                  text="confirmar", 
                                  style="success-outline",
                                  state="disabled",
                                  command=lambda: usuario.cad_user(self.user_data["nome"].title(),
                                                                   self.user_data["login"],
                                                                   self.user_data["senha"],
                                                                   self.user_data["valor"]))

        self.addWidget(banco_pts_cad, 0.5, 0.1, "center")
        self.addWidget(cad_frame, 0.5, 0.5, "center")
        self.addWidget(nome_txt, 0.4, 0.11, "e")
        self.addWidget(self.nome, 0.4, 0.1, "w")
        self.addWidget(login_txt, 0.4, 0.26, "e")
        self.addWidget(self.login, 0.4, 0.25, "w")
        self.addWidget(senha_txt, 0.4, 0.41, "e")
        self.addWidget(self.senha, 0.4, 0.4, "w")
        self.addWidget(valor_txt, 0.4, 0.56, "e")
        self.addWidget(self.valor, 0.4, 0.55, "w")
        self.addWidget(self.loading, 0.5, 0.75, "center")
        self.addWidget(self.cad_bt, 0.5, 0.88, "center")

    # def cadastar(self):  # terminar a função do butão de cadastro
    #     usuario.cad_user(self.user_data["nome"].title(),
    #                     self.user_data["login"],
    #                     self.user_data["senha"],
    #                     self.user_data["valor"])

    def att_progress(self, goback=False):
        def start(pra_tras):
            for i in range(25):
                 self.loading.after(20, self.loading.step(1 if not pra_tras else -1))
                 self.loading.update()
        def att():
            self.loading["value"] = self.progresso
        def bt_unlock():
            if self.loading["value"] == 100:
                self.cad_bt.config(state="normal")
        def bt_lock():
            if self.progresso < 100:
                self.cad_bt.config(state="disabled")

        if not goback:
            start(goback)    
            self.progresso += 25
        if goback and self.progresso >= 25:
            self.progresso -= 25
            bt_lock()
            start(goback)    

        self.frame.after(1500, self.loading.stop)
        self.frame.after(1500, att)
        self.frame.after(2000, bt_unlock)
        
    def ver_entradas(self, entrada, event):
        def nexter(entrada_ = entrada, event_ = event, volta=False):
            objetos = [self.nome, self.login, self.senha, self.valor]
            foco    = [ "nome"  , "login"   , "senha"   ,  "valor"  ]
            foco_id = foco.index(entrada_)
            focado = objetos[foco_id]

            if volta:
                focado.config(bootstyle="danger")
                if entrada in self.done_entrys:
                        self.done_entrys.remove(entrada)
                        self.user_data[entrada] = ""
                        self.att_progress(volta)

            if event_ == "return" and volta == False:    
                prox_foco = objetos[foco_id+1] if foco_id < len(foco)-1 else objetos[0]
                prox_foco.focus()

            if entrada not in self.done_entrys and volta == False:
                    focado.config(bootstyle="success")
                    self.done_entrys.append(entrada)
                    self.user_data[entrada] = focado.get()
                    self.att_progress()

        if entrada == "nome":
            if len(self.nome.get()) > 2:
                nexter()
            else:
                nexter(volta=True)
                self.erro("Digite seu nome.")

        if entrada == "login":
            if self.login.get() != "":
                nexter()
            else:
                nexter(volta=True)
                self.erro("Esse login não está disponível.")

        if entrada == "senha":
            if len(self.senha.get()) >= 5:
                nexter()
            else:
                nexter(volta=True)
                self.erro("Sua senha deve conter pelo menos 5 caracteres.")
            
        if entrada == "valor":
            if self.valor.get() != "":
                nexter()
            else:
                nexter(volta=True)
                self.erro("Deposite um valor inicial.")

class Logado(Abas):
    def __init__(self, titulo):
        super().__init__(titulo)

    def operação(self, valor):
        if valor != "0" and valor != "":
            usuario.saldo_update(valor)
            self.saldo_txt.config(text = f"R$ {usuario.saldo}")
            try:
                self.valor.delete(0,"end")
            except:
                self.valor_var= tk.StringVar(value=int(usuario.saldo*0.3))
                self.int_valor_var = int(self.valor_var.get())
                self.valor_meter["amounttotal"] = usuario.saldo
                self.valor_meter["amountused"] = self.int_valor_var
        else:
            logado.erro("Valor mínimo: R$1,00")

    def bt_fecha_frame(self,frame):
        def fecha_frame(frame):
            frame.destroy()
            self.saq_dep_bts()
            self.saldo_frame.place_configure(height=100, rely=0.35)

        bt_fecha = tk.Label(frame, text="x", font="Helvetica 20 bold")
        bt_fecha.place(x=350, y=2)
        bt_fecha.bind("<Enter>", lambda e:bt_fecha.config(fg="gray"))
        bt_fecha.bind("<Leave>", lambda e:bt_fecha.config(fg="white"))
        bt_fecha.bind("<Button>", lambda e:fecha_frame(frame))

    def dep_frame(self):
        self.deposito_bt.destroy()
        self.saque_bt.destroy()

        frame = ttkb.LabelFrame(self.frame,
                                text="",
                                width=380,
                                height=150)
        
        valor_txt = tk.Label(frame,
                             text="Quanto você quer depositar?",
                             font="verdana 11")
        
        self.valor = ttkb.Entry(frame,
                           style="secondary",
                           validate="key",
                           validatecommand=(main.validate_num, "%P"),
                           font="verdana 10",
                           justify="center")
        
        depositar_bt = ttkb.Button(frame,
                                   text="DEPOSITAR",
                                   style="outline",
                                   width=11,
                                   command= lambda: self.operação(self.valor.get()))
        
        self.bt_fecha_frame(frame)
        frame.place(relx=0.5, rely=0.7, anchor="center")
        valor_txt.place(relx=0.5, rely=0.15, anchor="center")
        self.valor.place(relx=0.5, rely=0.4, anchor="center")
        depositar_bt.place(relx=0.5, rely=0.7, anchor="center")

    def saq_frame(self):
        self.deposito_bt.destroy()
        self.saque_bt.destroy()
        self.saldo_frame.place_configure(height=75, rely=0.25)
    
        frame = ttkb.LabelFrame(self.frame,
                                width=380,
                                height=300)
        
        valor_txt = tk.Label(frame,
                             text="Quanto você quer sacar?",
                             font="verdana 10")
        
        self.valor_var= tk.StringVar(value=int(usuario.saldo*0.3))
        self.int_valor_var = int(self.valor_var.get())

        def meter_int(*args):
            int_value = self.valor_meter["amountused"]
            self.valor_meter["amountused"] = int(int_value)
            self.valor_var.set(int_value)
            self.valor_meter["subtext"] = f"{(self.valor_meter["amountused"]/self.valor_meter["amounttotal"]*100):.1f}%"

            if self.valor_meter["amountused"] <= usuario.saldo*0.5:
                self.valor_meter["bootstyle"] = "default"
            if self.valor_meter["amountused"] > usuario.saldo*0.5:
                self.valor_meter["bootstyle"] = "info"
            if self.valor_meter["amountused"] > usuario.saldo*0.7:
                self.valor_meter["bootstyle"] = "warning"
            if self.valor_meter["amountused"] > usuario.saldo*0.99:
                self.valor_meter["bootstyle"] = "danger"
        
        def entry_logic(valor_max):
                not_null = False 
                if self.valor_var.get() == "":
                    self.valor_meter.amountusedvar.set(0)
                else:
                    int_valor_var = int(self.valor_var.get())
                    not_null = True

                if not_null:
                    if int_valor_var <= usuario.saldo:
                        self.valor_meter.amountusedvar.set(int_valor_var)
                    else:
                        self.valor_meter.amountusedvar.set(usuario.saldo)

        self.valor_meter = ttkb.Meter(frame,
                           metersize=180,
                           interactive=True,
                           metertype="semi",
                           amounttotal=usuario.saldo,
                           amountused=self.int_valor_var,
                           meterthickness=15,
                           textleft="R$",
                           textright=",00",
                           subtext=f"{self.int_valor_var/usuario.saldo*100:.1f}%",
                           textfont="-size 20 -weight bold")
        self.valor_meter.amountusedvar.trace("w",meter_int)
        
        self.valor_entry = ttkb.Entry(frame,
                                 textvariable=self.valor_var,
                                 validate="key",
                                 validatecommand=(main.validate_num, "%P"),
                                 font="verdana 11",
                                 justify="center",
                                 width=11,
                                 style="secondary")
        self.valor_entry.bind("<Any-KeyRelease>",lambda e:entry_logic(usuario.saldo))

        depositar_bt = ttkb.Button(frame,
                                   text="SACAR",
                                   style="outline",
                                   width=10,
                                   command= lambda: self.operação(self.int_valor_var*-1))
        
        self.bt_fecha_frame(frame)
        frame.place(relx=0.5, rely=0.65, anchor="center")
        valor_txt.place(relx=0.5, rely=0.1, anchor="center")
        self.valor_meter.place(relx=0.3, rely=0.57, anchor="center")
        self.valor_entry.place(relx=0.75, rely=0.4, anchor="center")
        depositar_bt.place(relx=0.75, rely=0.65, anchor="center")
        
    def saq_dep_bts(self):
        my_style = ttkb.Style()
        my_style.configure("TButton", font=("Verdana", 10))
        self.saque_bt = ttkb.Button(self.frame,
                                    text="SACAR",
                                    style="outline",
                                    width=11,
                                    command=lambda: self.saq_frame())
        
        self.deposito_bt = ttkb.Button(self.frame,
                                       text="DEPOSITAR",
                                       style="outline",
                                       width=11,
                                       command=lambda: self.dep_frame())
        
        self.deposito_bt.place(relx=0.35, rely=0.6, anchor="center")
        self.saque_bt.place(relx=0.65, rely=0.6, anchor="center")

    def gera_aba(self):
        self.frame_func()

        my_style = ttkb.Style()
        my_style.configure("TLabelframe.Label", font=("Verdana 10 bold"))

        self.banco_pts_cad = tk.Label(self.frame,
                                text="BANCO PTS",
                                font="verdana 25 bold")
        
        self.saldo_frame = ttkb.Labelframe(self.frame, 
                                           text="  SALDO  ", 
                                           width=380,
                                           height=100,
                                           relief="solid",
                                           style = "success")
        
        self.saldo_txt = ttkb.Label(self.saldo_frame,
                                    text=f"R$ {usuario.saldo}",
                                    font="verdana 15")
        
        self.saq_dep_bts()
        
        self.addWidget(self.banco_pts_cad, 0.5, 0.1, "center")
        self.addWidget(self.saldo_frame, 0.5, 0.35, "center")
        self.addWidget(self.saldo_txt, 0.5, 0.4, "center")

main = Janela("superhero")
inicio = Inicio("Banco PTS")
cadastro = Cadastro("PTS Cadastro")
logado = Logado("PTS usuário")
usuario = User()

main.abre(inicio)

main.win.mainloop()