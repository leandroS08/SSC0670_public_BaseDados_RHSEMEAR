----------- PESSOAS (ENTIDADES FORTES E FRACAS)

create table Membro(
	NUSP int check (NUSP > 0),
	NomeCompleto varchar(50) not null,
	Tipo char(15) not null check (upper(Tipo) in ('MEMBRO ATIVO','EX-MEMBRO','MEMBRO ALUMNI')) DEFAULT 'EX-MEMBRO', 
	Apelido varchar(25),
	NivelHierarquico varchar(15) check (upper(NivelHierarquico) in ('DIREÇÃO','GERÊNCIA','OPERAÇÃO','-')) DEFAULT 'OPERAÇÃO',
	DataAdmissao date not null,
	AnoIngressoUSP smallint,
	CursoInstituicao varchar(75) not null,
	CursoNivel varchar(30) not null check (upper(CursoNivel) in ('GRADUAÇÃO - BACHARELADO','GRADUAÇÃO - LICENCIATURA','GRADUAÇÃO - TECNÓLOGO','PÓS-GRADUAÇÃO','MESTRADO','DOUTORADO','PÓS-DOUTORADO','OUTRO')),
	CursoNome varchar(50) not null, 
	CursoAnoIngresso smallint not null,
	CursoAnoFormatura smallint,
	RG varchar(12),
	DataNascimento date,
	Celular varchar(15),
	EmailPrincipal varchar(50) not null , 
	EmailSecundario varchar(50),
	LinkedIn varchar(100),
	Facebook varchar(100),
	Instagram varchar(100),
	FotoPerfil bytea,
	Cor varchar(20) check (upper(Cor) in ('PARDA','BRANCA','PRETA','AMARELA','INDÍGENA','PREFIRO NÃO DIZER')),
	Genero varchar(20) check (upper(Genero) in ('MASCULINO','FEMININO','NÃO-BINÁRIO','OUTRO','PREFIRO NÃO DIZER')),
	PaisOrigem varchar(20),
	EstadoOrigem varchar(30),
	CidadeOrigem varchar(30),
	PaisAtual varchar(20),
	EstadoAtual varchar(30),
	CidadeAtual varchar(30),
	constraint pk_Membro primary key (NUSP)
);

create table StatusMembro(
	MembroNUSP int,
	DataAtualizacao date,
	TipoStatus varchar(30) not null check (upper(TipoStatus) in ('EFETIVO','SOB AVALIAÇÃO','AFASTADO','CONVIDADO','COLABORADOR','CONSELHEIRO','EX-MEMBRO','ALUMNI','HONORÁRIO')),
	Observacao varchar(250),
	constraint pk_StatusMembro primary key (MembroNUSP, DataAtualizacao),
	constraint fk_StatusMembro foreign key (MembroNUSP) references Membro(NUSP) on delete cascade
);

create table InteresseAlumni(
	MembroNUSP int,
	AreaInteresse varchar(30),
	constraint pk_InteresseAlumni primary key (MembroNUSP, AreaInteresse),
	constraint fk_InteresseAlumni foreign key (MembroNUSP) references Membro(NUSP) on delete cascade
);

create table ExperienciaAlumni(
	MembroNUSP int,
	NExperiencia smallint,
	Instituicao varchar(75) not null, -- TRIGGER APENAS CARACTERES ALFABÉTICOS
	DataInicio date not null,
	Posicao varchar(75),
	DataFim date check (DataFim > DataInicio),
	Observacao varchar(200),
	constraint pk_ExperienciaAlumni primary key (MembroNUSP, NExperiencia),
	constraint fk_ExperienciaAlumni foreign key (MembroNUSP) references Membro(NUSP) on delete cascade
);

create table Professor(
	Nome varchar(50),
	DataAdmissao date not null,
	Instituicao varchar(75) not null,
	Unidade varchar(75),
	Departamento varchar(75),
	Lattes varchar(100),
	DataNascimento date,
	Celular varchar(15), -- TRIGGER APENAS CARACTERES NUMÉRICOS
	EmailPrincipal varchar(50) not null,
	EmailSecundario varchar(50),
	LinkedIn varchar(100),
	Facebook varchar(100),
	Instagram varchar(100),
	FotoPerfil varchar(100),
	Cor varchar(20) check (upper(Cor) in ('PARDA','BRANCA','PRETA','AMARELA','INDÍGENA','PREFIRO NÃO DIZER')),
	Genero varchar(20) check (upper(Genero) in ('MASCULINO','FEMININO','NÃO-BINÁRIO','OUTRO','PREFIRO NÃO DIZER')),
	PaisAtual varchar(20),
	EstadoAtual varchar(30),
	CidadeAtual varchar(30),
	constraint pk_Professor primary key (Nome)
);

create table InteresseProfessor(
	ProfessorNome varchar(50),
	AreaInteresse varchar(30),
	constraint pk_InteresseProfessor primary key (ProfessorNome, AreaInteresse),
	constraint fk_InteresseProfessor foreign key (ProfessorNome) references Professor(Nome) on delete cascade
);

create table PosicaoProfessor(
	ProfessorNome varchar(50),
	DataAtualizacao date,
	TipoStatus varchar(30) not null check (upper(TipoStatus) in ('ORIENTADOR','COORDENADOR','OUTRO')),
	Observacoes varchar(250),
	constraint pk_PosicaoProfessor primary key (ProfessorNome, DataAtualizacao),
	constraint fk_PosicaoProfessor foreign key (ProfessorNome) references Professor(Nome) on delete cascade
);


----------- ESTRUTURA ORGANIZACIONAL (ENTIDADES FORTES E FRACAS)

create table Nucleo(
	Sigla char(3),
	Nome varchar(30) not null,
	NumeroMembros smallint, -- TRIGGER: calculado a partir da posicao dos membros
	NumeroProjetos smallint, -- TRIGGER: calculado a partir da relacao com projetos
	DataCriacao date not null,
	DataFechamento date check (DataFechamento > DataCriacao),
	constraint pk_Nucleo primary key (Sigla)
);

create table IdentidadeNucleo(
	NucleoSigla char(3),
	DataAtualizacao date,
	Escopo varchar(250) not null,
	Missao varchar(250) not null,
	Visao varchar(250) not null,
	constraint pk_EscopoNucleo primary key (NucleoSigla, DataAtualizacao),
	constraint fk_EscopoNucleo foreign key (NucleoSigla) references Nucleo(Sigla) on delete cascade
);

create table Comite(
	Nome varchar(30), 
	NumeroMembros int, -- TRIGGER: calculado a partir da posicao dos membros
	DataCriacao date not null,
	DataFechamento date,
	DescricaoEscopo varchar(250) not null,
	constraint pk_Comite primary key (Nome)
);

create table Projeto(
	Nome varchar(50),
	TipoPrincipal varchar(30) not null check (upper(TipoPrincipal) in ('TÉCNICO-ROBÔ','TÉCNICO','EXTENSÃO','GESTÃO','GESTÃO - SETOR','OUTRO')), 
	Descricao varchar(250),
	NumeroMembros int,
	DataAbertura date,
	LinkTermoAbertura varchar(100),
	LinkPastaGeral varchar(100),
	LinkGestaoConhecimento varchar(100),
	LinkGestaoFinanceira varchar(100),
	LinkMultimidia varchar(100),
	constraint pk_Projeto primary key (Nome)
);

create table FrenteProjeto(
	ProjetoNome varchar(50),
	FrenteNome varchar(30),
	Descricao varchar(250),
	constraint pk_FrenteProjeto primary key (ProjetoNome, FrenteNome),
	constraint fk_FrenteProjeto foreign key (ProjetoNome) references Projeto(Nome) on delete cascade
);

create table StatusProjeto(
	ProjetoNome varchar(50),
	DataAtualizacao date,
	TipoStatus varchar(30) not null check (upper(TipoStatus) in ('ABERTO','FECHADO','PARALISADO','OUTRO')),
	Observacoes varchar(250),
	constraint pk_StatusProjeto primary key (ProjetoNome, DataAtualizacao),
	constraint fk_StatusProjeto foreign key (ProjetoNome) references Projeto(Nome) on delete cascade
);

create table NucleoProjeto(
	ProjetoNome varchar(50),
	NucleoSigla char(3),
	constraint pk_NucleoProjeto primary key (ProjetoNome, NucleoSigla),
	constraint fk1_NucleoProjeto foreign key (ProjetoNome) references Projeto(Nome) on delete cascade,
	constraint fk2_NucleoProjeto foreign key (NucleoSigla) references Nucleo(Sigla) on delete cascade
);

create table Competicao(
	Nome varchar(30),
	Ano int check (Ano > 2010 AND Ano <= date_part('year', CURRENT_DATE)),
	Descricao varchar(200),
	AlbumFotos varchar(100),
	constraint pk_Competicao primary key (Nome,Ano)
);

create table FaseCompeticao(
	CompeticaoNome varchar(30),
	CompeticaoAno int,
	NumeroFase smallint,
	Tipo varchar(30) not null check (upper(Tipo) in ('PRESENCIAL','VIRTUAL','OUTRO')),
	Pais varchar(20) not null,
	Estado varchar(30),
	Cidade varchar(30),
	DataInicio date,
	DataFim date,
	constraint pk_FaseCompeticao primary key (CompeticaoNome,CompeticaoAno,NumeroFase),
	constraint fk_FaseCompeticao foreign key (CompeticaoNome,CompeticaoAno) references Competicao(Nome,Ano) on delete cascade
);

create table ResultadoCompeticao(
	ProjetoNome varchar(50),
	CompeticaoNome varchar(30),
	CompeticaoAno int,
	Categoria varchar(60),
	Posicao smallint,
	Premiacao varchar(250),
	Descricao varchar(250),
	constraint pk_ResultadoCompeticao primary key (ProjetoNome, CompeticaoNome,CompeticaoAno,Categoria),
	constraint fk1_ResultadoCompeticao foreign key (ProjetoNome) references Projeto(Nome) on delete cascade,
	constraint fk2_ResultadoCompeticao foreign key (CompeticaoNome,CompeticaoAno) references Competicao(Nome,Ano)
);


----------- RELACIONAMENTOS DE PESSOAS COM AS ESTRUTURAS

create table PosicaoNucleo(
	MembroNUSP int,
	NucleoSigla char(3),
	Posicao varchar(10) check (upper(Posicao) in ('PRIMÁRIO','SECUNDÁRIO')),
	Cargo varchar(30) check (upper(Cargo) in ('PRESIDENTE','DIRETOR(A)','VICE-DIRETOR(A)','GERENTE','COORDENADOR(A)','MEMBRO','OUTRO')),
	DataInicio date,
	DataFim date,
	NivelHierarquia varchar(15) check (upper(NivelHierarquia) in ('DIREÇÃO','GERÊNCIA','OPERAÇÃO')) DEFAULT 'OPERAÇÃO', -- TRIGGER
	constraint pk_PosicaoNucleo primary key (MembroNUSP,NucleoSigla,Posicao,Cargo,DataInicio),
	constraint fk1_PosicaoNucleo foreign key (MembroNUSP) references Membro(NUSP) on delete cascade,
	constraint fk2_PosicaoNucleo foreign key (NucleoSigla) references Nucleo(Sigla) on delete cascade
);

create table PosicaoComite(
	MembroNUSP int,
	ComiteNome varchar(30),
	Cargo varchar(30) check (upper(Cargo) in ('COORDENADOR(A)','VICE-COORDENADOR(A)','MEMBRO','OUTRO')),
	DataInicio date,
	DataFim date check (DataFim > DataInicio),
	NivelHierarquia varchar(15) constraint ck_PosicaoComite_NivelHierarquia check (upper(NivelHierarquia) in ('GERÊNCIA','OPERAÇÃO')) DEFAULT 'OPERAÇÃO', -- TRIGGER
	constraint pk_PosicaoComite primary key (MembroNUSP,ComiteNome,Cargo,DataInicio),
	constraint fk1_PosicaoComite foreign key (MembroNUSP) references Membro(NUSP) on delete cascade,
	constraint fk2_PosicaoComite foreign key (ComiteNome) references Comite(Nome) on delete cascade
);

create table PosicaoProjeto(
	MembroNUSP int,
	ProjetoNome varchar(50),
	FrenteProjetoNome varchar(30),
	Cargo varchar(30) check (upper(Cargo) in ('GERENTE','MEMBRO','OUTRO')),
	DataInicio date,
	DataFim date check (DataFim > DataInicio),
	NivelHierarquia varchar(15) check (upper(NivelHierarquia) in ('GERÊNCIA','OPERAÇÃO')) DEFAULT 'OPERAÇÃO', -- TRIGGER
	constraint pk_PosicaoProjeto primary key (MembroNUSP,ProjetoNome,FrenteProjetoNome,Cargo,DataInicio),
	constraint fk1_PosicaoProjeto foreign key (MembroNUSP) references Membro(NUSP),
	constraint fk2_PosicaoProjeto foreign key (ProjetoNome,FrenteProjetoNome) references FrenteProjeto(ProjetoNome,FrenteNome)
);

create table OrientaNucleo(
	ProfessorNome varchar(50),
	NucleoSigla char(3),
	Observacoes char(250),
	constraint pk_OrientaNucleo primary key (ProfessorNome,NucleoSigla),
	constraint fk1_OrientaNucleo foreign key (ProfessorNome) references Professor(Nome) on delete cascade,
	constraint fk2_OrientaNucleo foreign key (NucleoSigla) references Nucleo(Sigla) on delete cascade
);

create table ParticipacaoCompeticao(
	MembroNUSP int,
	CompeticaoNome varchar(30),
	CompeticaoAno int,
	FlagCapitao boolean DEFAULT FALSE,
	constraint pk_ParticipacaoCompeticao primary key (MembroNUSP,CompeticaoNome,CompeticaoAno),
	constraint fk1_ParticipacaoCompeticao foreign key (MembroNUSP) references Membro(NUSP),
	constraint fk2_ParticipacaoCompeticao foreign key (CompeticaoNome,CompeticaoAno) references Competicao(Nome,Ano)
);


----------- MÓDULO DE AVALIAÇÕES

create table Questoes(
	Indice int,
	Descricao varchar(250),
	constraint pk_Questoes primary key (Indice)
);

create table AutoAvaliacao(
	MembroNUSP int,
	DataAvaliacao date,
	PerguntaIndice int,
	Resposta int not null check (Resposta >=1 AND Resposta <=5),
	Comentario varchar(250),
	constraint pk_AutoAvaliacao primary key (MembroNUSP, DataAvaliacao, PerguntaIndice),
	constraint fk1_AutoAvaliacao foreign key (MembroNUSP) references Membro(NUSP) on delete cascade,
	constraint fk2_AutoAvaliacao foreign key (PerguntaIndice) references Questoes(Indice) on delete cascade
);

create table AvaliacaoProjeto(
	MembroNUSP int,
	ProjetoNome varchar(50),
	ProjetoFrenteNome varchar(30),
	PosicaoProjetoCargo varchar(30),
	PosicaoProjetoDataInicio date,
	DataAvaliacao date,
	PerguntaIndice int,
	Resposta int not null check (Resposta >=1 AND Resposta <=5),
	Comentario varchar(250),
	constraint pk_AvaliacaoProjeto primary key (ProjetoNome, ProjetoFrenteNome, DataAvaliacao, PerguntaIndice, MembroNUSP, PosicaoProjetoCargo, PosicaoProjetoDataInicio),
	constraint fk1_AvaliacaoProjeto foreign key (MembroNUSP, ProjetoNome, ProjetoFrenteNome,PosicaoProjetoCargo,PosicaoProjetoDataInicio) references PosicaoProjeto(MembroNUSP, ProjetoNome, FrenteProjetoNome, Cargo, DataInicio) on delete cascade,
	constraint fk2_AvaliacaoProjeto foreign key (PerguntaIndice) references Questoes(Indice) on delete cascade
);

create table AvaliacaoNucleo(
	MembroNUSP int,
	NucleoSigla char(3),
	PosicaoNucleoPosicao varchar(10),
	PosicaoNucleoCargo varchar(30),
	PosicaoNucleoDataInicio date,
	DataAvaliacao date,
	PerguntaIndice int,
	Resposta int not null check (Resposta >=1 AND Resposta <=5),
	Comentario varchar(250),
	constraint pk_AvaliacaoNucleo primary key (NucleoSigla, DataAvaliacao, PerguntaIndice, MembroNUSP, PosicaoNucleoPosicao, PosicaoNucleoCargo, PosicaoNucleoDataInicio),
	constraint fk1_AvaliacaoNucleo foreign key (MembroNUSP, NucleoSigla,PosicaoNucleoPosicao,PosicaoNucleoCargo,PosicaoNucleoDataInicio) references PosicaoNucleo(MembroNUSP, NucleoSigla, Posicao, Cargo, DataInicio) on delete cascade,
	constraint fk2_AvaliacaoNucleo foreign key (PerguntaIndice) references Questoes(Indice) on delete cascade
);

create table AvaliacaoComite(
	MembroNUSP int,
	ComiteNome varchar(30),
	PosicaoComiteCargo varchar(30),
	PosicaoComiteDataInicio date,
	DataAvaliacao date,
	PerguntaIndice int,
	Resposta int not null check (Resposta >=1 AND Resposta <=5),
	Comentario varchar(250),
	constraint pk_AvaliacaoComite primary key (ComiteNome, DataAvaliacao, PerguntaIndice, MembroNUSP, PosicaoComiteCargo, PosicaoComiteDataInicio),
	constraint fk1_AvaliacaoComite foreign key (MembroNUSP, ComiteNome,PosicaoComiteCargo,PosicaoComiteDataInicio) references PosicaoComite(MembroNUSP, ComiteNome, Cargo, DataInicio) on delete cascade,
	constraint fk2_AvaliacaoComite foreign key (PerguntaIndice) references Questoes(Indice) on delete cascade
);

