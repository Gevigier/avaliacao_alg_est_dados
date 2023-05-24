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
        
        saida = False

        while True:
            try:
                resp = int(input())
                match resp:
                    case 0:
                        saida = True
                    case 1:
                        sistemaLoja.telaLogin(self)
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

    def validacaoEmail(self, tipo):
        while True:
            if tipo == 1:      #CADASTRO
                emailtestador   = str(input('INSIRA UM E-MAIL: '))
            elif tipo == 2:    #LOGIN
                emailtestador   = str(input('INSIRA SEU E-MAIL: '))
            
            if (not re.fullmatch(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", emailtestador)) == False:
                break
            else:
                print('''
        A informação inserida não se refere a um email. Por favor, tente novamente.
        ''')

        return(emailtestador)

    def validacaoCPF(self, numeros):
        cpf_separado = [int(char) for char in numeros if char.isdigit()]

        if len(cpf_separado) == 11:
            if cpf_separado != cpf_separado[::-1]:
                for i in range(9, 11):
                    value = sum((cpf_separado[num] * ((i+1) - num) for num in range(0, i)))
                    digit = ((value * 10) % 11) % 10
                    if digit == cpf_separado[i]:
                        self.cpf = ''.join([str(numero) for numero in cpf_separado])
                        return True
        
        return False
    
    def perguntarCPF(self):
        while True:
            cpf = input('CPF: ')

            if self.validacaoCPF(cpf):
                break
            else:
                print('''
        A informação inserida não se refere a um CPF válido. Por favor, tente novamente.
        ''')
        
        return(self.cpf)

    def validacaoLogin(self, user_db_loc, email_login, senha_login):
        
        for email in user_db_loc.loc[:,"E-mail"]:
            if email == email_login:
                index = int(''.join(filter(str.isdigit, str(user_db_loc.index[user_db_loc['E-mail']==email_login].tolist()))))
                senha_db = user_db_loc.at[index,"Senha"]
                if senha_login == senha_db:
                    self.nomeUserLogin = user_db_loc.at[index,"Nome"]
                    return 2 #Autenficado com sucesso
                else:
                    return 1 #Senha incorreta
        
        return 0 #E-mail não encontrado




    def telaCadastro(self):

        # Tela de Cadastro
        print('''
        -------------- CADASTRO DE USUÁRIO ------------
        ''')

        nomeUser    = str(input('NOME E SOBRENOME: '))

        emailUser   = self.validacaoEmail(1)
                
        senhaUser   = str(input('CRIE UMA SENHA: ')) 
        nascUser    = input('DATA DE NASCIMENTO: ') # Alguma forma de armazenar data?
        
        cpfUser     = self.perguntarCPF()

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
            
    def telaLogin(self):
        # Tela de Login
        print('''
        -------------- ENTRADA DE USUÁRIO -------------
        ''')

        emailUserLogin   = self.validacaoEmail(2)
        senhaUser        = str(input('INSIRA SUA SENHA: ')) 

        if self.telaConfirmacao() == 1:
            if (os.path.isfile('./user_db.csv')) is True:
                user_db = pd.read_csv('./user_db.csv', sep = ';', )

                match self.validacaoLogin(user_db, emailUserLogin, senhaUser):
                    case 0: #E-mail não encontrado
                        print('Este e-mail não está cadastrado')
                    case 1: #Senha incorreta
                        print('Senha incorreta')
                    case 2: #Validação com sucesso
                        print('''
---> Login realizado com sucesso.

                Seja bem-vindo, ''', self.nomeUserLogin,'''!
                ''')

            # else:
                # COMO NÃO HÁ DATA BASE, NÃO PRECISA VERIFICAR, APENAS RETORNAR ERRO
                # new_user.to_csv('./user_db.csv', mode='a', index=False, header=True, sep=';')
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