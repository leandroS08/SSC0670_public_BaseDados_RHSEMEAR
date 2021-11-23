--------------------------------------------------------- trigger de avaliação das entradas para os campos de um novo membro
CREATE OR REPLACE FUNCTION function_number() RETURNS TRIGGER AS $BODY$
BEGIN
	IF (NEW.DataAdmissao < CURRENT_DATE AND NEW.DataAdmissao > '2010-12-31') THEN 
		return new;
	ELSE
		RAISE 'Data não permitida!';
	END IF;

	IF NEW.Celular ~ '^[0-9\.]*$' THEN 
		return new;
	ELSE
		RAISE 'Apenas números são permitidos!';
	END IF;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER function_number BEFORE INSERT OR UPDATE ON Membro
    FOR EACH ROW EXECUTE PROCEDURE function_number();

--------------------------------------------------------- trigger do nivel de hierarquia a partir do cargo
CREATE OR REPLACE FUNCTION function_hierarquia_posicaonucleo() RETURNS TRIGGER AS $BODY$
BEGIN
  IF (NEW.Cargo = 'PRESIDENTE' OR NEW.Cargo = 'DIRETOR(A)' OR NEW.Cargo = 'VICE-DIRETOR(A)') THEN 
    NEW.NivelHierarquia = 'DIREÇÃO';
    return NEW;
  ELSIF (NEW.Cargo = 'GERENTE' OR NEW.Cargo = 'COORDENADOR(A)') THEN
    NEW.NivelHierarquia = 'GERÊNCIA';
    return NEW;
  ELSIF (NEW.Cargo = 'MEMBRO' OR NEW.Cargo = 'OUTRO') THEN
    NEW.NivelHierarquia = 'OPERAÇÃO';
    return NEW;
  END IF;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER function_hierarquia_posicaonucleo BEFORE INSERT OR UPDATE ON PosicaoNucleo
    FOR EACH ROW EXECUTE PROCEDURE function_hierarquia_posicaonucleo();


--------------------------------------------------------- trigger de atualização do tipo do membro a partir do status
CREATE OR REPLACE FUNCTION function_tipostatus_membro() RETURNS TRIGGER AS $BODY$
BEGIN
  IF (NEW.TipoStatus = 'ALUMNI' OR NEW.TipoStatus = 'HONORÁRIO') THEN 
    UPDATE Membro SET Tipo = 'MEMBRO ALUMNI' WHERE NUSP = NEW.MembroNUSP;
    return NEW;
  ELSIF (NEW.TipoStatus = 'EX-MEMBRO') THEN
    UPDATE Membro SET Tipo = 'EX-MEMBRO' WHERE NUSP = NEW.MembroNUSP;
    return NEW;
  ELSE
    UPDATE Membro SET Tipo = 'MEMBRO ATIVO' WHERE NUSP = NEW.MembroNUSP;
    return NEW;
  END IF;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER function_tipostatus_membro BEFORE INSERT OR UPDATE ON StatusMembro
    FOR EACH ROW EXECUTE PROCEDURE function_tipostatus_membro();


--------------------------------------------------------- trigger para o cálculo de número de membros em um núcleo
CREATE OR REPLACE FUNCTION function_counter_membros_nucleo() RETURNS TRIGGER AS $BODY$
BEGIN
	UPDATE Nucleo SET NumeroMembros = (SELECT COUNT(*) FROM (SELECT DISTINCT MembroNUSP FROM PosicaoNucleo WHERE Sigla = NEW.NucleoSigla) AS x);
	return NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER function_counter_membros_nucleo AFTER INSERT OR UPDATE ON PosicaoNucleo
    FOR EACH ROW EXECUTE PROCEDURE function_counter_membros_nucleo();
    

--------------------------------------------------------- trigger para impedir que um membro seja alocado em um projeto fora do seu núcleo atual