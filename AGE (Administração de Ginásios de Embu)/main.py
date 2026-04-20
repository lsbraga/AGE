#Bibliotecas

#Tinker
import tkinter as Tk
from tkinter.ttk import *
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

#Pillow
import os
from PIL import ImageTk, Image

#tk calendario
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import date

#importando vie-
from view import *

#Fazer cópia fotos
import os
import shutil

#exportação
import pandas as pd
from fpdf import FPDF

# 1. Pega o caminho de onde o seu script main.py está salvo
diretorio_atual = os.path.dirname(__file__)

# 2. Define o nome e o caminho da pasta de fotos (dentro do seu projeto)
pasta_fotos = os.path.join(diretorio_atual, "fotos_alunos")

# 3. Verifica se a pasta já existe. Se não existir, o Python cria ela agora!
if not os.path.exists(pasta_fotos):
    os.makedirs(pasta_fotos)
    print(f"Pasta criada em: {pasta_fotos}")
else:
    print("A pasta fotos_alunos já existe e está pronta.")

imagem_string = "" 
l_imagem = None # Será inicializada abaixo

diretorio_atual = os.path.dirname(__file__)
caminho_imagem = os.path.join(diretorio_atual, "logo.png")
caminho_add = os.path.join(diretorio_atual, "adicionar.png")
caminho_slv = os.path.join(diretorio_atual, "salvar.png")

#Cores
co0 = "#2e2d2b" #Preta
co1 = "#feffff" #Branco
co2 = "#e5e5e5" #Cinza
co3 = "#00a095" #Verde
co4 = "#403d3d" #Letra
co6 = "#003452" #Azul
co7 = "#ef5350" #Vermelho

co6 = "#038cfc" #Azul
co8 = "#263238" #Verde Escuro
co9 = "#e9edf5" #Verde +Escuro
co11 = "#9ffcd1"

#Janela 
janela = Tk()
janela.title("AGE - Administração de Ginásios de Embu -  Beta")
janela.geometry("1920x1080")
janela.configure(background=co11)
janela.resizable(width=TRUE, height=TRUE)

sytle = Style(janela)
sytle.theme_use("clam")

#Criando Frames (Separação da tela)
frame_logo = Frame(janela, width=1920, height=80, bg=co3)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=1, columnspan=1, ipadx=680)

frame_dados = Frame(janela, width=1920, height=85, bg=co11)
frame_dados.grid(row=2, column=0, pady=0, padx=0, sticky=NSEW)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=3, columnspan=1, ipadx=680)

frame_detalhes = Frame(janela, width=1920, height=200, bg=co11)
frame_detalhes.grid(row=4, column=0, pady=0, padx=10, sticky=NSEW)

frame_tabela = Frame(janela, width=1920, height=200, bg=co11)
frame_tabela.grid(row=5, column=0, pady=0, padx=10, sticky=NSEW)

#Fazendo a frame logo
app_lg = Image.open(caminho_imagem)
app_lg = app_lg.resize((95, 95))
app_lg = ImageTk.PhotoImage(app_lg)
app_logo = Label(frame_logo, image=app_lg, text="Cadastro de Alunos", width=1920, compound=LEFT, relief=RAISED, anchor=NW, font=("Ivy 15 bold"), bg=co3, fg=co1)
app_logo.place(x=0, y=0)

#Função aluno para cadastro aluno
def alunos():

    #Função novo aluno
    def novo_aluno():
        global imagem, imagem_string, l_imagem

        nome = e_nome.get()
        endereco = e_endereco.get()
        telefone = e_tel.get()
        sexo = c_sexo.get()
        data = data_nascimento.get()
        cpf = e_cpf.get()
        curso = c_turma.get()
        imagem_para_db = ""

        #Salvar imagem
        if imagem_string:
            try:
                # 1. Descobrir a extensão do arquivo (ex: .jpg ou .png)
                extensao = os.path.splitext(imagem_string)[1]
                
                # 2. Criar o novo nome baseado no CPF: "123456789.jpg"
                nome_foto_final = f"{cpf}{extensao}"
                
                # 3. Definir o caminho completo de destino
                caminho_destino = os.path.join(pasta_fotos, nome_foto_final)
                
                # 4. Faz a cópia real do arquivo para a pasta do projeto
                shutil.copy(imagem_string, caminho_destino)
                
                # 5. O que vai para o Banco de Dados é o NOVO caminho (a cópia)
                imagem_para_db = caminho_destino
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao copiar foto: {e}")
                return
        else:
            messagebox.showerror("Erro", "Selecione uma foto primeiro")
            return
        
        lista = [nome, endereco, telefone, sexo, imagem_para_db, data, cpf, curso]

        #Vereficando caso algum campo esteja vazio ou não
        for i in lista:
            if i =="":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return
        
         #Inserindo os dados no db
        try:
            criar_aluno(lista)

            #mensagem de sucesso
            messagebox.showinfo("Sucesso", "Os dados foram inseridos com sucesso")

            #limpando os campos
            e_nome.delete(0, END)
            e_endereco.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.set("")
            data_nascimento.delete(0, END)
            e_cpf.delete(0, END)
            c_turma.set("")

            #Mostrar os dados na tabela alunos  
            mostrar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no Banco de Dados: {e}")  

    #Função atualizar alunos
    def update_aluno():
        global imagem, imagem_string, l_imagem
        
        try:
            tree_itens = tree_aluno.focus()
            tree_dicionario = tree_aluno.item(tree_itens)
            tree_lista = tree_dicionario['values']

            valor_id = tree_lista[0]

            #Limpando os campos de entrada
            e_nome.delete(0, END)
            e_endereco.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.delete(0, END)
            data_nascimento.delete(0, END)
            e_cpf.delete(0, END)
            c_turma.delete(0, END)

            #Inserindo os valores no campos de entrada
            e_nome.insert(0, tree_lista[1])
            e_endereco.insert(0, tree_lista[2])
            e_tel.insert(0, tree_lista[3])
            c_sexo.insert(0, tree_lista[4])
            data_nascimento.insert(0, tree_lista[6])
            e_cpf.insert(0, tree_lista[7])
            c_turma.insert(0, tree_lista[8])

            imagem = tree_lista[5]
            imagem_string = imagem

            #abrir imagem
            imagem = Image.open(imagem)
            imagem = imagem.resize((130, 130))
            imagem = ImageTk.PhotoImage(imagem)
            l_imagem = Label(frame_detalhes, image=imagem, bg=co1, fg=co4)
            l_imagem.place(x=300, y=10)

            def update():
                        global imagem, imagem_string, l_imagem

                        nome = e_nome.get()
                        endereco = e_endereco.get()
                        telefone = e_tel.get()
                        sexo = c_sexo.get()
                        data = data_nascimento.get()
                        cpf = e_cpf.get()
                        curso = c_turma.get()
                        imagem = imagem_string

                        lista = [nome, endereco, telefone, sexo, imagem, data, cpf, curso, valor_id]

                        #Vereficando caso algum campo esteja vazio ou não
                        for i in lista:
                            if i =="":
                                messagebox.showerror("Erro", "Preencha todos os campos")
                                return
                        
                        #Atualizadno os dados no db
                        atualiza_aluno(lista)

                        #mensagem de sucesso
                        messagebox.showinfo("Sucesso", "Os dados foram atualizados com sucesso")

                        #limpando os campos
                        e_nome.delete(0, END)
                        e_endereco.delete(0, END)
                        e_tel.delete(0, END)
                        c_sexo.delete(0, END)
                        data_nascimento.delete(0, END)
                        e_cpf.delete(0, END)
                        c_turma.delete(0, END)

                        #Mostrar os dados na tabela alunos
                        mostrar_alunos()

                        #destruindo botão após salvar
                        botao_update.destroy()
                    
            botao_update = Button(frame_detalhes,command=update, anchor=CENTER, text="Salvar atualização".upper(), width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co3, fg=co1)
            botao_update.place(x=727, y=130)
        
        except IndexError:
            messagebox.showerror("Erro", "Selecione um dos alunos na tabela")

    #Função deletar aluno
    def delete_alunos():
        try:
            tree_itens = tree_aluno.focus()
            tree_dicionario = tree_aluno.item(tree_itens)
            tree_lista = tree_dicionario['values']

            valor_id = tree_lista[0]

            #deletar os dados do db
            deletar_aluno([valor_id])

            #Mensagem de sucesso
            messagebox.showinfo("Sucesso", "Dados do aluno foi apagado")

            #mostrando os dados na tabela
            mostrar_alunos()

        except IndexError:
            messagebox.showerror ("Erro", "Selecione um aluno na tabela")

    def procurar_aluno_nome():
        nome_procurar = e_nome_procurar.get()
        
        # Obtém todos os alunos e filtra
        todos_alunos = ver_aluno()
        lista_filtrada = []

        for aluno in todos_alunos:
            # Verifica se o nome digitado está contido no nome do aluno (sem diferenciar maiúsculas)
            if nome_procurar.lower() in aluno[1].lower():
                lista_filtrada.append(aluno)

        # Limpa a Treeview atual
        for item in tree_aluno.get_children():
            tree_aluno.delete(item)

        # Insere apenas os resultados da busca
        for item in lista_filtrada:
            tree_aluno.insert('', 'end', values=item)

    def ver_detalhes_aluno():
        try:
            tree_itens = tree_aluno.focus()
            tree_dicionario = tree_aluno.item(tree_itens)
            tree_lista = tree_dicionario['values']

            if not tree_lista:
                messagebox.showerror("Erro", "Selecione um aluno na tabela primeiro")
                return

            # Limpando os campos antes de preencher
            e_nome.delete(0, END)
            e_endereco.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.set("") 
            data_nascimento.set_date(tree_lista[6]) # Assume que o formato no DB é compatível
            e_cpf.delete(0, END)
            c_turma.set("")

            # Preenchendo com os dados da tabela
            e_nome.insert(0, tree_lista[1])
            e_endereco.insert(0, tree_lista[2])
            e_tel.insert(0, tree_lista[3])
            c_sexo.set(tree_lista[4])
            e_cpf.insert(0, tree_lista[7])
            c_turma.set(tree_lista[8])

            # Carregar a imagem
            global imagem, imagem_string, l_imagem
            # Pegamos o nome do arquivo salvo no banco (ex: 123.jpg) e o CPF atual
            foto_no_banco = tree_lista[5]
            cpf_atual = tree_lista[7]
            extensao = os.path.splitext(foto_no_banco)[1]
            imagem_string = os.path.join(pasta_fotos, f"{cpf_atual}{extensao}")
            
            try:
                if os.path.exists(imagem_string):
                    caminho_final = imagem_string
                else:
                    caminho_final= foto_no_banco
                
                img_bruta = Image.open(caminho_final)
                img_bruta = img_bruta.resize((130, 130))
                imagem = ImageTk.PhotoImage(img_bruta)

                try:
                    l_imagem.configure(image=imagem)
                    l_imagem.image = imagem
                    l_imagem.place(x=300, y=10)
                except:
                    l_imagem = Label(frame_detalhes, image=imagem, bg=co1, fg=co4)
                    l_imagem.image = imagem
                    l_imagem.place(x=300, y=10) 
            except:
                try:
                    l_imagem.configure(image='')
                except:
                    pass
                messagebox.showwarning("Aviso", "A foto deste aluno não foi encontrada no computador.")

        except IndexError:
            messagebox.showerror("Erro", "Selecione um aluno na tabela")
    
    #criar campos de entrada
    l_nome = Label(frame_detalhes, text="Nome *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_nome.place(x=4, y=10)
    e_nome = Entry(frame_detalhes, width=45, justify="left", relief="solid")
    e_nome.place(x=7, y=40)

    l_endereco = Label(frame_detalhes, text="Endereço *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_endereco.place(x=4, y=70)
    e_endereco = Entry(frame_detalhes, width=45, justify="left", relief="solid")
    e_endereco.place(x=7, y=100)

    l_tel = Label(frame_detalhes, text="Telefone *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_tel.place(x=4, y=130)
    e_tel = Entry(frame_detalhes, width=20, justify="left", relief="solid")
    e_tel.place(x=7, y=160)

    #Sexo
    l_sexo = Label(frame_detalhes, text="Sexo *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_sexo.place(x=190, y=130)
    c_sexo = ttk.Combobox(frame_detalhes, width=12, font=("Ivy 8 bold"))
    c_sexo ["values"] = ("Masculino", "Feminino")
    c_sexo.place(x=190, y=160)

    #Data Nascimento
    l_data_nascimento = Label(frame_detalhes, text="Data de nascimento *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_data_nascimento.place(x=446, y= 10)
    data_nascimento = DateEntry(frame_detalhes, width=18, background='darkblue', foreground="white", borderwidth=2, year=2026, locale="pt_BR")
    data_nascimento.place(x=450, y=40)

    #cpf
    l_cpf = Label(frame_detalhes, text="CPF *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_cpf.place(x=446, y=70)
    e_cpf = Entry(frame_detalhes, width=20, justify="left", relief="solid")
    e_cpf.place(x=450, y=100)

    #Turma
    turmas = ver_turma()
    turma = []

    for i in turmas:
        turma.append(i[1])
    
    l_turma = Label(frame_detalhes, text="Turma *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_turma.place(x=446, y=130)
    c_turma = ttk.Combobox(frame_detalhes, width=20, font=("Ivy 8 bold"))
    c_turma['values'] = (turma)
    c_turma.place(x=450, y=160)

    #Função foto
    global imagem, imagem_string, l_imagem

    def escolher_imagem():
        global imagem, imagem_string, l_imagem

        caminho = fd.askopenfilename() 
        if not caminho:
            return

        imagem_string = caminho
        #abrindo a imagem
        try: 
            imagem = Image.open(caminho)
            imagem = imagem.resize((130, 130))
            imagem = ImageTk.PhotoImage(imagem)
            l_imagem = Label(frame_detalhes, image=imagem, bg=co4, fg=co1)
            l_imagem.place(x=300, y=10)

            botao_carregar['text'] = "Trocar de Foto".upper()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")
    botao_carregar = Button(frame_detalhes, command=escolher_imagem, text="Carregar Foto".upper(), width=20, compound=CENTER, anchor=CENTER, overrelief=RIDGE, font=("Ivy 7"), bg=co1, fg=co0)
    botao_carregar.place(x=300, y=160)

    #linha horizontal
    l_linha = Label(frame_detalhes, relief=GROOVE, text="h", width=1, height=100, anchor=NW, font="Ivy 1", bg=co0, fg=co0)
    l_linha.place(x=610, y=10)

    l_linha = Label(frame_detalhes, relief=GROOVE, text="h", width=1, height=100, anchor=NW, font="Ivy 1", bg=co1, fg=co0)
    l_linha.place(x=608, y=10)

    #Procurar Aluno
    l_nome = Label(frame_detalhes, text="Procurar Aluno", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_nome.place(x=627, y=10)
    e_nome_procurar = Entry(frame_detalhes, width=17, justify="center", relief="solid", font=("Ivy 10"))
    e_nome_procurar.place(x=630, y=35)

    botao_procurar = Button(frame_detalhes,command=procurar_aluno_nome, anchor=CENTER, text="Procurar", width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co1, fg=co0)
    botao_procurar.place(x=757, y=35)

    #botoes

    botao_salvar = Button(frame_detalhes,command=novo_aluno, anchor=CENTER, text="Salvar".upper(), width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co3, fg=co1)
    botao_salvar.place(x=627, y=110)

    botao_atualizar = Button(frame_detalhes,command=update_aluno, anchor=CENTER, text="Atualizar".upper(), width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co6, fg=co1)
    botao_atualizar.place(x=627, y=135)

    botao_deletar = Button(frame_detalhes,command=delete_alunos, anchor=CENTER, text="Deletar".upper(), width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co7, fg=co1)
    botao_deletar.place(x=627, y=160)

    botao_ver = Button(frame_detalhes,command=ver_detalhes_aluno, anchor=CENTER, text="Ver".upper(), width=9, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co1, fg=co0)
    botao_ver.place(x=727, y=110)

    #Tabela Alunos
    def mostrar_alunos():
        app_nome = Label(frame_tabela, text="Tabela de Alunos", height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co11, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

    #creating a treeview with dual scrollbars
    list_header = ['id', 'nome', 'endereço', 'telefone', 'sexo', 'imagem', 'data', 'cpf', 'curso']

    df_list = ver_aluno()

    global tree_aluno

    tree_aluno = ttk.Treeview(frame_tabela, selectmode="extended",columns=list_header, show="headings")

    #vertical scrollbar
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_aluno.yview)
    #horizontal scrollbar
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_aluno.xview)

    tree_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree_aluno.grid(column=0, row=1, sticky='nsew')
    vsb.grid(column=1, row=1, sticky='ns')
    hsb.grid(column=0, row=2, sticky='ew')
    frame_tabela.grid_rowconfigure(0, weight=12)

    hd=["nw","nw","nw","center","center","center","center","center","center"]
    h=[30, 180, 200, 100, 70, 70, 80, 100, 120]
    n=0

    for col in list_header:
        tree_aluno.heading(col, text=col.title(), anchor=NW)
    #adjust the column's width to the header string
        tree_aluno.column(col, width=h[n],anchor=hd[n])

        n+=1

    for item in df_list:
        tree_aluno.insert('', 'end', values=item)

    mostrar_alunos()

#Função para adicionar curso e turmas
def adicionar():
    global frame_tabela_curso, frame_tabela_linha, frame_tabela_turma
    #Criando frames
    frame_tabela_curso = Frame(frame_tabela, width=300, height=200, bg=co11)
    frame_tabela_curso.grid(row=0, column=0, pady=0, padx=10, sticky=NSEW)

    frame_tabela_linha = Frame(frame_tabela, width=30, height=200, bg=co11)
    frame_tabela_linha.grid(row=0, column=1, pady=0, padx=10, sticky=NSEW)

    frame_tabela_turma = Frame(frame_tabela, width=300, height=200, bg=co11)
    frame_tabela_turma.grid(row=0, column=2, pady=0, padx=10, sticky=NSEW)

#Função novo curso
    def novo_curso():
        nome = e_nome_curso.get()
        professor = e_professor.get()
        horario = e_horario.get()

        lista = [nome, professor, horario]

        # Verificando se os valores estão vazios
        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return
        
        #Inserindo os dados do db
        criar_curso(lista)
        messagebox.showinfo("Sucesso", "Dados foram cadastrados com sucesso")
        e_nome_curso.delete(0, END)
        e_professor.delete(0, END)
        e_horario.delete(0, END)

        mostrar_cursos()

#Funcao atualizar curso
    def update_curso():
        try:
            tree_itens = tree_curso.focus()
            tree_dicionario = tree_curso.item(tree_itens)
            tree_lista = tree_dicionario["values"]

            valor_id = tree_lista[0]

            #Inserindo os valores nas entries
            e_nome_curso.insert(0, tree_lista[1])
            e_professor.insert(0, tree_lista[2])
            e_horario.insert(0, tree_lista[3])

            #Função atualizar
            def update():
                nome = e_nome_curso.get()
                professor = e_professor.get()
                horario = e_horario.get()

                lista = [valor_id, nome, professor, horario]

                # Verificando se os valores estão vazios
                for i in lista:
                    if i == "":
                        messagebox.showerror("Erro", "Preencha todos os campos")
                        return
                
                #Inserindo os dados do db
                atualizar_curso(lista)
                #mensagem scucesso
                messagebox.showinfo("Sucesso", "Dados foram cadastrados com sucesso")
                e_nome_curso.delete(0, END)
                e_professor.delete(0, END)
                e_horario.delete(0, END)

                mostrar_cursos()

                #Destruindo botão salvar após salvar os dados
                botao_salvar.destroy()

            botao_salvar = Button(frame_detalhes,command=update, anchor=CENTER, text="Salvar Atualização".upper(), overrelief=RIDGE, font="Ivy 7 bold", bg=co3, fg=co1)
            botao_salvar.place(x=227, y=130)
        except IndexError:
            messagebox.showerror("Erro", "Selecione um dos cursos na tabela")

#Função deletar Cursos
    def delete_curso():
        try:
            tree_itens = tree_curso.focus()
            tree_dicionario = tree_curso.item(tree_itens)
            tree_lista = tree_dicionario ['values']

            valor_id = tree_lista[0]

            #Deletar o curso
            deletar_curso([valor_id])
            messagebox.showinfo("Sucesso", "Os dados foram apagados com sucesso")
            mostrar_cursos()

        except IndexError:
            messagebox.showerror("Erro", "Selecione um curso na tabela")


    l_nome = Label(frame_detalhes, text="Nome do Curso", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_nome.place(x=4, y=10)
    e_nome_curso = Entry(frame_detalhes, width=35, justify="left", relief="solid")
    e_nome_curso.place(x=7, y=40)

    l_professor = Label(frame_detalhes, text="Professor(a) *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_professor.place(x=4, y=70)
    e_professor = Entry(frame_detalhes, width=20, justify="left", relief="solid")
    e_professor.place(x=7, y=100)

    l_horario = Label(frame_detalhes, text="Horário *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_horario.place(x=4, y=130)
    e_horario = Entry(frame_detalhes, width=10, justify="left", relief="solid")
    e_horario.place(x=7, y=160)

    botao_carregar = Button(frame_detalhes, command=novo_curso, anchor=CENTER, text="Novo".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co3, fg=co1)
    botao_carregar.place(x=107, y=160)

    botao_atualizar = Button(frame_detalhes, command=update_curso, anchor=CENTER, text="Atualizar".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co6, fg=co1)
    botao_atualizar.place(x=187, y=160)

    botao_deletar = Button(frame_detalhes, command=delete_curso, anchor=CENTER, text="Deletar".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co7, fg=co1)
    botao_deletar.place(x=267, y=160)

    #linha horizontal
    l_linha = Label(frame_detalhes, relief=GROOVE, text="h", width=1, height=100, anchor=NW, font="Ivy 1", bg=co0, fg=co0)
    l_linha.place(x=374, y=10)

    l_linha = Label(frame_detalhes, relief=GROOVE, text="h", width=1, height=100, anchor=NW, font="Ivy 1", bg=co1, fg=co0)
    l_linha.place(x=372, y=10)

    #linha tabela
    l_linha = Label(frame_tabela_linha, relief=GROOVE, text="h", width=1, height=140, anchor=NW, font="Ivy 1", bg=co0, fg=co0)
    l_linha.place(x=6, y=10)

    l_linha = Label(frame_tabela_linha, relief=GROOVE, text="h", width=1, height=140, anchor=NW, font="Ivy 1", bg=co1, fg=co0)
    l_linha.place(x=4, y=10)


#Tabela cursos
    def mostrar_cursos():
        app_nome = Label(frame_tabela_curso, text="Tabela de Cursos", height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co11, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        #creating a treeview with dual scrollbars
        list_header = ['ID','Curso','Professor','Horario']

        df_list = ver_cursos()

        global tree_curso

        tree_curso = ttk.Treeview(frame_tabela_curso, selectmode="extended",columns=list_header, show="headings")

        #vertical scrollbar
        vsb = ttk.Scrollbar(frame_tabela_curso, orient="vertical", command=tree_curso.yview)
        #horizontal scrollbar
        hsb = ttk.Scrollbar(frame_tabela_curso, orient="horizontal", command=tree_curso.xview)

        tree_curso.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree_curso.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
        frame_tabela_curso.grid_rowconfigure(0, weight=12)

        hd=["nw","nw","e","e"]
        h=[30,150,80,60]
        n=0

        for col in list_header:
            tree_curso.heading(col, text=col.title(), anchor=NW)
            #adjust the column's width to the header string
            tree_curso.column(col, width=h[n],anchor=hd[n])

            n+=1

        for item in df_list:
            tree_curso.insert('', 'end', values=item)

    mostrar_cursos()

    #Nova turma
    def nova_turma():
        nome = e_nome_turma.get()
        curso = c_curso.get()
        data = data_inicio.get()

        lista = [nome, curso, data]

        # Verificando se os valores estão vazios
        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return
        
        #Inserindo os dados do db
        criar_turma(lista)
        messagebox.showinfo("Sucesso", "Dados foram cadastrados com sucesso")
        c_curso.delete(0, END)
        data_inicio.delete(0, END)

        mostrar_turmas()

    #Função atualizar TURMA
    def update_turma():  
        try:
            tree_itens = tree_turma.focus()
            tree_dicionario = tree_turma.item(tree_itens)
            tree_lista = tree_dicionario["values"]

            valor_id = tree_lista[0]

            #Inserindo os valores nas entries
            e_nome_turma.insert(0, tree_lista[1])
            c_curso.insert(0, tree_lista[2])
            data_inicio.insert(0, tree_lista[3])

            #Função atualizar
            def update():
                nome = e_nome_turma.get()
                curso = c_curso.get()
                data = data_inicio.get()

                lista = [valor_id, nome, curso, data]

                # Verificando se os valores estão vazios
                for i in lista:
                    if i == "":
                        messagebox.showerror("Erro", "Preencha todos os campos")
                        return
                
                #Inserindo os dados do db
                atualizar_turma(lista)
                #mensagem scucesso
                messagebox.showinfo("Sucesso", "Dados foram cadastrados com sucesso")
                e_nome_turma.delete(0, END)
                c_curso.delete(0, END)
                data_inicio.delete(0, END)

                mostrar_turmas()

                #Destruindo botão salvar após salvar os dados
                botao_salvar.destroy()

            botao_salvar = Button(frame_detalhes,command=update, anchor=CENTER, text="Salvar Atualização".upper(), overrelief=RIDGE, font="Ivy 7 bold", bg=co3, fg=co1)
            botao_salvar.place(x=407, y=130)
        except IndexError:
            messagebox.showerror("Erro", "Selecione um dos cursos na tabela")

    #Deletar turma
    def delete_turma():
        try:
            tree_itens = tree_turma.focus()
            tree_dicionario = tree_turma.item(tree_itens)
            tree_lista = tree_dicionario ['values']

            valor_id = tree_lista[0]

            #Deletar o curso
            deletar_turma([valor_id])
            messagebox.showinfo("Sucesso", "Os dados foram apagados com sucesso")
            mostrar_turmas()

        except IndexError:
            messagebox.showerror("Erro", "Selecione um curso na tabela")
    
    #detalhes turma
    l_nome = Label(frame_detalhes, text="Nome da Turma *", height=1, anchor=NW, font="Ivy 10", bg=co11, fg=co4)
    l_nome.place(x=404, y=10)
    e_nome_turma = Entry(frame_detalhes, width=35, justify="left", relief="solid")
    e_nome_turma.place(x=407, y=40)

    l_turma = Label(frame_detalhes, text="Nome da Turma *", height=1, anchor=NW, font="Ivy 10", bg=co11, fg=co4)
    l_turma.place(x=404, y=10)

    #pegando curso
    cursos = ver_cursos()
    curso = []

    for i in cursos:
        curso.append(i[1])
    
    c_curso = ttk.Combobox(frame_detalhes, width=20, font=("Ivy 8 bold"))
    c_curso['values'] = (curso)
    c_curso.place(x=407, y=100)

    l_data_inicio = Label(frame_detalhes, text="Data de inicio *", height=1, anchor=NW, font=("Ivy 10"), bg=co11, fg=co4)
    l_data_inicio.place(x=406, y= 130)
    data_inicio = DateEntry(frame_detalhes, width=10, background='darkblue', foreground="white", borderwidth=2, year=2026, locale="pt_BR")
    data_inicio.place(x=407, y=155)

    botao_carregar = Button(frame_detalhes, command=nova_turma, anchor=CENTER, text="Salvar".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co3, fg=co1)
    botao_carregar.place(x=507, y=160)

    botao_atualizar = Button(frame_detalhes,command=update_turma, anchor=CENTER, text="Atualizar".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co6, fg=co1)
    botao_atualizar.place(x=587, y=160)

    botao_deletar = Button(frame_detalhes,command=delete_turma, anchor=CENTER, text="Deletar".upper(), width=10, overrelief=RIDGE, font="Ivy 7 bold", bg=co7, fg=co1)
    botao_deletar.place(x=667, y=160)

    #Tabela turma
    def mostrar_turmas():
        app_nome = Label(frame_tabela_turma, text="Tabela de Cursos", height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co11, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        #creating a treeview with dual scrollbars
        list_header = ['id', 'nome', 'curso', 'data']

        df_list = ver_turma()

        global tree_turma

        tree_turma = ttk.Treeview(frame_tabela_turma, selectmode="extended",columns=list_header, show="headings")

        #vertical scrollbar
        vsb = ttk.Scrollbar(frame_tabela_turma, orient="vertical", command=tree_turma.yview)
        #horizontal scrollbar
        hsb = ttk.Scrollbar(frame_tabela_turma, orient="horizontal", command=tree_turma.xview)

        tree_turma.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree_turma.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
        frame_tabela_turma.grid_rowconfigure(0, weight=120)

        hd=["nw","nw","e","e"]
        h=[30,130,150,80]
        n=0

        for col in list_header:
            tree_turma.heading(col, text=col.title(), anchor=NW)
            #adjust the column's width to the header string
            tree_turma.column(col, width=h[n],anchor=hd[n])

            n+=1

        for item in df_list:
            tree_turma.insert('', 'end', values=item)

    mostrar_turmas()
#Função para salvar
def salvar():
    # Criar campos na tela de exportação
    l_tabela = Label(frame_detalhes, text="Escolha a tabela para exportar", font=("Ivy 10"), bg=co11, fg=co4)
    l_tabela.place(x=10, y=10)
    
    c_tabela = ttk.Combobox(frame_detalhes, width=20, font=("Ivy 10"))
    c_tabela['values'] = ("Alunos", "Cursos", "Turmas")
    c_tabela.place(x=10, y=40)

    # Função interna para processar a exportação
    def exportar(formato):
        tabela_selecionada = c_tabela.get()
        if not tabela_selecionada:
            messagebox.showerror("Erro", "Selecione uma tabela primeiro")
            return

        # Busca os dados corretos baseado na escolha
        if tabela_selecionada == "Alunos":
            dados = ver_aluno()
            colunas = ['ID', 'Nome', 'Email', 'Telefone', 'Sexo', 'Imagem', 'Data', 'CPF', 'Curso']
        elif tabela_selecionada == "Cursos":
            dados = ver_cursos()
            colunas = ['ID', 'Curso', 'Professor', 'Horario']
        else: # Turmas
            dados = ver_turma()
            colunas = ["ID", 'Nome', 'Curso', 'Data']

        if formato == "excel":
            exportar_para_excel(dados, colunas, tabela_selecionada)
        elif formato == "pdf":
            exportar_para_pdf(dados, colunas, tabela_selecionada)

    # Botões de exportação
    btn_excel = Button(frame_detalhes, command=lambda: exportar("excel"), text="Exportar Excel", width=15, bg="#228b22", fg=co1, font=("Ivy 8 bold"))
    btn_excel.place(x=10, y=80)

    btn_pdf = Button(frame_detalhes, command=lambda: exportar("pdf"), text="Exportar PDF", width=15, bg="#b22222", fg=co1, font=("Ivy 8 bold"))
    btn_pdf.place(x=140, y=80)

# --- FUNÇÕES DE APOIO (Coloque fora da função salvar) ---
def exportar_para_excel(dados, colunas, nome_arquivo):
    df = pd.DataFrame(dados, columns=colunas)
    filename = f"Relatorio_{nome_arquivo}.xlsx"
    df.to_excel(filename, index=False)
    messagebox.showinfo("Sucesso", f"Arquivo {filename} gerado com sucesso!")

def exportar_para_pdf(dados, colunas, nome_arquivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Título
    pdf.cell(200, 10, txt=f"Relatório de {nome_arquivo}", ln=True, align='C')
    pdf.ln(10)
    
    # Cabeçalho
    for col in colunas:
        pdf.cell(40, 10, str(col), 1)
    pdf.ln()

    # Dados
    for linha in dados:
        for item in linha:
            pdf.cell(40, 10, str(item), 1)
        pdf.ln()
    
    filename = f"Relatorio_{nome_arquivo}.pdf"
    pdf.output(filename)
    messagebox.showinfo("Sucesso", f"Arquivo {filename} gerado com sucesso!")


#Função de control

def control(i):
    #Cadastro de aluno
    if i == 'cadastro':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()

        #Chamando def alunos
        alunos()

    if i == 'adicionar':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()

        #Chamando def adicionar
        adicionar()
        
    if i == 'salvar':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()

        #Chamando def salvar
        salvar()

#Criando botão cadastro
app_img_cadastro = Image.open(caminho_add)
app_img_cadastro = app_img_cadastro.resize((18, 18))
app_img_cadastro = ImageTk.PhotoImage(app_img_cadastro)
app_cadastro = Button(frame_dados, command=lambda:control("cadastro"), image=app_img_cadastro, text="  Cadastro", width=100, compound=LEFT, overrelief=RIDGE, font=("Ivy 11"), bg=co1, fg=co0)
app_cadastro.place(x=10, y=30)

#Criando botão adicionar
app_img_adicionar = Image.open(caminho_add)
app_img_adicionar = app_img_adicionar.resize((18, 18))
app_img_adicionar = ImageTk.PhotoImage(app_img_adicionar)
app_adicionar = Button(frame_dados, command=lambda:control("adicionar"), image=app_img_adicionar, text="  Turmas", width=100, compound=LEFT, overrelief=RIDGE, font=("Ivy 11"), bg=co1, fg=co0)
app_adicionar.place(x=123, y=30)

#Criando botão salvar
app_img_salvar = Image.open(caminho_slv)
app_img_salvar = app_img_salvar.resize((18, 18))
app_img_salvar = ImageTk.PhotoImage(app_img_salvar)
app_salvar = Button(frame_dados, command=lambda:control("salvar"), image=app_img_salvar, text="  Exportar", width=100, compound=LEFT, overrelief=RIDGE, font=("Ivy 11"), bg=co1, fg=co0)
app_salvar.place(x=236, y=30)

# Botão Sair (Vermelho para destaque)
app_sair = Button(frame_dados, command=janela.destroy, text="Sair", width=12, overrelief=RIDGE, font=("Ivy 10 bold"), bg=co7, fg=co1)
app_sair.place(x=349, y=30) # Seguindo a sequência de X

janela.mainloop()