import tkinter as tk
from PIL import ImageTk,Image  
import psycopg2
from tkinter import ttk
import select

connection = None
cursor = None  
b = [False, False, False, False, False]
pressed = 1

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

        global b
        page = str(self)[len(str(self))-1]
        #print(page)
        for i in range (len(b)):
            if i+1 == int(page):
                b[i] = True
            else:
                b[i] = False
        #print(b)

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global connection, cursor

        #Username
        self.container1_1 = tk.Frame(self)
        self.container1_1["padx"] = 30
        self.container1_1["pady"] = 10
        self.container1_1.pack()
        #Password
        self.container1_2 = tk.Frame(self)
        self.container1_2["padx"] = 20
        self.container1_2["pady"] = 10
        self.container1_2.pack()
        #Button
        self.container1_3 = tk.Frame(self)
        self.container1_3["pady"] = 10
        self.container1_3.pack()
        #Message
        self.container1_4 = tk.Frame(self)
        self.container1_4.pack()

        def logintodb(): 
            global connection, cursor

            user = self.username_entry.get()
            passw = self.password_entry.get()

            print(f"Entrada: {user} {passw}")

            try:
                print('Connecting to the PostgreSQL database...')
                connection = psycopg2.connect(dbname="bd_rhsemear", user=user, password=passw)
                connection.autocommit = True
            
                cursor = connection.cursor()
                
                #print('PostgreSQL database version:')
                cursor.execute('SELECT version()')

                db_version = cursor.fetchone()
                print(db_version)

                print('Conectado com sucesso!\n')

                self.message.destroy()
                self.message = tk.Label(self.container1_4, text="Login bem sucedido!")
                self.message["fg"] = ("#007f46")
                self.message.pack()
            
            except (Exception, psycopg2.DatabaseError) as error:
                self.message.destroy()
                self.message = tk.Label(self.container1_4, text=error)
                self.message["fg"] = ("red")
                self.message.pack()

                print(error)

        self.username = tk.Label(self.container1_1, text ="Usuário")
        self.username["font"] = ("Quicksand", "10")
        self.username["fg"] = ("black")
        self.username.place(in_=self.container1_1, x=0, y=30, relwidth=1, relheight=3)
        self.username.pack(side = "top")

        self.username_entry = tk.Entry(self.container1_1, width = 15)
        self.username_entry["font"] = ("Quicksand", "10")
        self.username_entry["fg"] = ("black")
        self.username_entry.pack(side = "top")

        self.password = tk.Label(self.container1_2, text ="Senha")
        self.password["font"] = ("Quicksand", "10")
        self.password["fg"] = ("black")
        self.password.pack(side = "top")

        self.password_entry = tk.Entry(self.container1_2, width = 15)
        self.password_entry["font"] = ("Quicksand", "10")
        self.password_entry["fg"] = ("black")
        self.password_entry.pack(side = "top")

        self.button = tk.Button(self.container1_3, text ="Login", bg ='#007f46', command = logintodb)
        self.button["font"] = ("Quicksand", "10", "bold")
        self.button["fg"] = ("white")
        self.button.pack()

        self.message = tk.Label(self.container1_4, text ="")
        self.message["font"] = ("Quicksand", "10", "bold")
        self.message.pack()

class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pass

class Page2_1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global connection, cursor

        #Parâmetros
        self.container2_1_1 = tk.Frame(self)
        self.container2_1_1.pack()

        #Botao
        self.container2_1_2 = tk.Frame(self)
        self.container2_1_2["pady"] = 20
        self.container2_1_2.pack()

        #Tabela de dados
        self.container2_1_3 = tk.Frame(self)
        self.container2_1_3["pady"] = 20
        self.container2_1_3.pack()

        self.tipo_membro = tk.Label(self.container2_1_1, text ="Tipo de membro")
        self.tipo_membro["font"] = ("Quicksand", "10")
        self.tipo_membro["fg"] = ("black")
        self.tipo_membro.place(in_=self.container2_1_1, x=0, y=30, relwidth=1, relheight=3)
        self.tipo_membro.pack(side = "left")

        self.tipo_membro_entry = tk.Entry(self.container2_1_1, width = 15)
        self.tipo_membro_entry["font"] = ("Quicksand", "10")
        self.tipo_membro_entry["fg"] = ("black")
        self.tipo_membro_entry.pack(side = "left")

        self.nucleo = tk.Label(self.container2_1_1, text ="Núcleo")
        self.nucleo["font"] = ("Quicksand", "10")
        self.nucleo["fg"] = ("black")
        self.nucleo.pack(side = "left")

        self.nucleo_entry = tk.Entry(self.container2_1_1, width = 15)
        self.nucleo_entry["font"] = ("Quicksand", "10")
        self.nucleo_entry["fg"] = ("black")
        self.nucleo_entry.pack(side = "left")

        def callback():
            print(str(cursor))
            table = select.func2_5(cursor, self.tipo_membro_entry.get(),self.nucleo_entry.get())
            #print (self.table)
            print('oi')

            n_rows = len(table)
            n_cols = len(table[0])

            print(str(table))
            print(n_rows)
            print(n_cols)

            row = []
            for i in range(n_rows):
                col = []
                for j in range(n_cols):
                    cell = tk.Entry(self.container2_1_3,relief="groove")
                    cell.grid(row=i, column=j, sticky="nsew")
                    cell.insert("end", '%s' % (table[i][j]))
                    col.append(cell)


        self.botao = tk.Button(self.container2_1_2, text='Consultar', bg ='#007f46',command = callback)
        self.botao["font"] = ("Quicksand", "10", "bold")
        self.botao["fg"] = ("white")
        self.botao.pack(expand = True, side="left")
      
class Page2_2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #NUSP
        self.container2_1_1 = tk.Frame(self)
        self.container2_1_1["padx"] = 10
        self.container2_1_1["pady"] = 10
        self.container2_1_1.pack()

        #Resposta
        self.container2_1_2 = tk.Frame(self)
        self.container2_1_2["padx"] = 10
        self.container2_1_2["pady"] = 10
        self.container2_1_2.pack()

        def busca():
            pass

        self.nUSP_text = tk.Label(self.container2_1_1, text ="N USP")
        self.nUSP_text["font"] = ("Quicksand", "10")
        self.nUSP_text["fg"] = ("black")
        self.nUSP_text.place(in_=self.container2_1_1, x=0, y=30, relwidth=1, relheight=3)
        self.nUSP_text.pack(side = "left")

        self.nUSP_text = tk.Entry(self.container2_1_1, width = 15)
        self.nUSP_text["font"] = ("Quicksand", "10")
        self.nUSP_text["fg"] = ("black")
        self.nUSP_text.place(in_=self.container2_1_1, x=0, y=30, relwidth=1, relheight=3)
        self.nUSP_text.pack(side = "left")

        self.button = tk.Button(self.container2_1_1, text ="Login", bg ='#007f46', command = busca)
        self.button["font"] = ("Quicksand", "10", "bold")
        self.button["fg"] = ("white")
        self.button.pack(side = "left")

        self.message = tk.Label(self.container2_1_2, text ="")
        self.message["font"] = ("Quicksand", "10", "bold")
        self.message.pack()

class Page2_3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global connection, cursor

        #Parâmetros
        self.container2_3_1 = tk.Frame(self)
        self.container2_3_1.pack()

        #Botao
        self.container2_3_2 = tk.Frame(self)
        self.container2_3_2["pady"] = 20
        self.container2_3_2.pack()

        #Tabela de dados
        self.container2_3_3 = tk.Frame(self)
        self.container2_3_3["pady"] = 20
        self.container2_3_3.pack()

        self.membroNUSP = tk.Label(self.container2_3_1, text ="NUSP")
        self.membroNUSP["font"] = ("Quicksand", "10")
        self.membroNUSP["fg"] = ("black")
        self.membroNUSP.place(in_=self.container2_3_1, x=0, y=30, relwidth=1, relheight=3)
        self.membroNUSP.pack(side = "left")

        self.membroNUSP_entry = tk.Entry(self.container2_3_1, width = 15)
        self.membroNUSP_entry["font"] = ("Quicksand", "10")
        self.membroNUSP_entry["fg"] = ("black")
        self.membroNUSP_entry.pack(side = "left")


        def callback():
            print(str(cursor))
            table = select.func2_3(cursor, self.membroNUSP_entry.get())
            #print (self.table)
            print('oi')

            n_rows = len(table)
            n_cols = len(table[0])

            print(str(table))
            print(n_rows)
            print(n_cols)

            row = []
            for i in range(n_rows):
                col = []
                for j in range(n_cols):
                    cell = tk.Entry(self.container2_3_3,relief="groove")
                    cell.grid(row=i, column=j, sticky="nsew")
                    cell.insert("end", '%s' % (table[i][j]))
                    col.append(cell)


        self.botao = tk.Button(self.container2_3_2, text='Consultar', bg ='#007f46',command = callback)
        self.botao["font"] = ("Quicksand", "10", "bold")
        self.botao["fg"] = ("white")
        self.botao.pack(expand = True, side="left")
      

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pass

class Page3_1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #label = tk.Label(self, text="Página de inserção de registros")
        #label.pack(side="top", fill="both", expand=True)
        global connection, cursor

        #Linha 1
        self.container3_1_1 = tk.Frame(self)
        self.container3_1_1.pack()

        #Linha 2
        self.container3_1_2 = tk.Frame(self)
        self.container3_1_2.pack()

        #Linha 3
        self.container3_1_3 = tk.Frame(self)
        self.container3_1_3.pack()

        #Linha 4
        self.container3_1_4 = tk.Frame(self)
        self.container3_1_4.pack()

        #Linha 5
        self.container3_1_5 = tk.Frame(self)
        self.container3_1_5.pack()

        #Linha 6
        self.container3_1_6 = tk.Frame(self)
        self.container3_1_6["pady"] = 30
        self.container3_1_6.pack()

        #Linha 7
        self.container3_1_7 = tk.Frame(self)
        self.container3_1_7.pack()

        self.nome_projeto = tk.Label(self.container3_1_1, text ="Nome do projeto", width=20)
        self.nome_projeto["font"] = ("Quicksand", "10")
        self.nome_projeto["fg"] = ("black")
        self.nome_projeto.place(in_=self.container3_1_1, x=0, y=30, relwidth=1, relheight=3)
        self.nome_projeto.pack(side = "left")

        self.nome_projeto_entry = tk.Entry(self.container3_1_1)
        self.nome_projeto_entry["font"] = ("Quicksand", "10")
        self.nome_projeto_entry["fg"] = ("black")
        self.nome_projeto_entry.pack(side = "left", fill="x", expand=True)

        self.tipo_principal = tk.Label(self.container3_1_2, text ="Tipo", width=20)
        self.tipo_principal["font"] = ("Quicksand", "10")
        self.tipo_principal["fg"] = ("black")
        self.tipo_principal.pack(side = "left")

        self.tipo_principal_entry = tk.Entry(self.container3_1_2)
        self.tipo_principal_entry["font"] = ("Quicksand", "10")
        self.tipo_principal_entry["fg"] = ("black")
        self.tipo_principal_entry.pack(side = "left", fill="x", expand=True)

        self.descricao = tk.Label(self.container3_1_3, text ="Descricao", width=20)
        self.descricao["font"] = ("Quicksand", "10")
        self.descricao["fg"] = ("black")
        self.descricao.pack(side = "left")

        self.descricao_entry = tk.Entry(self.container3_1_3)
        self.descricao_entry["font"] = ("Quicksand", "10")
        self.descricao_entry["fg"] = ("black")
        self.descricao_entry.pack(side = "left", fill="x", expand=True)

        self.dataabertura = tk.Label(self.container3_1_4, text ="Data de abertura", width=20)
        self.dataabertura["font"] = ("Quicksand", "10")
        self.dataabertura["fg"] = ("black")
        self.dataabertura.pack(side = "left")

        self.dataabertura_entry = tk.Entry(self.container3_1_4)
        self.dataabertura_entry["font"] = ("Quicksand", "10")
        self.dataabertura_entry["fg"] = ("black")
        self.dataabertura_entry.pack(side = "left", fill="x", expand=True)

        self.nucleo = tk.Label(self.container3_1_5, text ="Núcleo", width=20)
        self.nucleo["font"] = ("Quicksand", "10")
        self.nucleo["fg"] = ("black")
        self.nucleo.pack(side = "left")

        self.nucleo_entry = tk.Entry(self.container3_1_5)
        self.nucleo_entry["font"] = ("Quicksand", "10")
        self.nucleo_entry["fg"] = ("black")
        self.nucleo_entry.pack(side = "left", fill="x", expand=True)

        def callback():
            global cursor
            result = select.func2_4(cursor, self.nome_projeto_entry.get(),self.tipo_principal_entry.get(),self.descricao_entry.get(),self.dataabertura_entry.get(),self.nucleo_entry.get())

            self.message.destroy()

            if ( result == 'no results to fetch'):
                self.message = tk.Label(self.container3_1_7, text='Inserção bem sucedida!')
                self.message["fg"] = ("#007f46")
                self.message.pack()
            else:
                self.message = tk.Label(self.container3_1_7, text=str(result))
                self.message["fg"] = ("red")
                self.message.pack()


        self.botao = tk.Button(self.container3_1_6, text='Criar', bg ='#007f46',command = callback)
        self.botao["font"] = ("Quicksand", "10", "bold")
        self.botao["fg"] = ("white")
        self.botao.pack(expand = True, side="left")

        self.message = tk.Label(self.container3_1_7, text ="")
        self.message["font"] = ("Quicksand", "10", "bold")
        self.message.pack()


class Page4(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Página de atualização de registros")
       label.pack(side="top", fill="both", expand=True)

class Page5(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Página de remoção de registros")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        global b

        #Imagem
        self.container0 = tk.Frame(self)
        self.container0.pack()
        #Titulo
        self.container1 = tk.Frame(self)
        self.container1.pack()
        #Menu
        self.container2 = tk.Frame(self)
        self.container2["padx"] = 30
        self.container2.pack(side="top", fill="x", expand=False)
        #Opções
        self.container3 = tk.Frame(self)
        self.container3["padx"] = 30
        self.container3["pady"] = 30
        self.container3.pack(side="top", fill="x", expand=False)
        #Frame
        self.container4 = tk.Frame(self)
        self.container4.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self.container0, width = 200, height = 70)      
        self.canvas.pack()      
        self.img = ImageTk.PhotoImage(Image.open("logo_semear.PNG"))  
        self.canvas.create_image(20,20, anchor=tk.NW, image=self.img) 
        self.canvas.pack()   

        self.titulo = tk.Label(self.container1, text="Banco de Dados RH")
        self.titulo["font"] = ("Quicksand", "12", "bold")
        self.titulo["fg"] = ("#007f46")
        self.titulo.pack ()

        p1 = Page1(self)
        p2 = Page2(self)
        p2_1 = Page2_1(self)
        p2_3 = Page2_3(self)
        p3 = Page3(self)
        p3_1 = Page3_1(self)
        p4 = Page4(self)
        p5 = Page5(self)

        p1.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p2_1.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p2_3.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p3_1.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=self.container4, x=0, y=0, relwidth=1, relheight=1)

        def callback(eventObject): # callback de todos os botões, para manter controle sobre qual o último pressionado
            global b
            global pressed
            pressed = 0
            for i in range(len(b)):
                if b[i] == True:
                    pressed = i+1
            print(pressed)

        def callback2(eventObject): # callback para atualizar a lista suspensa de opções com base no último botão pressionado
            self.option_menu.config(values=options_list[pressed-1])
        
        def callback3(eventObject): # callback de selecionar
            option = str(eventObject)

            if option == options_list[1][0]:
                pass
            elif option == options_list[1][1]:
                p2_1.show()
            elif option == options_list[1][3]:
                p2_3.show()
            elif option == options_list[2][3]:
                p3_1.show()

        self.funcao_login = tk.Button(self.container2, text="Login", command=p1.show)
        self.funcao_login["font"] = ("Quicksand", "10", "bold")
        self.funcao_login["bg"] = ("black")
        self.funcao_login["fg"] = ("white")
        self.funcao_login.bind('<Button-1>', callback)
        self.funcao_login.pack(expand = True, fill="x", side="left")
  
        self.funcao_consultar= tk.Button(self.container2, text="Consultar", command=p2.show)
        self.funcao_consultar["font"] = ("Quicksand", "10", "bold")
        self.funcao_consultar["bg"] = ("#007f46")
        self.funcao_consultar["fg"] = ("white")
        self.funcao_consultar.bind('<Button-1>', callback)
        self.funcao_consultar.pack(expand = True, fill="x", side="left")

        self.funcao_inserir = tk.Button(self.container2, text="Inserir", command=p3.show)
        self.funcao_inserir["font"] = ("Quicksand", "10", "bold")
        self.funcao_inserir["bg"] = ("#007f46")
        self.funcao_inserir["fg"] = ("white")
        self.funcao_inserir.bind('<Button-1>', callback)
        self.funcao_inserir.pack(expand = True, fill="x", side="left")

        self.funcao_atualizar = tk.Button(self.container2, text="Atualizar", command=p4.show)
        self.funcao_atualizar["font"] = ("Quicksand", "10", "bold")
        self.funcao_atualizar["bg"] = ("#007f46")
        self.funcao_atualizar["fg"] = ("white")
        self.funcao_atualizar.bind('<Button-1>', callback)
        self.funcao_atualizar.pack(expand = True, fill="x", side="left")

        self.funcao_remover = tk.Button(self.container2, text="Remover", command=p5.show)
        self.funcao_remover["font"] = ("Quicksand", "10", "bold")
        self.funcao_remover["bg"] = ("#007f46")
        self.funcao_remover["fg"] = ("white")
        self.funcao_remover.bind('<Button-1>', callback)
        self.funcao_remover.pack(expand = True, fill="x", side="left")

        self.funcao_sair = tk.Button(self.container2, text="Sair", command=self.quit)
        self.funcao_sair["font"] = ("Quicksand", "10", "bold")
        self.funcao_sair["bg"] = ("black")
        self.funcao_sair["fg"] = ("white")
        self.funcao_sair.pack(expand = True, fill="x", side="left")

        options_list = [
        ["Sem opções"],
        ["Opções de consulta","01: Lista de membros (por tipo, por núcleo, por comitê, por projeto)", 
        "02: Informações pessoais de um membro", "03: Posições atuais de um membro no grupo (núcleos, comitês, projetos)", 
        "04: Histórico de cargos de um membro no grupo","05: Lista de professores",
        "06: Projetos abertos de um núcleo", "07: Competições por ano", "08: Resultados de uma competição"],
        ["Opções de inserção","01: Membro", "02: Status de Membro", "03: Projeto", "04: Competição", "05: Posição Núcleo", "06: Posição Comitê", "07: Posição Projeto"],
        ["Indisponível"],
        ["Indisponível"]
        ]
        
        self.option_menu = ttk.Combobox(self.container3, width=50)
        self.option_menu["font"] = ("Quicksand", "10", "bold")
        self.option_menu.bind('<Button-1>', callback2)
        self.option_menu.pack(expand = True, fill="x", side="top")

        self.funcao_selecionar = tk.Button(self.container3, text='Selecionar', bg ='#007f46',command=lambda: callback3(self.option_menu.get()))
        self.funcao_selecionar["font"] = ("Quicksand", "10", "bold")
        self.funcao_selecionar["fg"] = ("white")
        self.funcao_selecionar.pack(expand = True, side="top")

        p1.show()
    