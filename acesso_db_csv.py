# CÓDIGO QUE INTERAGE COM O "BANCO DE DADOS" DE USUÁRIOS (EM .CSV)

import pandas as pd             # Lidar com .csv
import os                       # Verificar a existência dos .csv
from datetime import datetime   # Usado para pegar a data/hora atual
import pytz                     # Usado para pegar a data/hora no horário de São Paulo

class acesso_db:
    '''Classe responsável por interagir com o .csv de "banco de dados" de usuários'''
    def existencia_db():
        '''Verifica se existe o .csv e retorna como True ou False'''
        if (os.path.isfile('./user_db.csv')) is True:
            return True
        else:
            return False

    def cadastrarUser(new_user_entry):
        '''Escreve o dataframe de usuário em .csv de acordo com existencia_db()'''
        if acesso_db.existencia_db(): 
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=False)
        else:
            new_user_entry.to_csv('./user_db.csv', mode='a', index=False, header=True)

        return True

    def validarLogin(self, email_login, senha_login):
        '''Lê o .csv e verifica se o e-mail e senha inserido estão cadastrados'''
        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv')

            for email in user_db.loc[:,"E-mail"]: # Itera dentro da coluna de e-mail
                if email == email_login: # Verifica se o e-mail inserido está cadastado
                    index = int(''.join(filter(str.isdigit, str(user_db.index[user_db['E-mail']==email_login].tolist()))))
                    senha_db = str(user_db.at[index,"Senha"])
                    if str(senha_login) == senha_db: # Verifica se a senha inserida está correta
                        self.nomeUserLogin = user_db.at[index,"Nome"]
                        return 2 # Autenficado com sucesso
                    else:
                        return 1 # Senha incorreta
            return 0 # E-mail não encontrado
        
        else: 
            return 0 # Se não existir ainda o .csv, apenas retorna como "e-mail não encontrado"

    def verificarCadEmail(email_teste):
        '''Verifica se o e-mail inserido não está previamente cadastrado'''
        if acesso_db.existencia_db(): 
            user_db = pd.read_csv('./user_db.csv')
  
            for email in user_db.loc[:,"E-mail"]:
                if email == email_teste:
                    return False # Este e-mail já está cadastrado
        return True # Este e-email não está cadastrado

    def registrarLogin(self, email_login):
        '''Atualiza o .csv de cadastro inserindo a data e hora do último login'''
        user_db = pd.read_csv('./user_db.csv') # Lê a base de dados existente
        os.remove('./user_db.csv') # Apaga base de dados já existente no diretório

        for email in user_db.loc[:,"E-mail"]: # Itera dentro da coluna de e-mail
            index = int(''.join(filter(str.isdigit, str(user_db.index[user_db['E-mail']==email_login].tolist()))))

        dataLogin   = datetime.now(pytz.timezone('America/Sao_Paulo'))
        user_db.loc[index, ['Último Login']] = dataLogin # Insere a data e hora atual no dataframe

        user_db.to_csv('./user_db.csv', mode='a', index=False, header=True) # Escreve o dataframe em .csv