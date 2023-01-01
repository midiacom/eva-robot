from tkinter import *
from tkinter import messagebox
import tkinter
from  tkinter import ttk # usando tabelas

# closing application
def on_closing(window):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("Eva says: Bye bye!")
        window.destroy()

# classe da interface grafica do usuario
class Gui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        parent.title("Eva Simulator for EvaML - Version 1.0 - UFF/MidiaCom/CICESE")
        self.w = 1200
        self.h = 550  # on linux use 525 # on windows use 550
        parent.geometry(str(self.w) + "x" + str(self.h))

        # define the closing app function
        parent.protocol("WM_DELETE_WINDOW", lambda: on_closing(parent)) 

        # does not show the min button
        parent.resizable(0,0)

        # fonte tamanho 9 para botoes e textos em geral
        self.font1 = ('Arial', 9)

        #setting the default font for applicantion
        parent.option_add( "*font", "Arial 9")

        # define o frame para a imagem do robô
        self.frame_robot = tkinter.Frame(master=parent, width= 400, height=self.h)
        self.frame_robot.pack(pady= 22, side=tkinter.LEFT)

        # criando o canvas gráfico
        self.canvas = Canvas(self.frame_robot, width = 400, height = self.h) # o canvas e' necessario para usar imagens com transparencia
        self.canvas.pack()

        # define o frame para o terminal e o menu de botões
        self.frame_centro = tkinter.Frame(master=parent, width= 530, height=self.h)
        self.frame_centro.pack(fill=tkinter.Y, side=tkinter.LEFT)

        # define o frame para as tabelas de memória
        self.frame_memory = tkinter.Frame(master=parent, width= 180, height=self.h)
        self.frame_memory.place(x=938, y=60)

        # define o frame para o menu de botões
        self.frame_botoes = tkinter.Frame(master=self.frame_centro)
        self.frame_botoes.pack(pady=15, padx=10)

        # define o frame para o terminal
        self.frame_terminal = tkinter.Frame(master=self.frame_centro, height=400)
        self.frame_terminal.pack(fill=tkinter.X)

        # cria a tabela de memoria
        # define as propriedads da tabela com o mapa de memoria de $
        tkinter.Label(self.frame_memory, bg="gray70", width="34", font = self.font1, text="System Variables $ (Memory Map)", pady=1).pack()

        # define o estilo das tabelas
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 8), rowheight=15) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Arial', 8,'bold')) # Modify the font of the headings
        self.tab_dollar = ttk.Treeview(self.frame_memory, style="mystyle.Treeview", height=15)
        self.tab_dollar.pack()

        self.tab_dollar['columns']= ('Index', 'Content', "Source")
        self.tab_dollar.column("#0", width=0,  stretch=NO)
        self.tab_dollar.column("Index",anchor=CENTER, width=45)
        self.tab_dollar.column("Content",anchor=CENTER, width=107)
        self.tab_dollar.column("Source",anchor=CENTER, width=90)

        self.tab_dollar.heading("#0",text="",anchor=CENTER)
        self.tab_dollar.heading("Index",text="Index",anchor=CENTER)
        self.tab_dollar.heading("Content",text="Content",anchor=CENTER)
        self.tab_dollar.heading("Source",text="Source",anchor=CENTER)

        # label so pra separar as tabelas
        tkinter.Label(self.frame_memory, text="", font = ('Arial', 6)).pack()

        # define as propriedades da tabela com o mapa de memoria de variaveis do usuario
        tkinter.Label(self.frame_memory, width="34", bg="gray70", font = self.font1, text="User Variables (Memory Map)", pady=1).pack()
        self.tab_vars = ttk.Treeview(self.frame_memory, style="mystyle.Treeview", height=9)
        self.tab_vars.pack(fill=tkinter.Y)

        self.tab_vars['columns']= ('Var', 'Value')
        self.tab_vars.column("#0", width=0,  stretch=NO)
        self.tab_vars.column("Var", anchor=CENTER, width=130)
        self.tab_vars.column("Value", anchor=CENTER, width=110)

        self.tab_vars.heading("#0",text="",anchor=CENTER)
        self.tab_vars.heading("Var", text="Var",anchor=CENTER)
        self.tab_vars.heading("Value",text="Value",anchor=CENTER)

        # Defining the image files
        self.eva_image = PhotoImage(file = "images/eva.png") 
        self.bulb_image = PhotoImage(file = "images/bulb.png")
        # eva expressions images
        self.im_eyes_neutral = PhotoImage(file = "images/eyes_neutral.png")
        self.im_eyes_angry = PhotoImage(file = "images/eyes_angry.png")
        self.im_eyes_sad = PhotoImage(file = "images/eyes_sad.png")
        self.im_eyes_happy = PhotoImage(file = "images/eyes_happy.png")
        self.im_eyes_on = PhotoImage(file = "images/eyes_on.png")
        # matrix voice images
        self.im_matrix_blue = PhotoImage(file = "images/matrix_blue.png")
        self.im_matrix_green = PhotoImage(file = "images/matrix_green.png")
        self.im_matrix_yellow = PhotoImage(file = "images/matrix_yellow.png")
        self.im_matrix_white = PhotoImage(file = "images/matrix_white.png")
        self.im_matrix_red = PhotoImage(file = "images/matrix_red.png")
        self.im_matrix_grey = PhotoImage(file = "images/matrix_grey.png")
        self.im_bt_play = PhotoImage(file = "images/bt_play.png")
        self.im_bt_stop = PhotoImage(file = "images/bt_stop.png")
        # desenha o eva e a lampada desligada
        self.canvas.create_image(160, 262, image = self.eva_image)
        self.canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        self.canvas.create_image(340, 285, image = self.bulb_image)


        # criacao dos botoes da interface com usuário
        self.bt_padx = 3 # ajuste de espaçamento entre botões
        self.bt_power = Button (self.frame_botoes, text = "    Power On    ", font = self.font1)
        self.bt_power.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_import = Button (self.frame_botoes, text = "    Import Script File...    ", font = self.font1, state = DISABLED)
        self.bt_import.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_run = Button (self.frame_botoes, text = "    Run    ", image = self.im_bt_play, font = self.font1, state = DISABLED, compound = LEFT)
        self.bt_run.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_stop = Button (self.frame_botoes, text = "    Stop    ", font = self.font1, image = self.im_bt_stop, state = DISABLED, compound = LEFT)
        self.bt_stop.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_clear = Button (self.frame_botoes, text = "  Clear Terminal  ", font = self.font1, state = NORMAL, compound = LEFT)
        self.bt_clear.pack(side=tkinter.LEFT, padx=self.bt_padx)

        # Terminal text configuration
        self.terminal = Text (self.frame_terminal, fg = "cyan", bg = "black", height = "34", width = "85")
        self.terminal.configure(font = ("Arial", 8))
        self.terminal.tag_configure("error", foreground="red")
        self.terminal.tag_configure("motion", foreground="orange")
        self.terminal.tag_configure("tip", foreground="yellow")
        # limpa, desenha e coloca terminal no frame dele
        self.terminal.delete('1.0', END)
        # criando terminal text
        self.terminal.insert(INSERT, "=====================================================================================\n")
        self.terminal.insert(INSERT, "                                                                Eva Simulator for EvaML\n")
        self.terminal.insert(INSERT, "                                                Version 1.0 - UFF/MidiaCom/CICESE [2022]\n")
        self.terminal.insert(INSERT, "=====================================================================================")

        self.terminal.pack()

        # Desenha o eva e a lampada desligada
        # Defining the image files
        self.eva_image = PhotoImage(file = "images/eva.png") 
        self.bulb_image = PhotoImage(file = "images/bulb.png")
        self.canvas.create_image(160, 262, image = self.eva_image)
        self.canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        self.canvas.create_image(340, 285, image = self.bulb_image)
