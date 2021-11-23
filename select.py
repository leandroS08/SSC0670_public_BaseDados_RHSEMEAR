import psycopg2
from termcolor import colored

#Função 2.1: listar membros (todos ou apenas ativos)
def func2_1(cursor, option):
    if option == '1':
        query = ""
        query += "SELECT NUSP, NomeCompleto, TO_CHAR( AGE(CURRENT_DATE, DataAdmissao) , 'YY ano(s) MM mes(es)') AS TempoGrupo"
        query += " FROM Membro"
        query += " WHERE Tipo LIKE 'Membro Ativo   '"
        query += " ORDER BY NomeCompleto"
        results = []
        print(query)
    
    elif option == '2':
        query = ""
        query += "SELECT NUSP, NomeCompleto, Tipo, TO_CHAR( AGE(CURRENT_DATE, DataAdmissao) , 'YY ano(s) MM mes(es)') AS TempoGrupo"
        query += " FROM Membro"
        query += " ORDER BY NomeCompleto"
        results = []
        print(query)
    
    else:
        print('Opção inválida')

    try:
        cursor.execute(query)
        result = cursor.fetchall()

        for value in result:
            results.append(str(value))

        if (len(results) == 0):
            print('sem dados')

        else:
            for aux in result:
                print(aux)
        
        return result

    except Exception as error:
        print(error)
        return None

#Função 2.1: consultar dados de um membro
def func2_2(cursor, membroNUSP):
    query = ""
    query += "SELECT *"
    query += " FROM Membro"
    query += " WHERE NUSP = " + membroNUSP + ";"
    results = []
    print(query)
  
    try:
        cursor.execute(query)
        result = cursor.fetchall()

    except Exception as error:
        print('Erro')
    
    query = "SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'membro'"
    column = []
    print(query)
  
    try:
        cursor.execute(query)
        column = cursor.fetchall()
        #print(column)

    except Exception as error:
        print('Erro')
    
    for i in range(len(result[0])):
        print(str(column[i][3]) + " : " + str(result[0][i]))


#Função 2.1: consultar dados de um membro
def func2_3(cursor, membroNUSP):
    query = ""
    query = "SELECT M.NUSP, M.NomeCompleto, N.Nome, PN.Cargo, PN.DataInicio"
    query += " FROM Membro M"
    query += " LEFT JOIN PosicaoNucleo PN on M.NUSP = PN.MembroNUSP"
    query += " LEFT JOIN Nucleo N on N.Sigla = PN.NucleoSigla"
    query += " WHERE M.NUSP = " + membroNUSP + " AND M.Tipo LIKE 'Membro Ativo   ' AND PN.MembroNUSP IS NOT NULL AND PN.DataFim IS NULL"
    query += " UNION ALL "
    query += "SELECT M.NUSP, M.NomeCompleto, PC.ComiteNome, PC.Cargo, PC.DataInicio"
    query += " FROM Membro M"
    query += " LEFT JOIN PosicaoComite PC on M.NUSP = PC.MembroNUSP"
    query += " LEFT JOIN Comite C on C.Nome = PC.ComiteNome"
    query += " WHERE M.NUSP = " + membroNUSP + " AND M.Tipo LIKE 'Membro Ativo   ' AND PC.MembroNUSP IS NOT NULL AND PC.DataFim IS NULL"
    query += " UNION ALL "
    query += "SELECT M.NUSP, M.NomeCompleto, PP.ProjetoNome, PP.Cargo, PP.DataInicio"
    query += " FROM Membro M"
    query += " LEFT JOIN PosicaoProjeto PP on M.NUSP = PP.MembroNUSP"
    query += " LEFT JOIN Projeto P on P.Nome = PP.ProjetoNome"
    query += " WHERE M.NUSP = " + membroNUSP + " AND M.Tipo LIKE 'Membro Ativo   ' AND PP.MembroNUSP IS NOT NULL AND PP.DataFim IS NULL"
    #query += " GROUP BY NomeCompleto" 
    results = []
    print(query)
  
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        #for i in range(len(results)):
        #    print(str(results[i]))
        return results

    except Exception as error:
        print('QUERY: '+ query)
        text = colored('ERRO:', 'red', attrs=['reverse', 'blink'])
        print(text + ' ' + str(error) + '\n')
        return None


#Abrir projeto
def func2_4(cursor, projetonome, projetotipo, projetodescricao, projetodataabertura, projetonucleo):
    query = "INSERT INTO Projeto (Nome, TipoPrincipal, Descricao, DataAbertura) VALUES ('" + projetonome + "','"  + projetotipo + "','"  + projetodescricao + "','" + projetodataabertura + "');"
    print(query)
  
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print('inserção bem sucedida!')
        return result

    except Exception as error:
        print(error)
        return error
    

def func2_5(cursor, tipomembro, nucleo):
    query = ""
    query += "SELECT DISTINCT M.NUSP, M.NomeCompleto, TO_CHAR( AGE(CURRENT_DATE, M.DataAdmissao) , 'YY ano(s) MM mes(es)') AS TempoGrupo"
    query += " FROM Membro M"
    query += " LEFT JOIN PosicaoNucleo PN ON M.NUSP = PN.MembroNUSP"
    query += " WHERE M.Tipo = 'Membro Ativo   '"
    query += " AND PN.DataFim IS NULL"
    query += " AND PN.NucleoSigla = '" + nucleo + "'"
    query += " ORDER BY M.NomeCompleto"
    results = []
    print(query)

    try:
        cursor.execute(query)
        result = cursor.fetchall()

        for value in result:
            results.append(str(value))

        if (len(results) == 0):
            print('sem dados')

        else:
            for aux in result:
                print(aux)
        
        return result

    except Exception as error:
        print(error)
        return None