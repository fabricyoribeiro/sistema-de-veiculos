create table if not exists motorista (
	id serial primary key,
	nome varchar(50),
	cpf varchar(11) unique not null,
	salario numeric(10,2)
);

create table if not exists posto(
    id serial primary key,
    nome varchar(50),
    cidade varchar(50),
    cnpj varchar(50)
);

create table if not exists marca(
    id serial primary key,
    marca varchar(20),
    classificacao varchar(50)	
);

create table if not exists modelo(
    id serial primary key,
    descricao varchar(50),
    marca_id int,
    constraint fkmarca foreign key (marca_id) references marca(id)
);

create table if not exists veiculo(
	id serial primary key,
	placa varchar(7) unique not null,
	modelo_id int,
	km_total numeric(10,2),
    constraint fkmodelo foreign key (modelo_id)references modelo(id)
);

create table if not exists viagem(
	id serial primary key,
	veiculo_id int,
	motorista_id int,
	destino varchar(100),
	constraint fk_motorista foreign key(motorista_id) references motorista(id),
	constraint fkveiculo foreign key(veiculo_id) references veiculo(id)
);


create table if not exists abastecimento(
	id serial primary key,
    data_abastecimento date,
	viagem_id int,
	veiculo_id int,
    posto_id int,
	valor_gasto float,
	km_atual numeric(10, 2),
    constraint fkposto foreign key (posto_id) references posto(id),
	constraint fkviagem foreign key (viagem_id) references viagem(id),
	constraint fkveiculo foreign key (veiculo_id) references veiculo(id)
);
