# |=================================================================|
# |                     AVALIAÇÃO PARCIAL 02                        |
# |                                                                 |
# |       UNIVERSIDADE UNOPAR PITÁGORAS ANHANGUERA - CATUAÍ         |
# |         3º SEMESTRE DE ENGENHARIA DA COMPUTAÇÃO - N             |
# |                                                                 |
# |                   DISCIPLINA DE ALGORITMOS E ESTRUTURA DE DADOS |
# |                              DOCENTE: PROFESSOR SANDRO T. PINTO |
# |                                                                 |
# | DISCENTES PARTICIPANTES DESTE TRABALHO AVALIATIVO:              |
# | - MARCOS GABRIEL GEVIGIER                                       |
# | - CARLOS EDUARDO ALVES RICO                                     |
# | - JOÃO VITOR BOAVENRURA AMÂNCIO                                 |
# | - FILIPE ESTEVÃO GOMES DOS SANTOS                               |
# | - DANIEL CARLOS DA SILVA                                        |
# |=================================================================|
# 
# ESTE CÓDIGO UTILIZA A BIBLIOTECA PANDAS!
# PARA INSTALAR, BASTA DIGITAR "pip install pandas" NO TERMINAL PYTHON

# Bibliotecas utilziadas
import pandas as pd                                     # Lidar com .csv
import time                                             # Usado para segurar o código por alguns segundos
from datetime import datetime                           # Usado para pegar a data/hora atual
import pytz                                             # Usado para pegar a data/hora no horário de São Paulo

# Parte do código do sistema
from acesso_db_csv import acesso_db                     # Acessa o "banco de dados" de usuários
from acesso_db_produto_csv import acesso_db_produto     # Acesso o "banco de dados" de produtos
from validacao_info_user import validacao_info          # Solicita e valida info de usuários

class sistemaLoja:
    '''Classe principal que executa todo o programa com suas telas'''
    def __init__(self):
        '''Inicialização'''
        sistemaLoja.telaInicial(self)

    def telaInicial(self):
        '''Tela inicial'''

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

    def telaConfirmacao():
        '''Tela de "Confirmar" e "Cancelar"

        Tela de confirmação para ser usada e reciclada por todo o código'''
        while True:
            opcoes = int(input('''
            [1] Confirmar                    [0] Cancelar
                        '''))

            match opcoes:
                case 1:
                    return True # SIM
                case 0:
                    return False # NÃO
                case _:
                    print('Opção incorreta. Insira um número referente a uma das opções disponíveis.') 

    def telaCadastro(self):
        '''Tela de Cadastro'''
        print('''
        -------------- CADASTRO DE USUÁRIO ------------
        ''')

        nomeUser  = validacao_info.validacaoNome() # Pede e valida nome
        emailUser = validacao_info.validacaoEmail(1) # Pede e valida e-mail (tipo 1 = cadastro)
        senhaUser = validacao_info.validacaoSenha() # Pede e valida senha
        nascUser  = validacao_info.validacaoNascimento() # Pede e valida data de nascimento
        cpfUser   = validacao_info.validacaoCPF() # Pede e valida CPF

        dataCad   = datetime.now(pytz.timezone('America/Sao_Paulo')) # Hora e data do cadastro

        new_user = pd.DataFrame({'Nome':[nomeUser],
        'E-mail':[emailUser],
        'Senha': [senhaUser],
        'Nascimento': [nascUser],
        'CPF': [cpfUser],
        'Data Cadastro': [dataCad],
        'Último Login': ['']})
        # Cria um dataframe com todas as informações do usuário

        if sistemaLoja.telaConfirmacao(): # CONFIRMAR ou CANCELAR
            if acesso_db.cadastrarUser(new_user): # Cadastras usuário
                print('''
---> Cadastro realizado com sucesso.
                
                ''')
                sistemaLoja.telaInicial(self) # Retorna a tela inicial
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self) # Retorna a tela inicial
 
    def telaLogin(self):
        '''Tela de Login'''
        print('''
        -------------- ENTRADA DE USUÁRIO -------------
        ''')

        self.emailLogin   = validacao_info.validacaoEmail(2) # Pergunta e valida e-mail (tipo 2 = login)
        senhaLogin        = str(input('INSIRA SUA SENHA: ')) 

        if sistemaLoja.telaConfirmacao(): # CONFIRMAR ou CANCELAR
                match acesso_db.validarLogin(self, self.emailLogin, senhaLogin): # Valida login
                    case (0) | (1): # 0 = E-mail não encontrado | 1 = Senha incorreta
                        print('''
---> O e-mail ou senha inserido não está correto.
        Por favor, tente novamente''')
                        sistemaLoja.telaLogin(self) # Retorna à tela inicial

                    case 2: # Validação com sucesso
                        print('''
---> Login realizado com sucesso.

                Seja bem-vindo, ''', self.nomeUserLogin,'''!
                ''')
                        
                        acesso_db.registrarLogin(self, self.emailLogin) # Regista data e hora do último login
                        sistemaLoja.telaVenda(self) # Redireciona à tela de venda
        else:
            print('''
                   -x- Operação Cancelada -x-
                  Retornando a tela inicial...
                ''')
            sistemaLoja.telaInicial(self) # Retorna à tela inicial

    def menuVenda(self):
        '''Menu de produtos para tela de venda'''
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
  '''.format(acesso_db_produto.visualizarProduto(self, 0), # 0
             acesso_db_produto.visualizarValor(self, 0),   # 1
             acesso_db_produto.visualizarProduto(self, 1), # 2
             acesso_db_produto.visualizarValor(self, 1),   # 3
             acesso_db_produto.visualizarProduto(self, 2), # 4
             acesso_db_produto.visualizarValor(self, 2)    # 5
             ))

    def telaVenda(self):
        '''Tela de Venda'''
        sistemaLoja.menuVenda(self) # Exibe menu de produtos

        processo_compra = False
        retorno_inicio = False
       
        while True:
            try:
                respVenda = int(input())
                match respVenda:
                    case 0: # Sair
                        print('''
    Ao prosseguir, você será desconectado de sua conta e redirecionado a tela inicial
        ''')
                        if sistemaLoja.telaConfirmacao(): # CONFIRMAR ou CANCELAR
                            retorno_inicio = True
                            # Determina True para retorno e dá break, para que seja redirecionado
                            # por fora, para impedir loop infinito 
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
                            # Determina True para processo de compra e dá break, para que seja redirecionado
                            # por fora, para impedir loop infinito
                            break 
                        else:
                            print('''
        Tudo bem! Você será redirecionado à loja.
                            ''')

                            sistemaLoja.menuVenda(self) # Volta a executar o menu
                    case _:
                        raise

            except:
                print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

        if retorno_inicio:
            sistemaLoja.telaInicial(self) # Caso cancelado, retorna ao inicio

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
                            acesso_db_produto.comprarProduto(self, respVenda-1) # Atualiza os bancos de dados
                            sistemaLoja.telaAgradecimento() # Chama a tela de agradecimento
                            time.sleep(5) # Pausa o programa por 5 segundos
                            break
                        case _:
                            raise
                except:
                    print('Opção incorreta. Insira um número referente a uma das opções disponíveis.')

            sistemaLoja.telaVenda(self) # Retorna à tela de venda

    def telaAgradecimento():
        '''Tela de agradecimento pós compra'''
        print('''
        
        Obrigado por comprar conosco, tenha um ótimo dia :)
        O boleto de seu pedido já foi enviado ao e-mail cadastrado

                >>> Volte sempre! <<<

    ---> Você será redirecionado para à loja...

        ''')

if __name__ == "__main__":
    # Este IF serve para que o código seja executado
    sistema = sistemaLoja()