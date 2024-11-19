import pickle


candidatos = [
    {"nome": "Candidato A", "numero": "10", "partido": "Partido X"},
    {"nome": "Candidato B", "numero": "20", "partido": "Partido Y"},
    {"nome": "Candidato C", "numero": "30", "partido": "Partido Z"}
]


with open("candidatos.pkl", "wb") as file:
    pickle.dump(candidatos, file)

print("Arquivo candidatos.pkl criado com sucesso!")
