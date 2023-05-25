import pandas as pd
import os
import re

class acesso_db:
    def existencia_db():
        if (os.path.isfile('./user_db.csv')) is True:
            return True
        else:
            return False

    def cadastrarUser(new_user_entry):
        if acesso_db.existencia_db(): 
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=False, sep=';')
        else:
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=True, sep=';')

        return True

    def validarLogin(self, email_login, senha_login):

        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv', sep = ';')

            for email in user_db.loc[:,"E-mail"]:
                if email == email_login:
                    index = int(''.join(filter(str.isdigit, str(user_db.index[user_db['E-mail']==email_login].tolist()))))
                    senha_db = str(user_db.at[index,"Senha"])
                    if str(senha_login) == senha_db:
                        self.nomeUserLogin = user_db.at[index,"Nome"]
                        return 2 #Autenficado com sucesso
                    else:
                        return 1 #Senha incorreta
            return 0 #E-mail não encontrado
        
        else:
            return 0

    def verificarCadEmail(email_teste):
        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv', sep = ';')
  
            for email in user_db.loc[:,"E-mail"]:
                if email == email_teste:
                    return False #Este e-mail já está cadastrado
        return True #Este e-email não está cadastrado

class validacao_info:
    def validacaoEmail(tipo):
        while True:
            if tipo == 1:      #CADASTRO
                emailtestador   = str(input('INSIRA UM E-MAIL: '))
            elif tipo == 2:    #LOGIN
                emailtestador   = str(input('INSIRA SEU E-MAIL: '))
            
            if (not re.fullmatch(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", emailtestador)) == False:
                if tipo == 1: #CADASTRO
                    if acesso_db.verificarCadEmail(emailtestador):
                        break
                    else:
                        print('''
        Este e-mail já está cadastrado. Por favor, tente novamente.
            ''')
                elif tipo == 2: #LOGIN
                    break
            else:
                print('''
        A informação inserida não se refere a um email. Por favor, tente novamente.
        ''')
                
        return(emailtestador)

    def validacaoCFF(self, numeros):
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

            if validacao_info.validacaoCFF(self, cpf):
                break
            else:
                print('''
        A informação inserida não se refere a um CPF válido. Por favor, tente novamente.
        ''')
    
        return(cpf)
        
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

    def telaCadastro(self):

        # Tela de Cadastro
        print('''
        -------------- CADASTRO DE USUÁRIO ------------
        ''')

        nomeUser    = str(input('NOME E SOBRENOME: '))
        emailUser   = validacao_info.validacaoEmail(1)
        senhaUser   = str(input('CRIE UMA SENHA: ')) 
        nascUser    = input('DATA DE NASCIMENTO: ') # Alguma forma de armazenar data?
        
        cpfUser     = validacao_info.perguntarCPF(self)

        new_user = pd.DataFrame({'Nome':[nomeUser],
        'E-mail':[emailUser],
        'Senha': [senhaUser],
        'Nascimento': [nascUser],
        'CPF': [cpfUser]})
        
        if self.telaConfirmacao() == 1:
            if acesso_db.cadastrarUser(new_user):
                print('''
---> Cadastro realizado com sucesso.
                
                ''')
                sistemaLoja.telaInicial(self) 
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self)
 
    def processoLogin(self, emailUserLogin, senhaUser):
        if self.telaConfirmacao() == 1:
                match acesso_db.validarLogin(self, emailUserLogin, senhaUser):
                    case (0) | (1): #0 = E-mail não encontrado | 1 = Senha incorreta
                        print('''
---> O e-mail ou senha inserido não está correto.
        Por favor, tente novamente''')
                        sistemaLoja.telaLogin(self)

                    case 2: #Validação com sucesso
                        print('''
---> Login realizado com sucesso.

                Seja bem-vindo, ''', self.nomeUserLogin,'''!
                ''')
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

        emailLogin   = validacao_info.validacaoEmail(2)
        senhaLogin   = str(input('INSIRA SUA SENHA: ')) 

        sistemaLoja.processoLogin(self, emailLogin, senhaLogin)



if __name__ == "__main__":
    # Este IF serve para que o código seja executado
    sistema = sistemaLoja()