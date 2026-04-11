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

print(ver_cursos())

#Atualizar Cursos (Uptade U)
def atualizar_curso(i):
    with con:
        cur = con.cursor()
        query = "UPDATE Cursos SET nome=?, duracao=?, preco=? WHERE id=?"
        cur.execute(query,i)

#atualizar_curso(l)

#Deletar Cursos (Delete D)
def deletar_curso(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Cursos WHERE id=?"
        cur.execute(query, i)

#deletar_curso([1])