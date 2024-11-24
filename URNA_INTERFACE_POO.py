#Replicar o arquivo URNA_INTERFACE em POO

import tkinter as tk
from tkinter import Toplevel, messagebox
import pickle
import os
import winsound
from PIL import Image, ImageTk

class Urna:
    eleitores: list
    candidatos: list
    votos: list
    voto_atual: str
    eleitor_atual: dict
    tentativas: int
    
    quadrados: list

    tela_label: tk.Label
    label_numero: tk.Label
    label_nome: tk.Label
    label_partido: tk.Label
    label_foto: tk.Label

    janela_cadastro: Toplevel

    entry_titulo: tk.Entry
    entry_cpf: tk.Entry
    entry_rg: tk.Entry

    frame_dir: tk.Frame
    frame_esq: tk.Frame

    def __init__(self):
        self.eleitores = self.carregar_pkl("eleitores.pkl")
        self.candidatos = self.carregar_pkl("candidatos.pkl")
        self.votos = self.carregar_pkl("votos.pkl")
        self.voto_atual = ""
        self.eleitor_atual = None
        self.tentativas = 0

    def carregar_pkl(self, nome_arquivo: str):
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                return pickle.load(file)
        else:
            return []

    def salvar_pkl(self, nome_arquivo: str, dados: list):
        with open(nome_arquivo, "wb") as file:
            pickle.dump(dados, file)

    def tocar_som_confirmacao(self):
        winsound.MessageBeep(winsound.MB_OK)

    def buscar_eleitor(self, titulo: str, cpf: str, rg: str):
        for eleitor in self.eleitores:
            if eleitor["titulo"] == titulo and eleitor["cpf"] == cpf and eleitor["rg"] == rg:
                if eleitor not in self.votos:
                    return eleitor
                else:
                    messagebox.showerror("Erro", "Este eleitor já votou.")
                    return None
        self.tentativas += 1
        if self.tentativas >= 3:
            messagebox.showerror("Erro", "Número máximo de tentativas excedido. Voto registrado como NULO.")
            return None
        messagebox.showerror("Erro", "Dados incorretos. Tente novamente.")
        return None

    def buscar_candidato(self, numero: str):
        for candidato in self.candidatos:
            if candidato["numero"] == numero:
                return candidato
        return None

    def registrar_voto(self, numero_voto: str):
        candidato = self.buscar_candidato(numero_voto)
        if candidato:
            self.votos.append(candidato)
            self.salvar_pkl("votos.pkl", self.votos)
            self.tocar_som_confirmacao()
            messagebox.showinfo("Voto registrado", f"Voto para {candidato['nome']} registrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Candidato não encontrado.")
    
    def atualizar_tela(self, texto: str):
        self.tela_label.config(text=texto)

    def adicionar_numero(self, numero: int):
        if len(self.voto_atual) < 2:
            self.voto_atual += numero
            self.atualizar_tela(self.voto_atual)
            self.preencher_quadrados()

    def corrigir(self):
        self.voto_atual = ""
        self.atualizar_tela(self.voto_atual)
        self.preencher_quadrados()

    def voto_branco(self):
        self.registrar_voto("branco")
        self.corrigir()

    def preencher_quadrados(self):
        for i, quadrado in enumerate(self.quadrados):
            if i < len(self.voto_atual):
                quadrado.config(text=self.voto_atual[i])
            else:
                quadrado.config(text="[]")
    
    def confirmar(self):
        if not self.voto_atual:
            messagebox.showerror("Erro", "Voto em branco. Por favor, insira um número.")
            return
    
        candidato = self.buscar_candidato(self.voto_atual)
        if candidato:
            self.registrar_voto(self.voto_atual)
            self.mostrar_informacoes_candidato(candidato)
            messagebox.showinfo("Confirmação", f"Voto registrado para {candidato['nome']}")
        else:
            self.registrar_voto("nulo")
            messagebox.showinfo("Confirmação", "Voto registrado como NULO.")
        
        self.corrigir
        self.eleitor_atual = None
        self.abrir_janela_cadastro()

    def mostrar_informacoes_candidato(self, candidato: dict):
        self.label_numero.config(text=f"NUMERO: {candidato['numero']}")
        self.label_nome.config(text=f"CANDIDATO: {candidato['nome']}")
        self.label_partido.config(text=f"PARTIDO: {candidato['partido']}")

        try:
            imagem_candidato = Image.open(f"imagens/{candidato['numero']}.png")
            imagem_candidato = imagem_candidato.resize((100, 100))
            img = ImageTk.PhotoImage(imagem_candidato)
            self.label_foto.config(image=img)
            self.label_foto.image = img
        except FileNotFoundError:
            self.label_foto.config(text="Imagem não encontrada", image=None)

    def abrir_janela_cadastro(self):
        self.janela_cadastro = Toplevel()
        self.janela_cadastro.title("Cadastro de Eleitor")
        self.janela_cadastro.geometry("400x300+500+300")

        label_titulo = tk.Label(self.janela_cadastro, text="Título de Eleitor:", font=("Arial", 14))
        label_titulo.pack(pady=5)
        self.entry_titulo = tk.Entry(self.janela_cadastro, font=("Arial", 14))
        self.entry_titulo.pack(pady=5)

        label_cpf = tk.Label(self.janela_cadastro, text="CPF:", font=("Arial", 14))
        label_cpf.pack(pady=5)
        self.entry_cpf = tk.Entry(self.janela_cadastro, font=("Arial", 14))
        self.entry_cpf.pack(pady=5)

        label_rg = tk.Label(self.janela_cadastro, text="RG:", font=("Arial", 14))
        label_rg.pack(pady=5)
        self.entry_rg = tk.Entry(self.janela_cadastro, font=("Arial", 14))
        self.entry_rg.pack(pady=5)

        btn_confirmar = tk.Button(self.janela_cadastro, text="Confirmar", command=self.confirmar_dados, font=("Arial", 14), bg="blue")
        btn_confirmar.pack(pady=20)

    def confirmar_dados(self):
        titulo = self.entry_titulo.get()
        cpf = self.entry_cpf.get()
        rg = self.entry_rg.get()

        eleitor = self.buscar_eleitor(titulo, cpf, rg)
        if eleitor:
            self.eleitor_atual = eleitor
            self.atualizar_tela(f"Eleitor: {eleitor['nome']}")
            self.janela_cadastro.destroy()
            self.criar_quadrados()

    def criar_quadrados(self):
        self.voto_atual = ""

        teclado_frame = tk.Frame(self.frame_dir)
        teclado_frame.pack(pady=10)

        self.quadrados = []
        for i in range(2):
            quadrado = tk.Label(teclado_frame, text="[]", font=("Arial", 36), width=4, height=2, relief="solid")
            quadrado.grid(row=0, column=i, padx=5, pady=5)
            self.quadrados.append(quadrado)

        Bts = [
            ("1", lambda: self.adicionar_numero("1")), ("2", lambda: self.adicionar_numero("2")), ("3", lambda: self.adicionar_numero("3")),
            ("4", lambda: self.adicionar_numero("4")), ("5", lambda: self.adicionar_numero("5")), ("6", lambda: self.adicionar_numero("6")),
            ("7", lambda: self.adicionar_numero("7")), ("8", lambda: self.adicionar_numero("8")), ("9", lambda: self.adicionar_numero("9")),
            ("0", lambda: self.adicionar_numero("0"))
        ]

        for i, (txt, cmd) in enumerate(Bts):
            btn = tk.Button(teclado_frame, text=txt, command=cmd, font=("Arial", 18), width=4, height=2)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        frame_botoes = tk.Frame(self.frame_dir)
        frame_botoes.pack(pady=10)

        btn_branco = tk.Button(frame_botoes, text="BRANCO", command=self.voto_branco, font=("Arial", 14), bg="white", width=10)
        btn_branco.pack(side=tk.LEFT, padx=10)

        btn_confirmar = tk.Button(frame_botoes, text="CONFIRMAR", command=self.confirmar, font=("Arial", 14), bg="green", width=10)
        btn_confirmar.pack(side=tk.LEFT, padx=10)

        btn_corrigir = tk.Button(frame_botoes, text="CORRIGIR", command=self.corrigir, font=("Arial", 14), bg="yellow", width=10)
        btn_corrigir.pack(side=tk.LEFT, padx=10)

    def iniciar(self):
        root = tk.Tk()
        root.title("Urna Eletrônica")
        root.geometry("700x500")
        root.resizable(False, False)

        self.frame_esq = tk.Frame(root, width=350, height=500, bg="black")
        self.frame_dir = tk.Frame(root, width=350, height=500)

        self.frame_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tela_label = tk.Label(self.frame_esq, text='Urna Eletrônica', font=("Arial", 24), bg="white", anchor="center")
        self.tela_label.pack(fill=tk.BOTH, expand=True)

        self.label_foto = tk.Label(self.frame_esq, text="Foto", font=("Arial", 12), bg="white")
        self.label_foto.pack(pady=10)
        
        self.label_nome = tk.Label(self.frame_esq, text="Candidato: ", font=("Arial", 14), bg="white")
        self.label_nome.pack()

        self.label_numero = tk.Label(self.frame_esq, text="Número: ", font=("Arial", 14), bg="white")
        self.label_numero.pack()

        self.label_partido = tk.Label(self.frame_esq, text="Partido: ", font=("Arial", 14), bg="white")
        self.label_partido.pack()

        self.abrir_janela_cadastro()
        root.mainloop()

if __name__ == "__main__":
    urna = Urna()
    urna.iniciar()