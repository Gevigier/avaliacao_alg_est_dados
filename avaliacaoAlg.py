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

class acesso_db_produto:
    def existencia_db_loja():
        if (os.path.isfile('./product_db.csv')) is True:
            return True
        else:
            return False

    def acessar_db(self):
        if acesso_db_produto.existencia_db_loja(): 
            product_db = pd.read_csv('./product_db.csv', sep = ';')
        else:
            product_db = pd.DataFrame({'Produto':['Café Preto', 'Café Expresso', 'Energético'],
            'Valor':['2,00', '5,00', '8,00'],
            'Quantidade': ['27', '53', '42']})

        return(product_db)

    def visualizarValor():
        print('aaaa')

    def visualizarProduto(self, ver_produto):

        db_produto = acesso_db_produto.acessar_db(self)

        todos_produto = ''
        for produto in db_produto.loc[:,"Produto"]:
            todos_produto = todos_produto + produto + ";"
        
        lista_produto = todos_produto.split(';')

        match ver_produto:
            case 0:
                return lista_produto[0]
            case 1:
                return lista_produto[1]
            case 2:
                return lista_produto[2]

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
        

        while True:
            try:
                resp = int(input())
                match resp:
                    case 0:
                        break
                    case 1:
                        sistemaLoja.telaLogin(self)
                    case 2:
                        sistemaLoja.telaCadastro(self)
                    case _:                      
                        raise
                
                break
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')


    def telaConfirmacao():
        # Tela de confirmação para ser usada e reciclada por todo o código
        while True:
            opcoes = int(input('''
            [1] Confirmar                    [0] Cancelar
                        '''))

            match opcoes:
                case 1:
                    return 1 #SIM
                case 0:
                    return 0 #NÃO
                case _:
                    print('Opção incorreta. Insira um número referente a uma das opções disponíveis.') 

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
        
        if sistemaLoja.telaConfirmacao() == 1:
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
            # self.retorno = True
            sistemaLoja.telaInicial(self)
 
    def telaLogin(self):
        # Tela de Login
        print('''
        -------------- ENTRADA DE USUÁRIO -------------
        ''')

        emailLogin   = validacao_info.validacaoEmail(2)
        senhaLogin   = str(input('INSIRA SUA SENHA: ')) 

        if sistemaLoja.telaConfirmacao() == 1:
                match acesso_db.validarLogin(self, emailLogin, senhaLogin):
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
                        
                        sistemaLoja.telaVenda(self)
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self)

    def telaVenda(self):

        print('''
        ===x===x===x===x===x===x===x===x===x===x===x===
              A LOJA DO PROGRAMADOR - ANHANGUERA
        ===x===x===x===x===x===x===x===x===x===x===x===
        
|----------------      |----------------      |----------------   
|               |      |               |      |               |
|               |      |               |      |               |
|  {0}   |      | {1} |      |   {2}  |
|               |      |               |      |               |
|               |      |               |      |               |
----------------|      ----------------|      ----------------|


    Escolha uma opção:
  [1] Comprar "{0}"        [2] Comprar "{1}"
  [3] Comprar "{2}"        [0] Sair
  '''.format(acesso_db_produto.visualizarProduto(self, 0), acesso_db_produto.visualizarProduto(self, 1), acesso_db_produto.visualizarProduto(self, 2)))
        
        cancelar = False

        while True:
            try:
                respVenda = int(input())
                match respVenda:
                    case 0: #Sair
                        print('''
        Ao prosseguir, você será desconectado de sua conta e redirecionado a tela inicial
        ''')
                        if sistemaLoja.telaConfirmacao() == 1:
                            cancelar = True
                        else:
                            print('''
        Perfeito! Adoramos sua presença aqui :)
        ''')
                            sistemaLoja.telaVenda(self)
                    case 1: #Comprar café preto
                        print('comprado café preto')
                    case 2: #Comprar café expresso
                        print('comprado café expresso')
                    case 3: #Comprar Energético
                        print('comprado energético')
                    case _:
                        raise
                
                break
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

        if cancelar == True:
            sistemaLoja()





if __name__ == "__main__":
    # Este IF serve para que o código seja executado
    sistema = sistemaLoja()
    # sistemaLoja.telaVenda()