import tkinter as tk
from tkinter import Toplevel, messagebox
import pickle
import os
import winsound
from PIL import Image, ImageTk


def carregar_pkl(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as file:
            return pickle.load(file)
    else:
        return []


def salvar_pkl(nome_arquivo, dados):
    with open(nome_arquivo, "wb") as file:
        pickle.dump(dados, file)


eleitores = carregar_pkl("eleitores.pkl")
candidatos = carregar_pkl("candidatos.pkl")
votos = carregar_pkl("votos.pkl")

voto_atual = ""
eleitor_atual = None
tentativas = 0


def tocar_som_confirmacao():
    
    winsound.MessageBeep(winsound.MB_OK)


def buscar_eleitor(titulo, cpf, rg):
    global tentativas
    for eleitor in eleitores:
        if eleitor["titulo"] == titulo and eleitor["cpf"] == cpf and eleitor["rg"] == rg:
            if eleitor not in votos:
                return eleitor
            else:
                messagebox.showerror("Erro", "Este eleitor já votou.")
                return None
    tentativas += 1
    if tentativas >= 3:
        messagebox.showerror("Erro", "Número máximo de tentativas excedido. Voto registrado como NULO.")
        return None
    messagebox.showerror("Erro", "Dados incorretos. Tente novamente.")
    return None


def buscar_candidato(numero):
    for candidato in candidatos:
        if candidato["numero"] == numero:
            return candidato
    return None


def registrar_voto(numero_voto):
    votos.append(numero_voto)
    salvar_pkl("votos.pkl", votos)
    messagebox.showinfo("Confirmação", "Voto registrado com sucesso!")
    tocar_som_confirmacao()


def atualizar_tela(texto):
    tela_label.config(text=texto)


def adicionar_numero(numero):
    global voto_atual
    if len(voto_atual) < 2:
        voto_atual += numero
        atualizar_tela(voto_atual)
        preencher_quadrados()


def corrigir():
    global voto_atual
    voto_atual = ""
    atualizar_tela("")
    preencher_quadrados()


def voto_branco():
    registrar_voto("branco")
    corrigir()


def confirmar():
    global voto_atual
    global eleitor_atual
    if not voto_atual:
        messagebox.showerror("Erro", "Digite um número ou vote em branco.")
        return

    candidato = buscar_candidato(voto_atual)
    if candidato:
        registrar_voto(voto_atual)
        mostrar_informacoes_candidato(candidato)
        messagebox.showinfo("Confirmação", f"Voto registrado para {candidato['nome']}")
    else:
        registrar_voto("nulo")
        messagebox.showinfo("Confirmação", "Voto registrado como NULO.")
    corrigir()
    eleitor_atual = None
    abrir_janela_cadastro()


def mostrar_informacoes_candidato(candidato):
    label_numero.config(text=f"NUMERO: {candidato['numero']}")
    label_nome.config(text=f"CANDIDATO: {candidato['nome']}")
    label_partido.config(text=f"PARTIDO: {candidato['partido']}")

    try:
        imagem_candidato = Image.open(f"fotos/{candidato['numero']}.jpg")
        imagem_candidato = imagem_candidato.resize((100, 100))
        img = ImageTk.PhotoImage(imagem_candidato)
        label_foto.config(image=img)
        label_foto.image = img
    except FileNotFoundError:
        label_foto.config(text="Imagem não encontrada", image=None)


def preencher_quadrados():
    global voto_atual
    for i, quadrado in enumerate(quadrados):
        if i < len(voto_atual):
            quadrado.config(text=voto_atual[i])
        else:
            quadrado.config(text="[]")


def criar_quadrados():
    global voto_atual
    voto_atual = ""

    teclado_frame = tk.Frame(frame_dir)
    teclado_frame.pack(pady=10)

    global quadrados
    quadrados = []
    for i in range(2):
        quadrado = tk.Label(teclado_frame, text="[]", font=("Arial", 36), width=4, height=2, relief="solid")
        quadrado.grid(row=0, column=i, padx=5, pady=5)
        quadrados.append(quadrado)

    Bts = [
        ("1", lambda: adicionar_numero("1")), ("2", lambda: adicionar_numero("2")), ("3", lambda: adicionar_numero("3")),
        ("4", lambda: adicionar_numero("4")), ("5", lambda: adicionar_numero("5")), ("6", lambda: adicionar_numero("6")),
        ("7", lambda: adicionar_numero("7")), ("8", lambda: adicionar_numero("8")), ("9", lambda: adicionar_numero("9")),
        ("0", lambda: adicionar_numero("0"))
    ]

    for i, (txt, cmd) in enumerate(Bts):
        btn = tk.Button(teclado_frame, text=txt, command=cmd, font=("Arial", 18), width=4, height=2)
        btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    frame_botoes = tk.Frame(frame_dir)
    frame_botoes.pack(pady=10)

    btn_branco = tk.Button(frame_botoes, text="BRANCO", command=voto_branco, font=("Arial", 14), bg="white", width=10)
    btn_branco.pack(side=tk.LEFT, padx=10)

    btn_confirmar = tk.Button(frame_botoes, text="CONFIRMAR", command=confirmar, font=("Arial", 14), bg="green", width=10)
    btn_confirmar.pack(side=tk.LEFT, padx=10)

    btn_corrigir = tk.Button(frame_botoes, text="CORRIGIR", command=corrigir, font=("Arial", 14), bg="yellow", width=10)
    btn_corrigir.pack(side=tk.LEFT, padx=10)


def abrir_janela_cadastro():
    
    global eleitor_atual

    janela_cadastro = Toplevel(root)
    janela_cadastro.title("Cadastro de Eleitor")
    janela_cadastro.geometry("400x300+500+300")

    def confirmar_dados():
        global eleitor_atual
        titulo = entry_titulo.get()
        cpf = entry_cpf.get()
        rg = entry_rg.get()
        eleitor_atual = buscar_eleitor(titulo, cpf, rg)
        if eleitor_atual:
            atualizar_tela("Digite o número do candidato.")
            janela_cadastro.destroy()
            criar_quadrados()

    label_titulo = tk.Label(janela_cadastro, text="Título de Eleitor:", font=("Arial", 14))
    label_titulo.pack(pady=5)
    entry_titulo = tk.Entry(janela_cadastro, font=("Arial", 14))
    entry_titulo.pack(pady=5)

    label_cpf = tk.Label(janela_cadastro, text="CPF:", font=("Arial", 14))
    label_cpf.pack(pady=5)
    entry_cpf = tk.Entry(janela_cadastro, font=("Arial", 14))
    entry_cpf.pack(pady=5)

    label_rg = tk.Label(janela_cadastro, text="RG:", font=("Arial", 14))
    label_rg.pack(pady=5)
    entry_rg = tk.Entry(janela_cadastro, font=("Arial", 14))
    entry_rg.pack(pady=5)

    btn_confirmar = tk.Button(janela_cadastro, text="Confirmar", command=confirmar_dados, font=("Arial", 14), bg="blue")
    btn_confirmar.pack(pady=20)


root = tk.Tk()
root.title("Urna Eletrônica")
root.geometry("700x500")
root.resizable(False, False)

frame_esq = tk.Frame(root, width=350, height=500, bg="black")
frame_dir = tk.Frame(root, width=350, height=500)

frame_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tela_label = tk.Label(frame_esq, text='Urna Eletrônica', font=("Arial", 24), bg="white", anchor="center")
tela_label.pack(fill=tk.BOTH, expand=True)

label_foto = tk.Label(frame_esq, text="Foto", font=("Arial", 12), bg="white")
label_foto.pack(pady=10)

label_nome = tk.Label(frame_esq, text="Candidato: ", font=("Arial", 14), bg="white")
label_nome.pack()

label_numero = tk.Label(frame_esq, text="Número: ", font=("Arial", 14), bg="white")
label_numero.pack()

label_partido = tk.Label(frame_esq, text="Partido: ", font=("Arial", 14), bg="white")
label_partido.pack()

abrir_janela_cadastro()
root.mainloop()
