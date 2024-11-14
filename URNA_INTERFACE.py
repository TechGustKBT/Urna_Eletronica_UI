# Estrutua Básica da Interface do Sistema (FELIPE)
# 1. Criar a janela principal da interface gráfica utilizando o módulo tkinter.
# 2. Criar o Layout inicial, com botões e campos de entrada para que o eleitor insira o número do título.
# 3. Implementar o carregamento dos arquivos .pkl ou .csv contendo a lista de candidatos e eleitores.
#   a. Carregar esses dados na inicialização do sistema, permitindo acesso aos dados durante a operação da urna.
#   b. Usar o módulo pickle para arquivos .pkl e csv para arquivos .csv.
# __________________________________________________________________________________________________________________

# Verificação do Eleitor e Exibição de Informações (GUSTAVO)
# 1. Validar o título de eleitor inserido no campo de entrada:
#   a. Verificar se o título do eleitor existe na lista de eleitores.
#   b. Exibir os dados do eleitor (nome e título) na tela, se o título for encontrado.
#   c. Caso o título não seja encontrado, exibir uma mensagem de erro pedindo um novo número.
# __________________________________________________________________________________________________________________

# Entrada e Validação do Voto (LEO)
# 1. Implementar o campo para inserção do número do candidato ou seleção de voto branco/nulo.
# 2. Criar um botão para confirmar o vot.
# 3. Validar o número do candidato inserido:
#   a. Verificar se o número corresponde a um candidato existente.
#   b. Adicionar opções para voto branco e corrigir.
#   c. Exibir dados do candidato (nome, número e foto) antes de confirmar o voto.
# __________________________________________________________________________________________________________________

# Armazenamento do Voto e Reinicialização (PABLO)
# 1. Computar o voto:
#   a. Armazenar o voto em um arquivo .pkl, incluindo o número do eleitor e o candidato escolhido.
#   b. Registrar e salvar os dados no arquivo .pkl com o total de votos de cada candidato, incluindo votos brancos e nulos.
# 2. Reiniciar a interface para permitir que um novo eleitor insira seu título após a confirmação do voto anterior.
#   a. Criar um mecanismo para reiniciar a tela de entrada após o voto.