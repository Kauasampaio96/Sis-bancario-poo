import sys
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
        self.nome = nome
        self.cpf = cpf
        self.agencia = str(self._gerar_numero_conta())
        self.num_conta = str(self._gerar_numero_conta())
        self._saldo = 0
        self._limite = 5000
        self._senha = senha
        self.validacao = 0
        
        cursor.execute(f"INSERT INTO bancodados (Nome, Cpf, Agencia, Numconta, Saldo, limite, Senha, Validacao) VALUES ('{self.nome}', '{self.cpf}', '{self.agencia}', '{self.num_conta}', {self._saldo}, {self._limite}, '{self._senha}', {self.validacao} )")
        
        cursor.commit()
        
        
    def Saque(self, cpf, senha, valor):
        if self._limite > (self._saldo - valor):
            self._saldo -= valor
            transacoes = f'SACADO R$ {valor:,.2f}, O saldo é de R$ {self._saldo:,.2f}, {self._data_hora()}'
            
            cursor.execute(f"INSERT INTO Extrato (Conta, Transacao) VALUES ('{self.num_conta}', '{transacoes}')")
            
        else:
            print(f'Você não pode sacar mais que seu limite! Seu limite é de R$ {self._limite:,.2f}')
        
        
            


while True:

    print(' ______________________________________________')

    print('|           BANCO - POO                        |')

    print('|______________________________________________|') 

    print('|PRESSIONE 1 PARA LOGIN                        |')

    print('|PRESSIONE 2 PARA CADASTRAR CLIENTE            |')

    print('|PRESSIONE 3 PARA CONSULTAR SALDO              |')

    print('|PRESSIONE 4 P/ CONSULTA DE DADOS DA CONTA     |')
    
    print('|PRESSIONE 5 PARA TRANSFERÊNCIAS               |')

    print('|PRESSIONE 6 PARA DEPÓSITOS                    |')

    print('|PRESSIONE 0 PARA SAIR DO SISTEMA              |')

    print('|______________________________________________|')
          

    opc = int(input('>> '))
    
    if opc == 0:  
        login = input('Para sair do Sistema informe seu CPF: ') 
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
            
            elif valid_acesso == []:
                print('\nCpf ou Senha Incorretos. Confira os dados ou faça Login!')
            
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
            print('\nCpf ou Senha Incorretos. Confira os dados ou faça Login!') 
            
        
        else:       
            while True:    
                nome = input('Digite o nome do Titular da conta: ')
                nome.upper() 
                nome.strip()
                if not nome.isalpha():
                    print('Somente Letras!')
                            
                else: 
                    cpf = input('Digite seu CPF (com pontos e traço): ')
                    if not '-' in cpf or not '.' in cpf:
                        print('O CPF deve ter "-" e "." !')
                        
                    cursor.execute(f"SELECT Cpf FROM bancodados WHERE Cpf = '{cpf}'")
                    cpf_validacao = cursor.fetchall()
                    
                    if cpf_validacao == []:
                        
                        senha_creat = input('Digite sua Senha (8 Digítos): ')
                                
                        if len(senha_creat) < 8 or len(senha_creat) > 8:
                            print('A Senha deve conter 8 dígitos')
                                    
                        else:
                            conta = BancoPoo(nome, cpf, senha_creat)
                            print('Cadastro efetuado com sucesso!')
                            break
                            
                    elif cpf_validacao[0][0] == cpf:
                        print('Esse CPF já está cadastrado no sistema')
                        
                        
    
    if opc == 3:
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
            
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN!\n')
    
    
        else:
            cursor.execute(f"SELECT Saldo FROM bancodados  WHERE Cpf = '{login}'")
            saldo = cursor.fetchall()
            
            print(f'Seu saldo é de R$ {saldo[0][0]:,.2f}')
            

    
     
    if opc == 4:
        login = input('Digite seu CPF (com pontos e traço): ')
        senha = input('Digite sua Senha (8 Digítos): ')
        
        cursor.execute(f"SELECT Validacao FROM bancodados WHERE Cpf = '{login}'")
        valid_acesso = cursor.fetchall()
        if valid_acesso[0][0] == 0:
            print('\nVocê Precisa fazer LOGIN!\n')
    
    
        else:
            cursor.execute(f"SELECT Nome, Agencia, Numconta, Senha FROM bancodados  WHERE Cpf = '{login}'")
            dados_conta = cursor.fetchall()
               
            print('\n----DADOS DA CONTA----\n')
            print(f'Nome = {dados_conta[0][0]}')
            print(f'Agencia = {dados_conta[0][1]}')
            print(f'Numero da Conta = {dados_conta[0][2]}')
            print(f'Senha = {dados_conta[0][3]}')
    
    
        
        
        
            
            
            
            
            

        




