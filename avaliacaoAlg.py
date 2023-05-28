import pandas as pd             #Lidar com .csv
import os                       #Verificar a existência dos .csv
import re                       #Regex -> validar e-mail
import time                     #Usado para segurar o código por alguns segundos
from datetime import datetime   #Usado para pegar a data/hora atual
import pytz                     #Usado para pegar a data/hora no horário de São Paulo
import uuid                     #Gera um ID aleatório para as vendas
import string                   #Usado para validar senha

class acesso_db: #Classe responsável por interagir com o .csv de "banco de dados" de usuários
    def existencia_db(): #Verifica se existe o .csv e retorna como True ou False
        if (os.path.isfile('./user_db.csv')) is True:
            return True
        else:
            return False

    def cadastrarUser(new_user_entry): #Escreve o dataframe de usuário em .csv de acordo com existencia_db()
        if acesso_db.existencia_db(): 
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=False, sep=';')
        else:
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=True, sep=';')

        return True

    def validarLogin(self, email_login, senha_login): #Lê o .csv e verifica se o e-mail e senha inserido estão cadastrados
        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv', sep = ';')

            for email in user_db.loc[:,"E-mail"]: #Itera dentro da coluna de e-mail
                if email == email_login: #Verifica se o e-mail inserido está cadastado
                    index = int(''.join(filter(str.isdigit, str(user_db.index[user_db['E-mail']==email_login].tolist()))))
                    senha_db = str(user_db.at[index,"Senha"])
                    if str(senha_login) == senha_db: #Verifica se a senha inserida está correta
                        self.nomeUserLogin = user_db.at[index,"Nome"]
                        return 2 #Autenficado com sucesso
                    else:
                        return 1 #Senha incorreta
            return 0 #E-mail não encontrado
        
        else: 
            return 0 #Se não existir ainda o .csv, apenas retorna como "e-mail não encontrado"

    def verificarCadEmail(email_teste): #Verifica se o e-mail inserido não está previamente cadastrado
        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv', sep = ';')
  
            for email in user_db.loc[:,"E-mail"]:
                if email == email_teste:
                    return False #Este e-mail já está cadastrado
        return True #Este e-email não está cadastrado

    def registrarLogin(self, email_login): #Atualiza o .csv de cadastro inserindo a data e hora do último login
        user_db = pd.read_csv('./user_db.csv', sep = ';') #Lê a base de dados existente
        os.remove('./user_db.csv') #Apaga base de dados já existente no diretório

        for email in user_db.loc[:,"E-mail"]: #Itera dentro da coluna de e-mail
            index = int(''.join(filter(str.isdigit, str(user_db.index[user_db['E-mail']==email_login].tolist()))))

        dataLogin   = datetime.now(pytz.timezone('America/Sao_Paulo'))
        user_db.loc[index, ['Último Login']] = dataLogin #Insere a data e hora atual no dataframe

        user_db.to_csv('./user_db.csv', mode='a', index=False, header=True, sep=';') #Escreve o dataframe em .csv

class acesso_db_produto: #Classe responsável por interagir com o .csv de "banco de dados" de produtos
    def existencia_db_loja(): #Verifica se existe o .csv e retorna como True ou False
        if (os.path.isfile('./product_db.csv')) is True:
            return True #Já existe o banco de dados
        else:
            return False #Não existe o banco de dados

    def acessar_db(self): #Acessa o .csv ou cria um novo dataframe, conforme necessário
        if acesso_db_produto.existencia_db_loja(): 
            product_db = pd.read_csv('./product_db.csv', sep = ';')
        else:
            # Cria um dataframe para ser usado de banco de dados.
            # Sei que não é correto, mas gostaria de evitar que fosse enviado vários arquivos para o professor.
            product_db = pd.DataFrame({'Produto':['Notebook', 'Monitor', 'Teclado'],
            'Valor':['4000,00', '1200,00', '500,00'],
            'Quantidade': ['27', '53', '42']})

        return(product_db) #Retorna um dataframe (um criado ou o .csv lido)

    def visualizarProduto(self, ver_produto): #Retira o nome do produto de acordo com o índice pedido
        db_produto = acesso_db_produto.acessar_db(self) #Pega o "banco de dados"

        todos_produto = ''
        for produto in db_produto.loc[:,"Produto"]: #Itera dentro da coluna produtos
            todos_produto = todos_produto + produto + ";" #Monta uma string com todos os produtos
        
        lista_produto = todos_produto.split(';') #Separa a string em uma lista

        match ver_produto: #Envia apenas o nome do produto solicitado (de acordo com o índice da lista)
            case 0:
                return lista_produto[0]
            case 1:
                return lista_produto[1]
            case 2:
                return lista_produto[2]

    def visualizarValor(self, ver_valor): #Retira o valor do produto de acordo com o produto de visualizarProduto()
        db_produto = acesso_db_produto.acessar_db(self) #Pega o "banco de dados"

        for produto in db_produto.loc[:,"Produto"]: #Itera dentro da coluna de produtos
            index = int(''.join(filter(str.isdigit, str(db_produto.index[db_produto['Produto']==acesso_db_produto.visualizarProduto(self, ver_valor)].tolist()))))
            valor_db = str(db_produto.at[index,"Valor"])

            return(valor_db) #Retorna o valor do produto que foi pedido pela variável "ver_valor" e que teve seu nome retirado de visualizarProduto()

    def comprarProduto(self, produto_escolhido): #Realiza a compra do produto
        db_produto = acesso_db_produto.acessar_db(self) #Pega o "banco de dados"

        for produto in db_produto.loc[:,"Produto"]: #Itera dentro da coluna de produtos
            index = int(''.join(filter(str.isdigit, str(db_produto.index[db_produto['Produto']==acesso_db_produto.visualizarProduto(self, produto_escolhido)].tolist()))))
            quantidade_anterior = int(db_produto.at[index,"Quantidade"]) #Salva a quantidae anterior

        db_produto.loc[index, ['Quantidade']] = quantidade_anterior-1 #Atualiza o "banco de dados" com a nova quantidade (1 a menos)
        
        if acesso_db_produto.existencia_db_loja():
            os.remove('./product_db.csv') #Apaga base de dados já existente no diretório

        db_produto.to_csv('./product_db.csv', mode='a', index=False, header=True, sep=';') #Salva o dataframe em .csv com a quantidade nova

        acesso_db_produto.registrarVenda(self, produto_escolhido) #Registra a venda em outro .csv

    def registrarVenda(self, produto_venda):
        self.id_venda = uuid.uuid1() #Gera um ID aleatório
        dataCompra    = datetime.now(pytz.timezone('America/Sao_Paulo')) #Pega a data e hora da compra

        sells_db = pd.DataFrame({'Usuário': [self.emailLogin],
        'Pedido':[acesso_db_produto.visualizarProduto(self, produto_venda)],
        'ID':[self.id_venda],
        'Data Venda': [dataCompra]})
        #Cria um dataframe para ser transformado em .csv

        if (os.path.isfile('./sells_db.csv')) is True: #Já existe o banco de dados
            sells_db.to_csv('./sells_db.csv', mode='a', index=False, header=False, sep=';') #Escreve adicionando linhas
        else: #Não existe o banco de dados
            sells_db.to_csv('./sells_db.csv', mode='a', index=False, header=True, sep=';') #Escreve do zero, com cabeçalhos

class validacao_info: #Classe responsável por verificar se os dados inseridos no momento do cadastro estão corretos
    def validacaoNome(): #Solicita um nome e não retorna até que seja preenchido (não pode estar vazio)
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
                
        return(nome)

    def validacaoEmail(tipo): #Valida se foi inserido um e-mail (cadastro e login)
        while True:
            if tipo == 1:      #CADASTRO
                emailtestador   = str(input('INSIRA UM E-MAIL: '))
            elif tipo == 2:    #LOGIN
                emailtestador   = str(input('INSIRA SEU E-MAIL: '))
            
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

    def validacaoCPF(): #Solicita um CPF e verifica se é um número de CPF válido
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
        
    def validacaoNascimento(): #Solicita e verifica se a data de nascimento foi inserida corretamente
        while True:
            nascimento = str(input('DATA DE NASCIMENTO (dd/mm/aaaa): '))

            try:
                dataSep = datetime.strptime(nascimento, "%d/%m/%Y")
                break
            except:
                print('''
                ---> Houve algum erro ao cadastrar sua data de nascimento.
    Por favor, escreva no formato dd/mm/aaaa
    (separado por '/' -> Exemplo: 01/02/2000)
    ''')
                
        return(dataSep)

    def validacaoSenha(): #Solicita uma senha e valida se possui os requisitos mínimos necessários

        while True:
            l, u, p, d = 0, 0, 0, 0

            senha = str(input('''
            DIGITE SUA SENHA 
(REQUISITOS: mín. de : 8 caracteres / 1 maiúscula / 1 minúscula / 1 número / 1 caractere especial): '''))

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

                if senha == senha_repete:
                    break #A senha foi inserida corretamente
                else:
                    raise #A senha inserida não é igual a anterior
            except:
                print('''
    ---> A senha inserida não confere com a digitada anteriormente. Por favor, tente novamente.''')
                
        return(senha)

class sistemaLoja: #Classe principal que executa todo o programa com suas telas
    def __init__(self): #Inicialização
        # Inicialização
        sistemaLoja.telaInicial(self)

    def telaInicial(self): #Tela inicial

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
                        break
                    case 2:
                        sistemaLoja.telaCadastro(self)
                        break
                    case _:
                        raise
            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

    def telaConfirmacao(): #Tela de "Confirmar" e "Cancelar"
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

    def telaCadastro(self): #Tela de cadastro
        # Tela de Cadastro
        print('''
        -------------- CADASTRO DE USUÁRIO ------------
        ''')

        nomeUser = validacao_info.validacaoNome() #Pede e valida nome
        emailUser = validacao_info.validacaoEmail(1) #Pede e valida e-mail (tipo 1 = cadastro)
        senhaUser = validacao_info.validacaoSenha() #Pede e valida senha
        nascUser  = validacao_info.validacaoNascimento() #Pede e valida data de nascimento
        cpfUser   = validacao_info.validacaoCPF() #Pede e valida CPF

        dataCad   = datetime.now(pytz.timezone('America/Sao_Paulo')) #Hora e data do cadastro

        new_user = pd.DataFrame({'Nome':[nomeUser],
        'E-mail':[emailUser],
        'Senha': [senhaUser],
        'Nascimento': [nascUser],
        'CPF': [cpfUser],
        'Data Cadastro': [dataCad],
        'Último Login': ['']})
        # Cria um dataframe com todas as informações do usuário

        if sistemaLoja.telaConfirmacao() == 1: #CONFIRMAR ou CANCELAR
            if acesso_db.cadastrarUser(new_user): #Cadastras usuário
                print('''
---> Cadastro realizado com sucesso.
                
                ''')
                sistemaLoja.telaInicial(self) #Retorna a tela inicial
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self) #Retorna a tela inicial
 
    def telaLogin(self): #Tela de Login
        # Tela de Login
        print('''
        -------------- ENTRADA DE USUÁRIO -------------
        ''')

        self.emailLogin   = validacao_info.validacaoEmail(2) #Pergunta e valida e-mail (tipo 2 = login)
        senhaLogin        = str(input('INSIRA SUA SENHA: ')) 

        if sistemaLoja.telaConfirmacao() == 1: #CONFIRMAR ou CANCELAR
                match acesso_db.validarLogin(self, self.emailLogin, senhaLogin): #Valida login
                    case (0) | (1): #0 = E-mail não encontrado | 1 = Senha incorreta
                        print('''
---> O e-mail ou senha inserido não está correto.
        Por favor, tente novamente''')
                        sistemaLoja.telaLogin(self) #Retorna à tela inicial

                    case 2: #Validação com sucesso
                        print('''
---> Login realizado com sucesso.

                Seja bem-vindo, ''', self.nomeUserLogin,'''!
                ''')
                        
                        acesso_db.registrarLogin(self, self.emailLogin) #Regista data e hora do último login
                        sistemaLoja.telaVenda(self) #Redireciona à tela de venda
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self) #Retorna à tela inicial

    def menuVenda(self): #Menu de produtos para tela de venda
        print('''
        ===x===x===x===x===x===x===x===x===x===x===x===
              A LOJA DO PROGRAMADOR - ANHANGUERA
        ===x===x===x===x===x===x===x===x===x===x===x===
        
|----------------      |----------------      |----------------   
|               |      |               |      |               |
|               |      |               |      |               |
|    {0}   |      |    {2}    |      |    {4}    |
|               |      |               |      |               |
|               |      |               |      |               |
----------------|      ----------------|      ----------------|
R$ {1}                R$ {3}                 R$ {5}


    Escolha uma opção:
  [1] Comprar "{0}"       [2] Comprar "{2}"
  [3] Comprar "{4}"        [0] Sair
  '''.format(acesso_db_produto.visualizarProduto(self, 0), #0
             acesso_db_produto.visualizarValor(self, 0),   #1
             acesso_db_produto.visualizarProduto(self, 1), #2
             acesso_db_produto.visualizarValor(self, 1),   #3
             acesso_db_produto.visualizarProduto(self, 2), #4
             acesso_db_produto.visualizarValor(self, 2)    #5
             ))

    def telaVenda(self): #Tela de Venda
        sistemaLoja.menuVenda(self) #Exibe menu de produtos

        processo_compra = False
        retorno_inicio = False
       
        while True:
            try:
                respVenda = int(input())
                match respVenda:
                    case 0: #Sair
                        print('''
    Ao prosseguir, você será desconectado de sua conta e redirecionado a tela inicial
        ''')
                        if sistemaLoja.telaConfirmacao() == 1: #CONFIRMAR ou CANCELAR
                            retorno_inicio = True
                            #Determina True para retorno e dá break, para que seja redirecionado
                            #por fora, para impedir loop infinito 
                            break
                        else:
                            print('''
        Perfeito! Adoramos sua presença aqui :)
        
        ''') 
                            sistemaLoja.menuVenda(self)
                    case (1) | (2) | (3):
                        print('------> Você deseja comprar: {0}?'.format(acesso_db_produto.visualizarProduto(self, respVenda-1)))

                        if sistemaLoja.telaConfirmacao():
                            processo_compra = True
                            #Determina True para processo de compra e dá break, para que seja redirecionado
                            #por fora, para impedir loop infinito
                            break 
                        else:
                            print('''
        Tudo bem! Você será redirecionado à loja.
                            ''')

                            sistemaLoja.menuVenda(self) #Volta a executar o menu
                    case _:
                        raise

            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

        if retorno_inicio:
            sistemaLoja.telaInicial(self) #Caso cancelado, retorna ao inicio

        if processo_compra:
            print('''
        Qual a forma de pagamento?
        [1] Boleto                       [0] Cancelar
        ''')

            while True:
                try:
                    respPagamento = int(input())
                    match respPagamento:
                        case 0:
                            break
                        case 1:
                            acesso_db_produto.comprarProduto(self, respVenda-1) #Atualiza os bancos de dados
                            sistemaLoja.telaAgradecimento() #Chama a tela de agradecimento
                            time.sleep(5) #Pausa o programa por 5 segundos
                            break
                        case _:
                            raise
                except:
                    print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

            sistemaLoja.telaVenda(self) #Retorna à tela de venda

    def telaAgradecimento(): #Tela de agradecimento pós compra
        print('''
        
        Obrigado por comprar conosco, tenha um ótimo dia :)
        O boleto de seu pedido já foi enviado ao e-mail cadastrado

                >>> Volte sempre! <<<

    ---> Você será redirecionado para à loja...

        ''')

if __name__ == "__main__":
    # Este IF serve para que o código seja executado
    sistema = sistemaLoja()