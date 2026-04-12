import sqlite3

#criar conexão Py com o Sq
try:
    con = sqlite3.connect('cadastro_alunos.db')
    con.execute("PRAGMA foreign_keys = ON;")
    print("Conexão com o Banco de Dados realizada com sucesso!")
except sqlite3.Error as e:
    print("Não foi possível conectar com o Banco de Dados!", e)

#Tabela de Cursos

#Cadastro de Cursos (Creat C)

def criar_curso(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Cursos (nome, duracao, preco) VALUES (?, ?, ?)"
        cur.execute(query, i)
        
#criar_curso(["Python", "2 Semanas", 50])

#Ver todos os cursos (Read R)
def ver_cursos():
    lista = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Cursos")
        linha = cur.fetchall()

        for i in linha:
            lista.append(i)
    return lista

#Atualizar Cursos (Uptade U)
def atualizar_curso(i):
    with con:
        cur = con.cursor()
        query = "UPDATE Cursos SET nome=?, duracao=?, preco=? WHERE id=?"
        cur.execute(query, i)

#atualizar_curso(l)

#Deletar Cursos (Delete D)
def deletar_curso(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Cursos WHERE id=?"
        cur.execute(query, i)

#deletar_curso([1])

#Tabela Turmas

#Criar Turmas (Creat C)
def criar_turma(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO turmas (nome, nome_curso, data_inicio) VALUES (?, ?, ?)"
        cur.execute(query, i)

#Ver Turmas (Rear R)
def ver_turma():
    lista = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM turmas")
        linha = cur.fetchall()

        for i in linha:
            lista.append(i)
    return lista

#Atualizar Turma (Uptade U)
def atualizar_turma(i):
    with con:
        cur = con.cursor()
        query = "UPDATE turmas SET nome=?, nome_curso=?, data_inicio=? WHERE id=?"
        cur.execute(query, i)

#Deletar Turma (Delete D)
def deletar_turma(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM turmas WHERE id=?"
        cur.execute(query, i)

#Tabela Aluno --------------------------------------------------------------------------
#Criar Aluno (Create C)
def criar_aluno(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO alunos (nome, email, telefone, sexo, imagem, data_nascimento, cpf, nome_turma) VALUES (?, ?, ?, ?, ?, ?, ? ,?)"
        cur.execute(query, i)

#Ver Alunoa (Read R)
def ver_aluno():
    lista = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM alunos"
        cur.execute(query)
        linha = cur.fetchall()

        for i in linha:
            lista.append(i)
    return lista

#Atualizar Alunos (Update U)
def atualiza_aluno(i):
    with con:
        cur = con.cursor()
        query = "UPDATE alunos SET nome=?, email=?, telefone=?, sexo=?, imagem=?, data_nascimento=?, cpf=?, nome_turma=? WHERE id=?"
        cur.execute(query, i)

#Remover Aluno (Delete D)
def deletar_aluno(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM alunos WHERE id=?"
        cur.execute(query, i)