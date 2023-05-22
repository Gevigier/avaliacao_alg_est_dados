import pandas as pd

class sistemaLoja:

    def __init__(self):
        print('inicializado')
        sistemaLoja.telaInicial(self)
        
    def telaInicial(self):
        # Tela inicial
        print('''
        ===x===x===x=== LOJA ANHANGUERA ===x===x===x===
                  Seja bem-vindo a nossa loja!

        Escolha uma opção:
        1. Entrar                       2. Cadastre-se
                                        0. Encerrar''')
        
        while True:
            try:
                resp = int(input())
                match resp:
                    case 0:
                        print('fechar')
                    case 1:
                        print('entrar')
                    case 2:
                        print('cadastrar')
                        sistemaLoja.telaCadastro(self)
                
                break
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')


    def telaCadastro(self):

        # Tela de Cadastro
        print('''
        -------------- CADASTRO DE USUÁRIO ------------''')

        while True:
            try:
                # TENTA ABRIR A BASE DE DADOS (ARQUIVO CSV) DE USUÁRIOS
                user_db = pd.read_csv('./user_db.csv', sep=';')
            except:
                # CASO NÃO CONSIGA, CRIA UMA NOVA BASE DE DADOS VAZIA
                user_db = pd.DataFrame({'Nome':[],
                'E-mail':[],
                'Senha': [],
                'Nascimento': [],
                'CPF': []})
                break

        nomeUser    = str(input('NOME E SOBRENOME: '))
        emailUser   = str(input('INSIRA UM E-MAIL: ')) # Criar um sistema de teste pra ver se é um e-mail?
        senhaUser   = str(input('CRIE UMA SENHA: ')) 
        nascUser    = input('DATA DE NASCIMENTO: ') # Alguma forma de armazenar data?
        cpfUser     = str(input('CPF: ')) # Alguma forma de verificar se é um cpf?

        # append data frame to CSV file
        # user_db.to_csv('./user_db.csv', mode='a', index=False, header=False, sep=';')
                       




        while True:
            try:

                print('1. Confirmar     2. Cancelar')
                confirmacao = int(input())

                match confirmacao:
                    case 1:
                        print('confirmar')

                    case 2:
                        print('cancelar')
                        sistemaLoja.telaInicial(self)

                break
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')        
        



    
    def resto():
        # Tela de Login
        print('''
        -------------- ENTRADA DE USUÁRIO -------------''')

        email      = str(input('INSIRA UM E-MAIL: ')) # Criar um sistema de teste pra ver se é um e-mail?
        senha      = str(input('CRIE UMA SENHA: ')) # Teste para quão forte é a senha?

        confirmacao = str(input('1. Confirmar     2. Cancelar')) # Fazer esquema de insistir até que seja a opção correta




if __name__ == "__main__":

    sistema = sistemaLoja()