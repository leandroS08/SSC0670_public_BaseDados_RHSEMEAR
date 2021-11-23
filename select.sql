SELECT NUSP, NomeCompleto, TO_CHAR( AGE(CURRENT_DATE, DataAdmissao) , 'YY ano(s) MM mes(es)') AS TempoGrupo
FROM Membro
WHERE Tipo LIKE 'Membro Ativo'
ORDER BY NomeCompleto

SELECT M.NUSP, M.NomeCompleto, N.Nome, PN.Cargo, PN.DataInicio
FROM Membro M
LEFT JOIN PosicaoNucleo PN on M.NUSP = PN.MembroNUSP
LEFT JOIN Nucleo N on N.Sigla = PN.NucleoSigla
WHERE M.NUSP = membroNUSP AND M.Tipo LIKE 'Membro Ativo   ' AND PN.MembroNUSP IS NOT NULL AND PN.DataFim IS NULL
UNION ALL 
SELECT M.NUSP, M.NomeCompleto, PC.ComiteNome, PC.Cargo, PC.DataInicio
FROM Membro M
LEFT JOIN PosicaoComite PC on M.NUSP = PC.MembroNUSP
LEFT JOIN Comite C on C.Nome = PC.ComiteNome
WHERE M.NUSP =  membroNUSP  AND M.Tipo LIKE 'Membro Ativo   ' AND PC.MembroNUSP IS NOT NULL AND PC.DataFim IS NULL
UNION ALL
SELECT M.NUSP, M.NomeCompleto, PP.ProjetoNome, PP.Cargo, PP.DataInicio
FROM Membro M
LEFT JOIN PosicaoProjeto PP on M.NUSP = PP.MembroNUSP
LEFT JOIN Projeto P on P.Nome = PP.ProjetoNome
WHERE M.NUSP =  membroNUSP  AND M.Tipo LIKE 'Membro Ativo   ' AND PP.MembroNUSP IS NOT NULL AND PP.DataFim IS NULL;


