#importando SqLite 3
import sqlite3

#criar conexão Py com o Sq
try:
    con = sqlite3.connect('cadastro_alunos.db')
    con.execute("PRAGMA foreign_keys = ON;")
    print("Conexão com o Banco de Dados realizada com sucesso!")
except sqlite3.Error as e:
    print("Não foi possível conectar com o Banco de Dados!", e)

#criando tabela de Curso
try:
    with con:
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            duracao TEXT,
            preco REAL        
        )""")

        print("Tabela Cursos criada com sucesso")

except sqlite3.Error as e:
    print("Erro ao Criar a tabela de Cursos", e)

#criando tabela de turma:
try:
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            curso_nome TEXT,
            data_inicio DATE,
            FOREIGN KEY (curso_nome) REFERENCES cursos (nome) ON UPDATE CASCADE ON DELETE CASCADE
        )""")

        print("Tabela de Turmas criada com sucesso")

except sqlite3.Error as e:
    print("Erro ao criar a Tabela de Turmas:", e)

#Criando Tabela de Alunos
try:
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            email TEXT,
            telefone TEXT,
            sexo TEXT,
            imagem TEXT,
            data_nascimento DATE,
            cpf TEXT,
            nome_turma TEXT,
            FOREIGN KEY (nome_turma) REFERENCES turmas (nome) ON DELETE CASCADE
            )""")
        
        print("Tabela Alunos criada com sucesso")

except sqlite3.Error as e:
    print("Erro ao Criar a Tabela Alunos:", e)