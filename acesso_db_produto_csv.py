# CÓDIGO QUE INTERAGE COM O "BANCO DE DADOS" DE PRODUTOS (EM .CSV)

import pandas as pd             # Lidar com .csv
import os                       # Verificar a existência dos .csv
from datetime import datetime   # Usado para pegar a data/hora atual
import pytz                     # Usado para pegar a data/hora no horário de São Paulo
import uuid                     # Gera um ID aleatório para as vendas

class acesso_db_produto:
    '''Classe responsável por interagir com o .csv de "banco de dados" de produtos'''
    def existencia_db_loja(): # Verifica se existe o .csv e retorna como True ou False
        if (os.path.isfile('./product_db.csv')) is True:
            return True # Já existe o banco de dados
        else:
            return False # Não existe o banco de dados

    def acessar_db(self):
        '''Acessa o .csv ou cria um novo dataframe, conforme necessário'''
        if acesso_db_produto.existencia_db_loja(): 
            product_db = pd.read_csv('./product_db.csv')
        else:
            pass
            # Aqui, caberia levantar um erro de acesso,
            # mas não foi implementado

            # Para fins de teste, eu fiz o seguinte:
            # Cria um dataframe para ser usado de banco de dados.
            # Sei que não é correto, mas gostaria de evitar que fosse enviado vários arquivos para o professor.
            # product_db = pd.DataFrame({'Produto':['Notebook', 'Monitor', 'Teclado'],
            # 'Valor':['4000,00', '1200,00', '500,00'],
            # 'Quantidade': ['27', '53', '42']})

        return(product_db) # Retorna um dataframe (um criado ou o .csv lido)

    def visualizarProduto(self, ver_produto):
        '''Retira o nome do produto de acordo com o índice pedido'''
        db_produto = acesso_db_produto.acessar_db(self) # Pega o "banco de dados"

        todos_produto = ''
        for produto in db_produto.loc[:,"Produto"]: # Itera dentro da coluna produtos
            todos_produto = todos_produto + produto + ";" # Monta uma string com todos os produtos
        
        lista_produto = todos_produto.split(';') # Separa a string em uma lista

        match ver_produto: # Envia apenas o nome do produto solicitado (de acordo com o índice da lista)
            case 0:
                return lista_produto[0]
            case 1:
                return lista_produto[1]
            case 2:
                return lista_produto[2]

    def visualizarValor(self, ver_valor):
        '''Retira o valor do produto de acordo com o produto de visualizarProduto()'''
        db_produto = acesso_db_produto.acessar_db(self) # Pega o "banco de dados"

        for produto in db_produto.loc[:,"Produto"]: # Itera dentro da coluna de produtos
            index = int(''.join(filter(str.isdigit, str(db_produto.index[db_produto['Produto']==acesso_db_produto.visualizarProduto(self, ver_valor)].tolist()))))
            valor_db = str(db_produto.at[index,"Valor"])

            return(valor_db) # Retorna o valor do produto que foi pedido pela variável "ver_valor" e que teve seu nome retirado de visualizarProduto()

    def comprarProduto(self, produto_escolhido):
        '''Realiza a compra do produto'''
        db_produto = acesso_db_produto.acessar_db(self) # Pega o "banco de dados"

        for produto in db_produto.loc[:,"Produto"]: # Itera dentro da coluna de produtos
            index = int(''.join(filter(str.isdigit, str(db_produto.index[db_produto['Produto']==acesso_db_produto.visualizarProduto(self, produto_escolhido)].tolist()))))
            quantidade_anterior = int(db_produto.at[index,"Quantidade"]) # Salva a quantidae anterior

        db_produto.loc[index, ['Quantidade']] = quantidade_anterior-1 # Atualiza o "banco de dados" com a nova quantidade (1 a menos)
        
        if acesso_db_produto.existencia_db_loja():
            os.remove('./product_db.csv') # Apaga base de dados já existente no diretório

        db_produto.to_csv('./product_db.csv', mode='a', index=False, header=True) # Salva o dataframe em .csv com a quantidade nova

        acesso_db_produto.registrarVenda(self, produto_escolhido) # Registra a venda em outro .csv

    def registrarVenda(self, produto_venda):
        '''Escreve um dataframe com a compra e registra no "banco de dados" sells_db.csv'''
        self.id_venda = uuid.uuid1() # Gera um ID aleatório
        dataCompra    = datetime.now(pytz.timezone('America/Sao_Paulo')) # Pega a data e hora da compra

        sells_db = pd.DataFrame({'Usuário': [self.emailLogin],
        'Pedido':[acesso_db_produto.visualizarProduto(self, produto_venda)],
        'ID':[self.id_venda],
        'Data Venda': [dataCompra]})
        # Cria um dataframe para ser transformado em .csv

        if (os.path.isfile('./sells_db.csv')) is True: # Já existe o banco de dados
            sells_db.to_csv('./sells_db.csv', mode='a', index=False, header=False) # Escreve adicionando linhas
        else: # Não existe o banco de dados
            sells_db.to_csv('./sells_db.csv', mode='a', index=False, header=True) # Escreve do zero, com cabeçalhos