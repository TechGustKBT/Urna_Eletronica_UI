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
    teclado_frame: tk.Frame
    frame_botoes: tk.Frame

    def __init__(self):
        if not os.path.exists("pickle_files"):
            os.makedirs("pickle_files")
        if not os.path.exists("pickle_files/candidatos.pkl"):
            self.criar_candidatos()
        if not os.path.exists("pickle_files/eleitores.pkl"):
            self.criar_eleitores()
        self.setEleitores(self.carregar_pkl("pickle_files/eleitores.pkl"))
        self.setCandidatos(self.carregar_pkl("pickle_files/candidatos.pkl"))
        self.setVotos(self.carregar_pkl("pickle_files/votos.pkl"))
        self.setVotoAtual("")
        self.setEleitorAtual(None)
        self.setTentativas(0)
    
    def setEleitores(self, eleitores: list):
        self.eleitores = eleitores

    def getEleitores(self):
        return self.eleitores
    
    def setCandidatos(self, candidatos: list):
        self.candidatos = candidatos

    def getCandidatos(self):
        return self.candidatos
    
    def setVotos(self, votos: list):
        self.votos = votos

    def getVotos(self):
        return self.votos
    
    def setVotoAtual(self, voto_atual: str):
        self.voto_atual = voto_atual

    def getVotoAtual(self):
        return self.voto_atual
    
    def setEleitorAtual(self, eleitor_atual: dict):
        self.eleitor_atual = eleitor_atual

    def getEleitorAtual(self):
        return self.eleitor_atual
    
    def setTentativas(self, tentativas: int):
        self.tentativas = tentativas

    def getTentativas(self):
        return self.tentativas
    
    def addTentativa(self):
        self.tentativas += 1

    def contar_votos_por_candidato(self):
        contagem = {}
        for voto in self.votos:
            candidato = voto.get("nome", "NULO")
            if candidato in contagem:
                contagem[candidato] += 1
            else:
                contagem[candidato] = 1
        return contagem

    def addVoto(self, voto: dict):
        self.tocar_som_confirmacao()
        voto["eleitor"] = self.getEleitorAtual()["titulo"]
        self.votos.append(voto)
        self.salvar_pkl("pickle_files/votos.pkl", self.votos)

        contagem_votos = self.contar_votos_por_candidato()
        total_votos = ""
        for candidato, total_votos_candidato in contagem_votos.items():
            total_votos += f"{candidato}: {total_votos_candidato}\n"

        if voto["nome"] == "BRANCO" or voto["nome"] == "NULO":
            messagebox.showinfo("Voto registrado", f"Voto {voto['nome']} registrado com sucesso!\n{total_votos}")
        else:
            messagebox.showinfo("Voto registrado", f"Voto para '{voto['nome']}' registrado com sucesso!\n{total_votos}")

    def setQuadrados(self, quadrados: list):
        self.quadrados = quadrados

    def getQuadrados(self):
        return self.quadrados

    def criar_candidatos(self):
        messagebox.showinfo("Criando candidatos", "arquivo candidatos.pkl não encontrado, criando candidatos padrão")
        candidatos = [
            {"nome": "Candidato A", "numero": "10", "partido": "Partido X"},
            {"nome": "Candidato B", "numero": "20", "partido": "Partido Y"},
            {"nome": "Candidato C", "numero": "30", "partido": "Partido Z"}
        ]

        with open("pickle_files/candidatos.pkl", "wb") as file:
            pickle.dump(candidatos, file)

        print("Arquivo candidatos.pkl criado com sucesso!")

    def criar_eleitores(self):
        messagebox.showinfo("Criando eleitores", "arquivo eleitores.pkl não encontrado, criando eleitores padrão")
        eleitores = [
            {"nome": "João Silva", "titulo": "12345", "cpf": "111.222.333-44", "rg": "MG1234567"},
            {"nome": "Maria Oliveira", "titulo": "67890", "cpf": "555.666.777-88", "rg": "SP2345678"},
            {"nome": "Carlos Souza", "titulo": "54321", "cpf": "999.000.111-22", "rg": "RJ3456789"}
        ]

        with open("pickle_files/eleitores.pkl", "wb") as file:
            pickle.dump(eleitores, file)

        print("Arquivo eleitores.pkl criado com sucesso!")

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
        try:
            winsound.PlaySound("audio/urna_confirma.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(e)

    def tocar_som_tecla(self):
        try:
            winsound.PlaySound("audio/urna_tecla.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(e)

    def buscar_eleitor(self, titulo: str, cpf: str, rg: str):
        for eleitor in self.getEleitores():
            if eleitor["titulo"] == titulo and eleitor["cpf"] == cpf and eleitor["rg"] == rg:
                for voto in self.getVotos():
                    if voto["eleitor"] == eleitor["titulo"]:
                        messagebox.showerror("Erro", "Este eleitor já votou.")
                        return None
                return eleitor
                
        self.addTentativa()

        if self.getTentativas() >= 3:
            messagebox.showerror("Erro", "Número máximo de tentativas excedido.")
            self.root.destroy()
        else: 
            messagebox.showerror("Erro", "Dados incorretos. Tente novamente.")

        return None

    def buscar_candidato(self, numero: str):
        for candidato in self.getCandidatos():
            if candidato["numero"] == numero:
                return candidato
        return None

    def registrar_voto(self, numero_voto: str):
        if numero_voto == "branco":
            self.addVoto({"nome": "BRANCO", "numero": "0", "partido": "NULO"})
            return True
        elif numero_voto == "nulo":
            self.addVoto({"nome": "NULO", "numero": "0", "partido": "NULO"}) 
            return True
        else:
            candidato = self.buscar_candidato(numero_voto)
            if candidato:
                self.addVoto(candidato)
                
                return True
            else:
                messagebox.showerror("Erro", "Candidato não encontrado.")
                return False
    
    def atualizar_tela(self, texto: str):
        self.tela_label.config(text=texto)

    def adicionar_numero(self, numero: int):
        if len(self.getVotoAtual()) < 2:
            self.voto_atual += numero
            self.atualizar_tela(self.getVotoAtual())
            self.preencher_quadrados()
            self.candidato_default("Não Selecionado")

        if len(self.getVotoAtual()) == 2:
            candidato = self.buscar_candidato(self.getVotoAtual())
            if candidato:
                self.mostrar_informacoes_candidato(candidato)
            else:
                self.candidato_default("Não Encontrado")
            
    def corrigir(self):
        self.setVotoAtual("")
        self.atualizar_tela("")
        self.candidato_default("Não Selecionado")
        self.preencher_quadrados()

    def voto_branco(self):
        self.setVotoAtual("BRANCO")
        self.atualizar_tela(self.getVotoAtual())
        self.preencher_quadrados()

    def preencher_quadrados(self):
        try:
            self.tocar_som_tecla()
            for i, quadrado in enumerate(self.getQuadrados()):
                if self.getVotoAtual() == "BRANCO":
                    quadrado.config(text="BRANCO")
                elif i < len(self.getVotoAtual()):
                    quadrado.config(text=self.getVotoAtual()[i])
                else:
                    quadrado.config(text="[]")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Erro ao preencher quadrados:\n"+str(e))

    def confirmar(self):
        if self.getVotoAtual() == "BRANCO":
            confirmar = self.registrar_voto("branco")
        elif len(self.getVotoAtual()) == 0:
            confirmar = self.registrar_voto("nulo")
        else:
            candidato = self.buscar_candidato(self.getVotoAtual())
            if candidato:
                confirmar = self.registrar_voto(self.getVotoAtual())
            else:
                messagebox.showerror("Erro", "Candidato não encontrado.")
                confirmar = False
                
        if confirmar:
            self.corrigir()
            self.limpar_teclado()
            self.abrir_janela_cadastro()



    def mostrar_informacoes_candidato(self, candidato: dict):
        self.label_numero.config(text=f"NÚMERO: {candidato['numero']}")
        self.label_nome.config(text=f"CANDIDATO: {candidato['nome']}")
        self.label_partido.config(text=f"PARTIDO: {candidato['partido']}")

        try:
            imagem_candidato = Image.open(f"imagens/{candidato['numero']}.png")
        except FileNotFoundError:
            imagem_candidato = Image.open(f"imagens/no-image.png")

        imagem_candidato = imagem_candidato.resize((100, 100))
        img = ImageTk.PhotoImage(imagem_candidato)
        self.label_foto.config(image=img)
        self.label_foto.image = img

    def candidato_default(self, texto: str):
        self.label_numero.config(text="NÚMERO: "+texto)
        self.label_nome.config(text="CANDIDATO: "+texto)
        self.label_partido.config(text="PARTIDO: "+texto)

        imagem_candidato = Image.open(f"imagens/no-image.png")
        imagem_candidato = imagem_candidato.resize((100, 100))
        img = ImageTk.PhotoImage(imagem_candidato)
        self.label_foto.config(image=img)
        self.label_foto.image = img

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
            self.setEleitorAtual(eleitor)
            self.atualizar_tela(f"Eleitor: {eleitor['nome']}")
            self.janela_cadastro.destroy()
            self.criar_quadrados()
        

    def criar_quadrados(self):
        self.voto_atual = ""

        self.teclado_frame = tk.Frame(self.frame_dir)
        self.teclado_frame.pack(pady=10)

        self.quadrados = []

        Bts = [
            ("1", lambda: self.adicionar_numero("1")), ("2", lambda: self.adicionar_numero("2")), ("3", lambda: self.adicionar_numero("3")),
            ("4", lambda: self.adicionar_numero("4")), ("5", lambda: self.adicionar_numero("5")), ("6", lambda: self.adicionar_numero("6")),
            ("7", lambda: self.adicionar_numero("7")), ("8", lambda: self.adicionar_numero("8")), ("9", lambda: self.adicionar_numero("9")),
            ("0", lambda: self.adicionar_numero("0"))
        ]

        for i, (txt, cmd) in enumerate(Bts):
            btn = tk.Button(self.teclado_frame, text=txt, command=cmd, font=("Arial", 18), width=4, height=2)
            if txt == "0":  
                btn.grid(row=3, column=1, padx=5, pady=5)
            else:
                btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        self.frame_botoes = tk.Frame(self.frame_dir)
        self.frame_botoes.pack(pady=10)

        btn_branco = tk.Button(self.frame_botoes, text="BRANCO", command=self.voto_branco, font=("Arial", 14), bg="white", width=10)
        btn_branco.pack(side=tk.LEFT, padx=10)

        btn_corrigir = tk.Button(self.frame_botoes, text="CORRIGIR", command=self.corrigir, font=("Arial", 14), bg="red", width=10)
        btn_corrigir.pack(side=tk.LEFT, padx=10)

        btn_confirmar = tk.Button(self.frame_botoes, text="CONFIRMAR", command=self.confirmar, font=("Arial", 14), bg="green", width=10)
        btn_confirmar.pack(side=tk.LEFT, padx=10)



    def limpar_teclado(self):
        self.teclado_frame.destroy()
        self.frame_botoes.destroy()

    def iniciar(self):
        self.root = tk.Tk()
        self.root.title("Urna Eletrônica")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.frame_esq = tk.Frame(self.root, width=350, height=500, bg="black")
        self.frame_dir = tk.Frame(self.root, width=350, height=500)

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

        self.candidato_default("Não Selecionado")
        self.abrir_janela_cadastro()
        self.root.mainloop()

if __name__ == "__main__":
    urna = Urna()
    urna.iniciar()
