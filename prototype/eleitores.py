import pickle


eleitores = [
    {"nome": "João Silva", "titulo": "12345", "cpf": "111.222.333-44", "rg": "MG1234567"},
    {"nome": "Maria Oliveira", "titulo": "67890", "cpf": "555.666.777-88", "rg": "SP2345678"},
    {"nome": "Carlos Souza", "titulo": "54321", "cpf": "999.000.111-22", "rg": "RJ3456789"}
]


with open("eleitores.pkl", "wb") as file:
    pickle.dump(eleitores, file)

print("Arquivo eleitores.pkl criado com sucesso!")
