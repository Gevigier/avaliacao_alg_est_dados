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

        entry_db = pd.read_csv('./user_db.csv', sep=';')
        user_db = pd.DataFrame(entry_db)
        # print(dfCadastro)

        # user_db = pd.DataFrame({'Nome':['admin', 'Microsoft', 'SpaceX','Amazon','Samsung'],
        # 'E-mail':['admin@admin.com', 'Bill Gates, Paul Allen','Elon Musk','Jeff Bezos', 'Lee Byung-chul'],
        # 'Senha': [123456, 1975, 2002, 1994, 1938],
        # 'Nascimento': ['04-03-00', '144,106', '6,500', '647,500', '320,671'],
        # 'CPF': ['20456974348', '12345678901','1234','123154','487978']})

        # append data frame to CSV file
        # user_db.to_csv('./user_db.csv', mode='a', index=False, header=False, sep=';')
                       
        # print(dfCadastro)

        # print(pd.read_csv('./user_db.csv'))

        nomeUser    = str(input('NOME E SOBRENOME: '))
        emailUser   = str(input('INSIRA UM E-MAIL: ')) # Criar um sistema de teste pra ver se é um e-mail?
        senhaUser   = str(input('CRIE UMA SENHA: ')) # Teste para quão forte é a senha?
        nascUser    = input('DATA DE NASCIMENTO: ') # Alguma forma de armazenar data?
        cpfUser     = str(input('CPF: '))

        while True:
            try:

                print('1. Confirmar     2. Cancelar')
                confirmacao = int(input())

                match confirmacao:
                    case 1:
                        print('confirmar')
                        print(user_db)
                        # new_row    = {'Nome':'nomeUser', 'E-mail':'emailUser', 'Senha':'senhaUser', 'Nascimento':'nascUser', 'CPF':'cpfUser'}
                        # print(new_row)

                        f = user_db.append({'Name' : 'Ankit', 'Articles' : 97, 'Improved' : 2200},
                                ignore_index = True)

                        print('teste')
                        print(f)
                        # dfCadastro = user_db.append(new_row, ignore_index=True)
                        # print('novo df')
                        # print(dfCadastro)

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

        # Tela para ADM
        print('''
        ----------------- ADMINISTRAÇÃO ---------------'

        Escolha uma opção:
        1. Cadastrar Produto             0. Desconectar
        ''')


        # Tela de cadastro de Produto
        print('''
        ------------- CADASTRO DE PRODUTO -------------''') 


if __name__ == "__main__":

    sistema = sistemaLoja()