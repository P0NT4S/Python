from tkinter import *
from PIL import ImageTk, Image
import time
import sqlite3 as sql
import random

DB = sql.connect("palavras.db") # conecta com o banco de dados
cursor = DB.cursor() # criando um cursor pra operar o db

BG_COLOR     = "#494b55"
BG_TXTCOLOR  = "#6f7280"
BG_BTCOLOR   = "#2f3347"
RED          = "#f84048"
GREEN        = "#44e471"

palavra = ""
dick = ""
ja_foi = []
lifes = 6
msg = ""

class Vidas(Label):
    def __init__ (self,*args,**kwargs):
        Label.__init__(self, *args, **kwargs)
        self["bg"] = BG_COLOR
        self["fg"] = GREEN
        self["font"] = "TkMenuFont 25 bold"
        self["pady"] = 0

def escolhe_palavra():
    cursor.execute("SELECT * FROM tb_palavras") # selecionando tds os itens da lista 
    res = cursor.execute("SELECT palavra, dica FROM tb_palavras ORDER by RANDOM()")
    palavra0, dick0 = res.fetchone()
    return palavra0, dick0

def traçado(pal):
    traçados = []
    for l in pal:
        traçados.append("_")
    return traçados

def dano():
    if lifes == 5:
        v6.destroy()
    elif lifes == 4:   
        v5.destroy()
    elif lifes == 3:  
        v4.destroy()
    elif lifes == 2:   
        v3.destroy()
    elif lifes == 1:  
        v2.destroy()        
    elif lifes == 0:  
        v1.destroy()        

def letrando(event=None):
    global lifes
    global ja_foi
    ltr = str(qual_letra_inp.get()).lower()
    ctd = 0
    tem = False
    qual_letra_inp.delete(0,END)

    if ltr in ja_foi or ltr.upper() in traços:
        mensageiro("Essa letra já foi.")

    if ltr.isalpha() and len(ltr) == 1:
        for i in palavra:
            if i == ltr:
                traços.pop(ctd)
                traços.insert(ctd,ltr.upper())
                tem = True
            ctd += 1

        if tem == False and ltr not in ja_foi:
            lifes -= 1
            ja_foi.append(ltr)
            dano()
        finish()  
    elif len(ltr) == 0:
        mensageiro("Escreva uma letra.")
    elif len(ltr) > 1:
        mensageiro("Escreva só uma letra.")
    elif not ltr.isalpha():
        mensageiro("Apenas letras são aceitas.")
        
    letras_passadas.set(ja_foi)
    txt_var.set(traços)

def finish():
    global vitória
    global derrota
    global replay

    derrota = Label(frame_1,
                width=100,
                height=2,
                text="DERROTA",
                font="TkMenuFont 40 bold",
                bg=RED,
                fg="white")

    vitória = Label(frame_1,
                width=100,
                height=2,
                text="VITÓRIA",
                font="TkMenuFont 40 bold",
                bg=GREEN,
                fg="white")
    
    replay = Button(frame_1,
            text="jogar\nnovamente",
            bg= BG_BTCOLOR,
            fg="white",
            cursor="hand2",
            font="TkMenuFont 12 bold",
            width=9,
            height=2,
            border=0,
            activebackground=BG_TXTCOLOR,
            activeforeground="white",
            command=lambda:denovo()
            )

    if lifes == 1:
        mensageiro("Você só tem mais uma vida!")

    elif lifes == 0:
        derrota.place(relx=0.5, rely=0.45, anchor="center")
        replay.place(relx=0.5,rely=0.8,anchor="center")

    elif "_" not in traços:
        vitória.place(relx=0.5, rely=0.45, anchor="center")
        replay.place(relx=0.5,rely=0.8,anchor="center")

def mensageiro(erro):
    global msg
    msg = erro
    tamanho = len(msg)
    if ok.cget("state") == NORMAL:
        qual_letra_inp.config(state=DISABLED)
        ok.config(state=DISABLED)
        for i in range(tamanho+1):
            mensagem.set(msg[:i])
            msg_box.update()
            time.sleep(0.07)
        time.sleep(1.5)
        for i in range(tamanho+1):
            mensagem.set(msg[:-i])
            msg_box.update()
            time.sleep(0.06)
        ok.config(state=NORMAL)
        qual_letra_inp.config(state=NORMAL)

def denovo():
    

    global lifes, ja_foi, traços, v1, v2, v3, v4, v5, v6, palavra, dick

    palavra, dick = escolhe_palavra()
    ja_foi.clear()
    lifes = 6
    traços = traçado(palavra)
    letras_passadas.set(ja_foi)
    txt_var.set(traços)
    dica_var.set(dick)

    v1 = Vidas(frame_1,text="O")
    v1.place(relx=0.66,rely=0.28,anchor="center")
    v1.tkraise(aboveThis=img_widget)

    v2 = Vidas(frame_1,text="|")
    v2.place(relx=0.66,rely=0.4,anchor="center")
    v2.tkraise(aboveThis=img_widget)

    v3 = Vidas(frame_1,text="/")
    v3.place(relx=0.63,rely=0.4,anchor="center")
    v3.tkraise(aboveThis=img_widget)

    v4 = Vidas(frame_1,text="\\")
    v4.place(relx=0.69,rely=0.4,anchor="center")
    v4.tkraise(aboveThis=img_widget)

    v5 = Vidas(frame_1,text="\\")
    v5.place(relx=0.68,rely=0.52,anchor="center")
    v5.tkraise(aboveThis=img_widget)

    v6 = Vidas(frame_1,text="/")
    v6.place(relx=0.64,rely=0.52,anchor="center")
    v6.tkraise(aboveThis=img_widget)

    try:
        derrota.destroy()
        vitória.destroy()
        replay.destroy()
    finally:
        if Widget.winfo_exists(telainicial):
            telainicial.destroy()

traços = traçado(palavra)
# ----- Win Config ---------------------------------------
win = Tk()
winX = (win.winfo_screenmmwidth()//2)+250
win.geometry(f"500x300+{str(winX)}+150")
win.title("Forca!")
win.resizable(False,False)
win.configure(bg=BG_COLOR)

# ----- Frame1 -------------------------------------------
frame_1 = Frame(win, height=500, width=500, bg=BG_COLOR)
frame_1.pack()
frame_1.pack_propagate(False)

mensagem = StringVar()
mensagem.set(msg)

txt_var = StringVar()
txt_var.set(traços)

dica_var = StringVar()
dica_var.set(dick)

letras_passadas = StringVar()

og_forca = (Image.open("forca.png"))
re_forca = og_forca.resize((125,150))
forca_img = ImageTk.PhotoImage(re_forca)
img_widget = Label(frame_1, image=forca_img,bg=BG_COLOR)
img_widget.place(relx=0.6,rely=0.12)

dicaTXT = Label(frame_1,text="Dica:",
                fg="white",
                bg=BG_COLOR,
                font=("TkMenuFont", 13),
                ).place(relx=0.25,rely=0.18,anchor="center")

dicaValue = Label(frame_1,
                  textvariable= dica_var,
                  fg="white",
                  bg=BG_COLOR,
                  font=("TkMenuFont 14 bold")
                  ).place(relx=0.25,rely=0.27,anchor="center")

palavra_na_tela = Label(frame_1,
                        textvariable=txt_var,
                        fg="white",
                        bg=BG_COLOR,
                        font=("TkMenuFont", 20)
                        )
palavra_na_tela.place(relx=0.25,rely=0.38, anchor="center")

qual_letra_txt = Label(frame_1,
                       text="LETRA:",
                       fg="white",
                       bg=BG_COLOR,
                       font=("TkMenuFont 11 bold")
                       ).place(relx=0.095,rely=0.453)

qual_letra_inp = Entry(frame_1,
                       bg=BG_TXTCOLOR,
                       fg="white",
                       cursor="xterm",
                       insertbackground="light gray",
                       font=("TkMenuFont 12 bold"),
                       width=10,
                       border=0.4,
                       justify="center",
                       disabledbackground=BG_BTCOLOR
                       )
qual_letra_inp.place(relx=0.213,rely=0.45)

ok = Button(frame_1,
            text="ok",
            bg= BG_BTCOLOR,
            fg="white",
            cursor="hand2",
            font="TkMenuFont 12 bold",
            width=6,
            height=1,
            border=0,
            activebackground=BG_TXTCOLOR,
            activeforeground="white",
            command=lambda:letrando()
            )

win.bind("<Return>", letrando)
ok.place(relx=0.25,rely=0.6, anchor="center")

letras_falhas = Label(frame_1,
                      textvariable=letras_passadas,
                      bg=BG_COLOR,
                      fg=RED,
                      font="TkMenuFont 15 bold",
                      width=8)
letras_falhas.place(relx=0.25,rely=0.76,anchor="center")

msg_box = Label(frame_1,
                textvariable=mensagem,
                fg= RED,
                bg= BG_COLOR,
                font="TkMenuFont 12")
msg_box.place(relx=0.05,rely=0.9,anchor="w")

telainicial = Frame(frame_1, height=500, width=500, bg=BG_COLOR)
telainicial.pack()

start = Button(telainicial,
            text="começar",
            bg= BG_BTCOLOR,
            fg="white",
            cursor="hand2",
            font="TkMenuFont 12 bold",
            width=8,
            height=1,
            border=0,
            activebackground=BG_TXTCOLOR,
            activeforeground="white",
            command=lambda:denovo())
start.place(rely=0.5,relx=0.5,anchor="center")

win.mainloop()