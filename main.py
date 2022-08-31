from traceback import print_tb
import pyodbc
from random import randint
import pytz
from datetime import datetime

dados_conexao = ("Driver={SQLite3 ODBC Driver}; Server=localhost; Database=bancopoo.db;")

conexao = pyodbc.connect(dados_conexao)

cursor = conexao.cursor()


#cursor.execute(f"INSERT INTO bancodados (Nome, Cpf, Agencia, Numconta, Saldo, limite) VALUES ('thais', '654321', 78956, 123789, 1000, 10000)")

#cursor.commit()


def validacao_login(login, senha):
         
        cursor.execute(f"SELECT Cpf FROM bancodados WHERE Cpf = '{login}'")
        cpf_login = cursor.fetchall()
            
        cursor.execute(f"SELECT Senha FROM bancodados WHERE Senha = '{senha}'")
        senha_login = cursor.fetchall()
            
        
        return cpf_login, senha_login




class BancoPoo:
    
    @staticmethod      
           
    def _gerar_numero_conta():  
        '''
        Função que gera um número de 6 digitos, sendo que cada digito pode ser de 1 até 9.
        
        Não exige nenhum parâmetro.
        
        Retorna uma variavel com um número de 6 digitos aleatórios cada vez que é executada.
        
        '''
        num_conta= ''

        for i in range(5):
            num_conta += str(randint(1,9))
        
        return num_conta
    
    
    def _data_hora():
        '''
        Função que entrega de forma formatada o horário atual, levando em conta o fuso horário de Braisilia - DF (dias/meses/anos  horas:minutos:segundos)
        
        Não exige nenhum parâmetro.
        
        Retorna uma variável com o horário formatado em que a função foi rodada.
        
        '''
        fuso_brazil = pytz.timezone('Brazil/East') #horario de brasilia
        horario_brazil = datetime.now(fuso_brazil)
        
        return horario_brazil.strftime('%d/%m/%Y  %H:%M:%S')
    
    
    
    def __init__(self, nome, cpf, senha):
        self._nome = nome
        self._cpf = cpf
        self._agencia = str(self._gerar_numero_conta())
        self._num_conta = str(self._gerar_numero_conta())
        self._saldo = 0
        self._limite = 5000
        self._senha = senha
        self.validacao = 0
        
        cursor.execute(f"INSERT INTO bancodados (Nome, Cpf, Agencia, Numconta, Saldo, limite, Senha, Validacao) VALUES ('{self._nome}', '{self._cpf}', '{self._agencia}', '{self._num_conta}', {self._saldo}, {self._limite}, '{self._senha}', {self.validacao} )")
        
        
    def Saque(self, cpf, senha, valor):
        if self._limite > (self._saldo - valor):
            self._saldo -= valor
            transacoes = f'SACADO R$ {valor:,.2f}, O saldo é de R$ {self._saldo:,.2f}, {self._data_hora()}'
            
            cursor.execute(f"INSERT INTO Extrato (Conta, Transacao) VALUES ('{self._num_conta}', '{transacoes}')")
            
        else:
            print(f'Você não pode sacar mais que seu limite! Seu limite é de R$ {self._limite:,.2f}')
        
        
            


while True:

    print(' ____________________________________')

    print('|           BANCO - POO              |')

    print('|____________________________________|') 

    print('|PRESSIONE 1 PARA LOGIN              |')

    print('|PRESSIONE 2 PARA CADASTRAR CLIENTE  |')

    print('|PRESSIONE 3 PARA CONSULTAR SALDO    |')

    print('|PRESSIONE 4 PARA TRANSFERÊNCIAS     |')

    print('|PRESSIONE 5 PARA DEPÓSITOS          |')

    print('|PRESSIONE 0 PARA SAIR DO SISTEMA    |')

    print('|____________________________________|')
          

    opc = int(input('>> '))
    
    if opc == 0:  
        
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
            
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN! Caso não tenha uma conta, acesse a opção CADASTRAR CLIENTE')
            break
            
        
        else:
            validacao_login(login,senha)
                        
            dados_login = validacao_login(login,senha)
                    
            if dados_login[0] == [] or dados_login[1] == []:
                print('\nCPF ou Senha Incorretos!')
                
            
                        
            else:
                print('Saindo do sistema!')             
                cursor.execute(f"UPDATE bancodados SET Validacao = 0  WHERE Cpf = '{login}'")
                cursor.commit()
                cursor.close()
                conexao.close()
                break
    
    if opc == 1:
            
            login = input('Digite seu CPF (com pontos e traço): ')
            senha = input('Digite sua Senha (8 Digítos): ')
            
            cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
            valid_acesso = cursor.fetchall()
            
            if valid_acesso[0][0] == 1:
                print('\nVocê já está logado')    
            
            else:  
                validacao_login(login,senha)
                    
                dados_login = validacao_login(login,senha)
                
                if dados_login[0] == [] or dados_login[1] == []:
                    print('\nCPF ou Senha Incorretos!')
                    
                else:
                    cursor.execute(f"UPDATE bancodados SET Validacao = 1  WHERE Cpf = '{login}'")
                    cursor.commit()
                    
                    cursor.execute(f"SELECT Nome FROM bancodados WHERE Cpf = '{login}'")
                    nome_bem_vindo = cursor.fetchall()
                    print(f'\nAcesso liberado! Seja bem vindo(a) {nome_bem_vindo[0][0]}')
                    
    
    if opc == 2:
        
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
            
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN! Caso não tenha uma conta, acesse a opção CADASTRAR CLIENTE')
            break
            
        if valid_acesso[0][0] == 1:
            print('\nVocê Já está logado')
            
        
        else:
            
            validacao_login(login,senha)
                        
            dados_login = validacao_login(login,senha)
                    
            if dados_login[0] == [] or dados_login[1] == []:
                print('\nCPF ou Senha Incorretos!')
        
            else:
                while True:    
                    nome = input('Digite seu Nome: ')
                    nome.upper() 
                    nome.strip()
                    if not nome.isalpha():
                        print('Somente Letras!')
                            
                    else: 
                        cpf = input('Digite seu CPF (com pontos e traço): ')
                        if not '-' in cpf or not '.' in cpf:
                            print('O CPF deve ter "-" e "." !')
                            
                        else:
                            senha_creat = input('Digite sua Senha (8 Digítos): ')
                                
                            if len(senha_creat) < 8 or len(senha_creat) > 8:
                                print('A Senha deve conter 8 dígitos')
                                    
                            else:
                                conta = BancoPoo(nome, cpf, senha_creat)
                                print('Cadastro efetuado com sucesso!')
                                break
                        
    
    if opc == 3:
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
            
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN! Caso não tenha uma conta, acesse a opção CADASTRAR CLIENTE\n')
            break
    
    
        else:
            cursor.execute(f"SELECT Saldo FROM bancodados  WHERE Cpf = '{login}'")
            saldo = cursor.fetchall()
            
            print(f'Seu saldo é de R$ {saldo[0][0]:,.2f}')
    
    
    if opc == 3:
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
            
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN! Caso não tenha uma conta, acesse a opção CADASTRAR CLIENTE\n')
            break
    
    
        else:
            cursor.execute(f"SELECT Saldo FROM bancodados  WHERE Cpf = '{login}'")
            saldo = cursor.fetchall()
            
            print(f'Seu saldo é de R$ {saldo[0][0]:,.2f}')    
                
                        
           
    else:
        print('Digite uma das opções acima!')
    
        
        
        
            
            
            
            
            

        




