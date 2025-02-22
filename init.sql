-- Criação da tabela de testes SSL
CREATE TABLE IF NOT EXISTS ssl_test_results (
    id SERIAL PRIMARY KEY,
    dominio VARCHAR(255) NOT NULL,
    hora_inicio_teste TIMESTAMP NOT NULL,
    dias_restantes INT,
    nota VARCHAR(10),
    vulnerabilidade TEXT,
    vulneravel BOOLEAN,
    erro TEXT
);

-- Criação da tabela que salva os testes de disponibilidade
CREATE TABLE IF NOT EXISTS disponibilidade_sistemas (
    id SERIAL PRIMARY KEY,
    sistema VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    data_hora_teste TIMESTAMP NOT NULL,
    status BOOLEAN NOT NULL,
    tempo_resposta FLOAT,
    erro TEXT
);