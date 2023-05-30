# CÓDIGO QUE SOLICITA E VALIDA CADA INFORMAÇÃO INSERIDA PELO USUÁRIO NO MOMENTO DO CADASTRO

import re                               #Regex -> validar e-mail
from datetime import datetime           #Usado para pegar a data/hora atual
import string                           #Usado para validar senha

from acesso_db_csv import acesso_db     # Acessa o "banco de dados" de usuário

class validacao_info:
    '''Classe responsável por verificar se os dados inseridos no momento do cadastro estão corretos'''
    def validacaoNome():
        '''Solicita um nome e não retorna até que seja preenchido (não pode estar vazio)'''
        while True:
            try:
                nome = str(input('NOME E SOBRENOME: ')) #Solicita o nome

                if nome.strip(): #Verifica se está vazio
                    break
                else:
                    raise #Por estar vazio, chama a exception
            except:
                print('''
        É necessário inserir seu nome. Por favor, tente novamente.
        ''')
                
        return(nome.strip())

    def validacaoEmail(tipo):
        '''Valida se foi inserido um e-mail (cadastro e login)'''
        while True:
            if tipo == 1:      #CADASTRO
                email_input   = str(input('INSIRA UM E-MAIL: '))
            elif tipo == 2:    #LOGIN
                email_input   = str(input('INSIRA SEU E-MAIL: '))
            
            emailtestador = email_input.strip()

            if (not re.fullmatch(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", emailtestador)) == False:
                if tipo == 1: #CADASTRO
                    if acesso_db.verificarCadEmail(emailtestador):
                        break #Este e-mail não foi cadastrado anteriormente
                    else:
                        print('''
        Houve algum problema. Tente novamente.
            ''') #E-mail já cadastrado
                elif tipo == 2: #LOGIN
                    break
            else:
                print('''
        A informação inserida não se refere a um email. Por favor, tente novamente.
        ''')
                
        return(emailtestador)

    def validacaoCPF():
        '''Solicita um CPF e verifica se é um número de CPF válido'''
        while True:
            cpf = input('CPF: ')

            cpf_separado = [int(char) for char in cpf if char.isdigit()]

            if (len(cpf_separado) == 11) and (cpf_separado != cpf_separado[::-1]):
                for i in range(9, 11):
                    value = sum((cpf_separado[num] * ((i+1) - num) for num in range(0, i)))
                    digit = ((value * 10) % 11) % 10
                    if digit == cpf_separado[i]:
                        cpf_numeros = ''.join([str(numero) for numero in cpf_separado])
                        cpf_valido = True
                    else:
                        cpf_valido = False
            else:
                cpf_valido = False

            if cpf_valido:
                break
            else:
                print('''
        A informação inserida não se refere a um CPF válido. Por favor, tente novamente.
        ''')
    
        return(cpf_numeros)
        
    def validacaoNascimento():
        '''Solicita e verifica se a data de nascimento foi inserida corretamente'''
        while True:
            nascimento = str(input('DATA DE NASCIMENTO (dd/mm/aaaa): '))

            try:
                dataSep = datetime.date(datetime.strptime(nascimento, "%d/%m/%Y"))
                break
            except:
                print('''
                ---> Houve algum erro ao cadastrar sua data de nascimento.
    Por favor, escreva no formato dd/mm/aaaa
    (separado por '/' -> Exemplo: 01/02/2000)
    ''')
                
        return(dataSep)

    def validacaoSenha():
        '''Solicita uma senha e valida se possui os requisitos mínimos necessários'''

        while True:
            l, u, p, d = 0, 0, 0, 0

            senha_input = str(input('''
DIGITE SUA SENHA 
(REQUISITOS: mín. de: 8 caracteres / 1 maiúscula / 1 minúscula / 1 número / 1 caractere especial): '''))
            
            senha = senha_input.strip()

            try:
                if (len(senha) >= 8):
                    for i in senha:
                
                        # counting lowercase alphabets
                        if (i.islower()):
                            l+=1  
                        # counting uppercase alphabets
                        if (i.isupper()):
                            u+=1           
                        # counting digits
                        if (i.isdigit()):
                            d+=1           
                        # counting characters
                        if any(char in set(string.punctuation) for char in i):
                            p+=1

                if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(senha)):
                    break #A senha cumpre os requisitos
                else:
                    raise #A senha não cumpre os requisitos
            except:
                print('''
                
        A senha digitada não contempla um dos requisitos mínimos. Por favor, tente novamente.
''')
                
        while True: #Pede para a senha ser inserida novamente
            try:
                senha_repete = str(input('''
DIGITE SUA SENHA NOVAMENTE: '''))

                if senha == senha_repete.strip():
                    break #A senha foi inserida corretamente
                else:
                    raise #A senha inserida não é igual a anterior
            except:
                print('''
    ---> A senha inserida não confere com a digitada anteriormente. Por favor, tente novamente.''')
                
        return(senha)