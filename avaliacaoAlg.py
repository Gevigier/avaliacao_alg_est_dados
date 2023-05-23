import pandas as pd
import os
import re

class sistemaLoja:

    def __init__(self):
        # Inicialização
        sistemaLoja.telaInicial(self)
        


    def telaInicial(self):
        # Tela inicial
        print('''
        ===x===x===x=== LOJA ANHANGUERA ===x===x===x===
                  Seja bem-vindo a nossa loja!

        Escolha uma opção:
        [1] Entrar                       [2] Cadastre-se
                                         [0] Encerrar''')
        
        while True:
            try:
                resp = int(input())
                match resp:
                    case 0:
                        saida = True
                    case 1:
                        print('entrar')
                    case 2:
                        sistemaLoja.telaCadastro(self)
                
                break
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

        if saida == True:
            exit()



    def telaConfirmacao(self):
        # Tela de confirmação para ser usada e reciclada por todo o código
        while True:
            opcoes = int(input('''
            [1] Confirmar                    [2] Cancelar
                        '''))

            match opcoes:
                case 1:
                    return 1
                case 2:
                    return 0
                case _:
                    print('Opção incorreta. Insira um número referente a uma das opções disponíveis. (func separada)') 


    def telaCadastro(self):

        # Tela de Cadastro
        print('''
        -------------- CADASTRO DE USUÁRIO ------------
        ''')

        nomeUser    = str(input('NOME E SOBRENOME: '))

        while True:
            emailUser   = str(input('INSIRA UM E-MAIL: '))
            
            if (not re.fullmatch(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", emailUser)) == False:
                break
            else:
                print('''
        A informação inserida não se refere a um email. Por favor, tente novamente.
        ''')
                
        senhaUser   = str(input('CRIE UMA SENHA: ')) 
        nascUser    = input('DATA DE NASCIMENTO: ') # Alguma forma de armazenar data?
        cpfUser     = str(input('CPF: ')) # Alguma forma de verificar se é um cpf?

        new_user = pd.DataFrame({'Nome':[nomeUser],
        'E-mail':[emailUser],
        'Senha': [senhaUser],
        'Nascimento': [nascUser],
        'CPF': [cpfUser]})
        
        if self.telaConfirmacao() == 1:
            if (os.path.isfile('./user_db.csv')) is True:
                new_user.to_csv('./user_db.csv', mode='a', index=False, header=False, sep=';')
            else:
                new_user.to_csv('./user_db.csv', mode='a', index=False, header=True, sep=';')
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self)
            
    

    
    def resto():
        # Tela de Login
        print('''
        -------------- ENTRADA DE USUÁRIO -------------''')

        email      = str(input('INSIRA SEU E-MAIL: ')) # Criar um sistema de teste pra ver se é um e-mail?
        senha      = str(input('INSIRA SUA SENHA: ')) # Teste para quão forte é a senha?





if __name__ == "__main__":
    # Este IF serve para que o código seja executado
    sistema = sistemaLoja()