#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
from termcolor import colored
import sys
import pandas as pd
import math
from os.path import exists as file_exists
from tkinter import *
import select
import interface
import tkinter as tk

connection = None
cursor = None

def config(filename='database.ini', section='postgresql'):
	parser = ConfigParser()
	parser.read(filename)
 
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
	return db

def connect():
	global connection, cursor

	try:
		params = config()
 
		print('Connecting to the PostgreSQL database...')
		connection = psycopg2.connect(**params)
		connection.autocommit = True
	  
		cursor = connection.cursor()
		
		#print('PostgreSQL database version:')
		cursor.execute('SELECT version()')
 
		db_version = cursor.fetchone()
		print(db_version)

		print('Conectado com sucesso!\n')
	   
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		sys.exit()

def run_script_sql(filename):
	global connection, cursor

	file = open(filename, 'r', encoding='utf-8')
	sql = file.read()
	file.close()

	#text = colored('Executando ' + filename, 'cyan')
	#print (text)

	commands = sql.split(';')
	
	error_count = 0
	for command in commands[:-1]:
		if (len(command)>0):
			command = command + ';'
			try:
				cursor.execute(command)
			except(Exception, psycopg2.DatabaseError) as error:
				error_count+=1
				print(colored(str(error)),'red')
	
	if error_count == 0:
		return True
	else:
		return False

def insert_sql(table, values):
	global connection, cursor

	if values[0] == 'x' or values[0] == 'X': # checa a primeira coluna, que indica se a linha não deve ser inserida
		#text = colored('IGNORADA', 'yellow', attrs=['reverse', 'blink'])
		#print(text)
		return -1
	else:
		values_content = ""
		for index, value in enumerate(values):
			#print('Valor inserido: ' + str(value) + ' >>> ' + str(type(value)))
			if index != 0: # pula o primeiro campo, que é dedicado a coluna de "excluir"
				if index < len(values)-1:
					if type(value) is str:
						values_content += "'" + str(value) + "'" + ","
					elif math.isnan(value):
						values_content += "null,"
					else:
						values_content += str(int(value)) + ","
				else:
					if type(value) is str:
						values_content += "'" + str(value) + "'"
					elif math.isnan(value):
						values_content += "null"
					else:
						values_content += str(int(value))

		query = "INSERT INTO " + table + " VALUES (" + values_content + ");"

		try:
			cursor.execute(query)
			#text = colored('SUCESSO!', 'blue', attrs=['reverse', 'blink'])
			#print(text + query)
			result = 1

		except Exception as error:
			print('QUERY: '+ query)
			text = colored('ERRO:', 'red', attrs=['reverse', 'blink'])
			print(text + ' ' + str(error) + '\n')
			result = 0

		return result

def insert_table(tablename, filename):
	global connection, cursor
	sucess_counter = 0
	error_counter = 0

	tablename = tablename.lower()

	if file_exists(filename) == False:
		print( 'Tabela ' + tablename + ' >> ' ' arquivo não encontrado ')
		return 0

	data = pd.read_csv(filename)
	df = pd.DataFrame(data)
	#print(df)

	query = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = '" + tablename + "');"
	cursor.execute(query)
	if cursor.fetchone()[0] == True:
		for index, row in df.iterrows():
			result = insert_sql(tablename,row)
			if result == 1:
				sucess_counter += 1
			elif result == 0:
				error_counter += 1
		print( 'Tabela ' + tablename + ' >> ' + str(sucess_counter) + ' inserções bem sucedidas  / ' + str(error_counter) + ' erros de inserção')
	else:
		print( 'Tabela ' + tablename + ' >> ' ' erro ao acessar ')
		return 0

	if error_counter == 0:
		return 1
	else:
		return 0

def check_exists(tablename):
	global connection, cursor

	tablename = tablename.lower()

	try:
		cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (tablename,))
		return cursor.fetchone()[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(str(error))
		return False

def func1_list_tables():
	global connection, cursor

	query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
	#print(query)

	try:
		cursor.execute(query)
		list_tables = cursor.fetchall()
		for t_name_table in list_tables:
			print(t_name_table[0])
		return True

	except(Exception, psycopg2.DatabaseError) as error:
		print(str(error))
		return False

def func3_update_tables(tablename, filename):
	global connection, cursor

	tablename = tablename.lower()

	flag_error = False
	if check_exists(tablename):
		func5_clear_tables(tablename)

		insert_table(tablename,filename)
	else:
		print ('Tabela inexistente!')
		flag_error = True

	if flag_error == True:
		return False
	else:
		return True
	
def func4_populate_tables(tablename, filename):
	global connection, cursor

	tablename = tablename.lower()

	flag_error = False
	if check_exists(tablename):
		insert_table(tablename,filename)
	else:
		print ('Tabela inexistente!')
		flag_error = True

	if flag_error == True:
		return False
	else:
		return True

def func5_clear_tables(tablename):
	global connection, cursor

	tablename = tablename.lower()

	flag_error = False
	if tablename == 'all':
		pass
	elif check_exists(tablename):
		query = "TRUNCATE TABLE  " + tablename + " CASCADE;"
		#print(query)

		try:
			cursor.execute(query)

		except(Exception, psycopg2.DatabaseError) as error:
			print(str(error))
			flag_error = True
	else:
		print ('Tabela inexistente!')
		pass

	if flag_error == True:
		return False
	else:
		return True

def func6_reset_base():
	global connection, cursor

	run_script_sql('drop_tables.sql')

	run_script_sql('create_tables.sql')

	#run_script_sql('create_triggers.sql')

	counter_sucess = 0
	counter_sucess += insert_table('membro','tables/membro.csv')
	counter_sucess += insert_table('statusmembro','tables/statusmembro.csv')
	counter_sucess += insert_table('interessealumni','tables/interessealumni.csv')
	counter_sucess += insert_table('experienciaalumni','tables/experienciaalumni.csv')
	counter_sucess += insert_table('professor','tables/professor.csv')
	counter_sucess += insert_table('interesseprofessor','tables/interesseprofessor.csv')
	counter_sucess += insert_table('posicaoprofessor','tables/posicaoprofessor.csv')
	counter_sucess += insert_table('nucleo','tables/nucleo.csv')
	counter_sucess += insert_table('identidadenucleo','tables/identidadenucleo.csv')
	counter_sucess += insert_table('comite','tables/comite.csv')
	counter_sucess += insert_table('projeto','tables/projeto.csv')
	counter_sucess += insert_table('frenteprojeto','tables/frenteprojeto.csv')
	counter_sucess += insert_table('statusprojeto','tables/statusprojeto.csv')
	counter_sucess += insert_table('nucleoprojeto','tables/nucleoprojeto.csv')
	counter_sucess += insert_table('competicao','tables/competicao.csv')
	counter_sucess += insert_table('fasecompeticao','tables/fasecompeticao.csv')
	counter_sucess += insert_table('resultadocompeticao','tables/resultadocompeticao.csv')
	counter_sucess += insert_table('posicaonucleo','tables/posicaonucleo.csv')
	counter_sucess += insert_table('posicaocomite','tables/posicaocomite.csv')
	counter_sucess += insert_table('posicaoprojeto','tables/posicaoprojeto.csv')
	counter_sucess += insert_table('orientanucleo','tables/orientanucleo.csv')
	counter_sucess += insert_table('participacompeticao','tables/participacompeticao.csv')
	counter_sucess += insert_table('questoes','tables/questoes.csv')
	counter_sucess += insert_table('avaliacaoprojeto','tables/avaliacaoprojeto.csv')
	counter_sucess += insert_table('avaliacaonucleo','tables/avaliacaonucleo.csv')
	counter_sucess += insert_table('avaliacaocomite','tables/avaliacaocomite.csv')

	print('Tabelas resetadas: ' + str(counter_sucess))

def main():
	text = colored('BANCO DE DADOS RH SEMEAR', 'cyan', attrs=['reverse', 'blink'])
	print("\n" + text + "\n")

	global connection, cursor

	text = colored('CONECTANDO AO SERVIDOR', 'cyan', attrs=['bold', 'blink'])
	print("\n" + text)

	if len(sys.argv) == 1:
	# ==== Conexão interface ======== 
		root = tk.Tk()
		main = interface.MainView(root)
		main.pack(side="top", fill="both", expand=True)
		root.title('SEMEAR - Banco de Dados RH')
		root.wm_geometry('800x600')
		#root.resizable(0, 0)
		root.mainloop()
	# ===============================

	else:
		connect()

		sair = False

		while (sair is not True):
			voltar = False

			print(colored('MENU INICIAL', 'cyan', attrs=['bold', 'blink']))
			print('[0]: Sair')
			print('[1]: Listar tabelas')
			print('[2]: Consultar tabelas')
			print('[3]: Atualizar tabelas')
			print('[4]: Empilhar dados em tabelas')
			print('[5]: Limpar tabelas')
			print('[6]: Resetar banco')
			resposta1 = int(input('    > Escolha uma funcionalidade: '))

			if resposta1 == 0:
				print(colored('\nSAIR', 'cyan', attrs=['bold', 'blink']))
				print(colored('    > Finalizando aplicação. Até mais!', 'cyan'))

				sair = True

			elif resposta1 == 1:
				print(colored('\nLISTAR TABELAS', 'cyan', attrs=['bold', 'blink']))

				print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')

				func1_list_tables()

				print('---------------------------------------------------------')

			elif resposta1 == 2:
				while voltar == False:
					print(colored('\nCONSULTAR TABELAS', 'cyan', attrs=['bold', 'blink']))
					print('[0]: Voltar ao menu inicial')
					print('[1]: Lista de membros (por tipo, por núcleo, por comitê, por projeto)')
					print('[2]: Informações pessoais de um membro')
					print('[3]: Posições atuais de um membro no grupo (núcleos, comitês, projetos)')
					print('[4]: Histórico de cargos de um membro no grupo')
					print('[5]: Lista de professores')
					print('[6]: Projetos abertos de um núcleo')
					print('[7]: Competições por ano')
					print('[8]: Resultados de uma competição')
					search_index = input('    > Consulta a ser realizada: ')

					if search_index == '0':
						voltar = True
						break

					if search_index == '1':
						input1 = input('    > Apenas membros ativos (1) ou todos (2)? ')

						print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')
						select.func2_1(cursor, input1)

					if search_index == '2':
						input1 = input('    > NUSP do membro? ')

						print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')
						select.func2_2(cursor, input1)

					if search_index == '3':
						input1 = input('    > NUSP do membro? ')

						print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')
						select.func2_3(cursor, input1)

					print('---------------------------------------------------------')


			elif resposta1 == 3:
				while voltar == False:
					print(colored('\nATUALIZAR TABELAS', 'cyan', attrs=['bold', 'blink']))
					print('[0]: Voltar ao menu inicial')
					
					tablename = input('    > Tabela a atualizar: ')
					if tablename== '0':
						voltar = True
						break

					filename = input('    > Nome do arquivo csv: ')
					if filename== '0':
						voltar = True
						break

					filename = 'tables/' + filename + '.csv'
				
					print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')

					resultado = func3_update_tables(tablename, filename)

					if resultado == True:
						print(colored('    > Atualização realizada com sucesso!', 'cyan'))
					else:
						print(colored('    > Erro na atualização', 'red'))
					
					print('---------------------------------------------------------')


			elif resposta1 == 4:
				while voltar == False:
					print(colored('\nEMPILHAR DADOS EM TABELAS', 'cyan', attrs=['bold', 'blink']))
					print('[0]: Voltar ao menu inicial')

					tablename = input('    > Tabela a empilhar: ')
					if tablename== '0':
						voltar = True
						break

					filename = input('    > Nome do arquivo csv: ')
					if filename== '0':
						voltar = True
						break

					filename = 'tables/' + filename + '.csv'
				
					print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')

					resultado = func4_populate_tables(tablename, filename)

					if resultado == True:
						print(colored('    > Inserções realizadas com sucesso!', 'cyan'))
					else:
						print(colored('    > Erro na atualização', 'red'))
					
					print('---------------------------------------------------------')
			
			elif resposta1 == 5:
				while voltar == False:
					print(colored('\nLIMPAR TABELAS', 'cyan', attrs=['bold', 'blink']))
					print('[0]: Voltar ao menu inicial')

					resposta2 = input('    > Tabela a limpar ("all" para todas): ')

					if resposta2 == '0':
						voltar = True
						break

					print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')

					if resposta2 == '1':
						func1_list_tables()
					else:
						resultado = func5_clear_tables(resposta2)

					if resultado == True:
						print(colored('    > Tabela limpa com sucesso!', 'cyan'))
					else:
						print(colored('    > Erro na limpeza', 'red'))
					
					print('---------------------------------------------------------')
				
			elif resposta1 == 6:
				print(colored('\nRESETAR BANCO', 'cyan', attrs=['bold', 'blink']))

				print('\n---------------- RELATÓRIO DE EXECUÇÃO ------------------')

				func6_reset_base()

				print('---------------------------------------------------------')

			else:
				print(colored('\n    > Entrada inválida! Tente novamente.', 'red'))
				run_script_sql('drop_tables.sql')
			print('\n')

	cursor.close()
 
if __name__ == '__main__':
	main()
	
