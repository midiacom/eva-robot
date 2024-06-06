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

        parent.title("Eva Simulator for EvaML - Version 2.0 - Google Research/UFF/MidiaCom/CICESE")
        self.w = 1690
        self.h = 910  # on linux use 525 # on windows use 550
        parent.geometry(str(self.w) + "x" + str(self.h))

        # define the closing app function
        parent.protocol("WM_DELETE_WINDOW", lambda: on_closing(parent)) 

        # does not show the min button
        parent.resizable(0,0)

        # fonte tamanho 9 para botoes e textos em geral
        self.font1 = ('Arial', 9)

        #setting the default font for applicantion
        parent.option_add( "*font", "Arial 9")

        # Defining the image files
        self.eva_image = PhotoImage(file = "images/eva.png") 
        self.bulb_image = PhotoImage(file = "images/bulb.png")
        self.eva_woz = PhotoImage(file = "images/eva_woz.png")
        # eva expressions images
        self.im_eyes_neutral = PhotoImage(file = "images/eyes_neutral.png")
        self.im_eyes_angry = PhotoImage(file = "images/eyes_angry.png")
        self.im_eyes_sad = PhotoImage(file = "images/eyes_sad.png")
        self.im_eyes_happy = PhotoImage(file = "images/eyes_happy.png")
        self.im_eyes_on = PhotoImage(file = "images/eyes_on.png")
        self.im_eyes_happy = PhotoImage(file = "images/eyes_fear.png")
        self.im_eyes_on = PhotoImage(file = "images/eyes_surprise.png")
        # imagens do botões
        self.im_eyes_neutral_btn = PhotoImage(file = "images/eyes_neutral_btn.png")
        self.im_eyes_angry_btn = PhotoImage(file = "images/eyes_angry_btn.png")
        self.im_eyes_sad_btn = PhotoImage(file = "images/eyes_sad_btn.png")
        self.im_eyes_happy_btn = PhotoImage(file = "images/eyes_happy_btn.png")
        self.im_eyes_fear_btn = PhotoImage(file = "images/eyes_fear_btn.png")
        self.im_eyes_surprise_btn = PhotoImage(file = "images/eyes_surprise_btn.png")
        #self.im_eyes_inlove_btn = PhotoImage(file = "images/eyes_inlove.png")
        
        # matrix voice images
        self.im_matrix_blue = PhotoImage(file = "images/matrix_blue.png")
        self.im_matrix_green = PhotoImage(file = "images/matrix_green.png")
        self.im_matrix_yellow = PhotoImage(file = "images/matrix_yellow.png")
        self.im_matrix_white = PhotoImage(file = "images/matrix_white.png")
        self.im_matrix_red = PhotoImage(file = "images/matrix_red.png")
        self.im_matrix_grey = PhotoImage(file = "images/matrix_grey.png")

        self.im_bt_play = PhotoImage(file = "images/bt_play.png")
        self.im_bt_stop = PhotoImage(file = "images/bt_stop.png")

        # bulb button images
        self.im_bulb_white_btn = PhotoImage(file = "images/bulb_white_btn.png")
        self.im_bulb_off_btn = PhotoImage(file = "images/bulb_off_btn.png")
        self.im_bulb_red_btn = PhotoImage(file = "images/bulb_red_btn.png")
        self.im_bulb_pink_btn = PhotoImage(file = "images/bulb_pink_btn.png")
        self.im_bulb_green_btn = PhotoImage(file = "images/bulb_green_btn.png")
        self.im_bulb_yellow_btn = PhotoImage(file = "images/bulb_yellow_btn.png")
        self.im_bulb_blue_btn = PhotoImage(file = "images/bulb_blue_btn.png")


        # define o frame top
        self.frame_top = tkinter.Frame(master=parent) #self.h
        # define o frame bottom (Woz)
        self.frame_bottom = tkinter.Frame(master=parent) #self.h
        # Pack Top and Bottom frames
        self.frame_top.pack(side=tkinter.TOP)
        self.frame_bottom.pack(side=tkinter.TOP, pady = 45)

        # define o frame que acomodará o canva com a imagem do EVA
        self.frame_robot = tkinter.Frame(master=self.frame_top, width= 400) #self.h
        # define o frame para o terminal e o menu de botões
        self.frame_centro = tkinter.Frame(master=self.frame_top, width= 750, height=self.h)
        # define o frame para as tabelas de memória
        self.frame_memory = tkinter.Frame(master=self.frame_top, width= 180, height=self.h)
        # Pack Frames
        self.frame_robot.pack(side=tkinter.LEFT)
        self.frame_centro.pack(side=tkinter.LEFT, padx=10) # fill=tkinter.Y,
        self.frame_memory.pack(side=tkinter.LEFT) # self.frame_memory.place(x=1100, y=60)
        # criando o canvas gráfico
        self.canvas = Canvas(self.frame_robot, width = 400, height = 510) # o canvas e' necessario para usar imagens com transparencia
        self.canvas.pack(side=tkinter.LEFT, pady= 30)

        # Define os frames para o frame Bottom
        # Frame com as expressões
        self.frame_exp = tkinter.Frame(master=self.frame_bottom) #self.h
        # Frame com os Leds
        self.frame_leds = tkinter.Frame(master=self.frame_bottom) #self.h
        # Frame com as cores da lâmpada
        self.frame_lampada = tkinter.Frame(master=self.frame_bottom) #self.h
        # Frame com os botões de movimento
        self.frame_motion = tkinter.Frame(master=self.frame_bottom) #self.h
        # Frame com o botão de speak
        self.frame_tts = tkinter.Frame(master=self.frame_bottom) #self.h
        # Pack frames
        self.frame_canvas_woz = tkinter.Frame(master=self.frame_bottom) #self.h

        # Pack frames
        self.frame_exp.pack(side=tkinter.LEFT)
        self.frame_leds.pack(side=tkinter.LEFT)
        self.frame_lampada.pack(side=tkinter.LEFT)
        self.frame_motion.pack(side=tkinter.LEFT)
        self.frame_tts.pack(side=tkinter.LEFT)
        self.frame_canvas_woz.pack(side=tkinter.LEFT)

        lfs_padx = 6
        # label frame expressions
        self.lf_exp = LabelFrame(self.frame_exp, text = 'EVA Expressions', font = self.font1)
        self.lf_exp.pack(side=tkinter.LEFT, padx=lfs_padx)
        # botões com as expressões
        btn_exp_w = 60
        btn_exp_pady = 5
        self.bt_exp_neutral = Button (self.lf_exp, text = "Neutral", width = btn_exp_w, image = self.im_eyes_neutral_btn,font = self.font1, compound = TOP)
        self.bt_exp_neutral.grid(row=0, column=0, padx=4, pady=btn_exp_pady)
        self.bt_exp_happy = Button (self.lf_exp, text = "Happy", width = btn_exp_w, image = self.im_eyes_happy_btn,font = self.font1, compound = TOP)
        self.bt_exp_happy.grid(row=0, column=1, padx=4, pady=btn_exp_pady)
        self.bt_exp_angry = Button (self.lf_exp, text = "Angry", width = btn_exp_w, image = self.im_eyes_angry_btn,font = self.font1, compound = TOP)
        self.bt_exp_angry.grid(row=1, column=0, padx=4, pady=btn_exp_pady)
        self.bt_exp_sad = Button (self.lf_exp, text = "Sad", width = btn_exp_w, image = self.im_eyes_sad_btn,font = self.font1, compound = TOP)
        self.bt_exp_sad.grid(row=1, column=1, padx=4, pady=btn_exp_pady)
        self.bt_exp_fear = Button (self.lf_exp, text = "Fear", width = btn_exp_w, image = self.im_eyes_fear_btn,font = self.font1, compound = TOP)
        self.bt_exp_fear.grid(row=2, column=0, padx=4, pady=btn_exp_pady)
        self.bt_exp_surprise = Button (self.lf_exp, text = "Surprise", width = btn_exp_w, image = self.im_eyes_surprise_btn,font = self.font1, compound = TOP)
        self.bt_exp_surprise.grid(row=2, column=1, padx=4, pady=btn_exp_pady)

        # label frame Leds
        self.lf_leds = LabelFrame(self.frame_leds, text = 'RGB Leds Animations', font = self.font1)
        self.lf_leds.pack(side=tkinter.LEFT, padx=lfs_padx)
        # botões com os leds
        btn_led_w = 7
        btn_led_pady = 8
        self.bt_led_happy = Button (self.lf_leds, foreground = "green" , width = btn_led_w, text = "HAPPY",font = self.font1, compound = LEFT)
        self.bt_led_happy.grid(row=0, column=0, padx=4, pady=btn_led_pady)
        self.bt_led_sad = Button (self.lf_leds, foreground = "blue" , width = btn_led_w,  text = "SAD",font = self.font1, compound = LEFT)
        self.bt_led_sad.grid(row=0, column=1, padx=4, pady=btn_led_pady)
        self.bt_led_angry = Button (self.lf_leds, foreground = "red" , width = btn_led_w, text = "ANGRY",font = self.font1, compound = LEFT)
        self.bt_led_angry.grid(row=1, column=0, padx=4, pady=btn_led_pady)
        self.bt_led_angry2 = Button (self.lf_leds, foreground = "red" , width = btn_led_w, text = "ANGRY2",font = self.font1, compound = LEFT)
        self.bt_led_angry2.grid(row=1, column=1, padx=4, pady=btn_led_pady)
        self.bt_led_stop = Button (self.lf_leds, foreground = "black" , width = btn_led_w, text = "STOP",font = self.font1, compound = LEFT)
        self.bt_led_stop.grid(row=2, column=0, padx=4, pady=btn_led_pady)
        self.bt_led_speak = Button (self.lf_leds, foreground = "blue" , width = btn_led_w, text = "SPEAK",font = self.font1, compound = LEFT)
        self.bt_led_speak.grid(row=2, column=1, padx=4, pady=btn_led_pady)
        self.bt_led_listen = Button (self.lf_leds, foreground = "green" , width = btn_led_w, text = "LISTEN",font = self.font1, compound = LEFT)
        self.bt_led_listen.grid(row=3, column=0, padx=4, pady=btn_led_pady)
        self.bt_led_surprise = Button (self.lf_leds, foreground = "yellow" , width = btn_led_w, text = "SURPRISE",font = self.font1, compound = LEFT)
        self.bt_led_surprise.grid(row=3, column=1, padx=4, pady=btn_led_pady)
        self.bt_led_white = Button (self.lf_leds, foreground = "white" , width = btn_led_w, text = "WHITE",font = self.font1, compound = LEFT)
        self.bt_led_white.grid(row=4, column=0, padx=4, pady=btn_led_pady)
        self.bt_led_rainbow = Button (self.lf_leds, foreground = "black" , width = btn_led_w, text = "RAINBOW",font = self.font1, compound = LEFT)
        self.bt_led_rainbow.grid(row=4, column=1, padx=4, pady=btn_led_pady)
        

        # label frame lampada
        btn_bulb_pady = 7
        btn_bulb_padx = 2
        self.lf_bulb = LabelFrame(self.frame_lampada, text = 'Smart Bulb Colors', font = self.font1)
        self.lf_bulb.pack(side=tkinter.LEFT, padx=lfs_padx)
        # botões com as lâmpadas
        self.bt_bulb_white_btn = Button (self.lf_bulb, text = 'White', width = 60, image = self.im_bulb_white_btn,font = self.font1)
        self.bt_bulb_white_btn.grid(row=0, column=0, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_off_btn = Button (self.lf_bulb, text = 'OFF', width = 60, image = self.im_bulb_off_btn,font = self.font1)
        self.bt_bulb_off_btn.grid(row=0, column=1, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_red_btn = Button (self.lf_bulb, text = 'Red', width = 60, image = self.im_bulb_red_btn,font = self.font1)
        self.bt_bulb_red_btn.grid(row=0, column=2, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_pink_btn = Button (self.lf_bulb, text = 'White', width = 60, image = self.im_bulb_pink_btn,font = self.font1)
        self.bt_bulb_pink_btn.grid(row=1, column=0, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_green_btn = Button (self.lf_bulb, text = 'Black', width = 60, image = self.im_bulb_green_btn,font = self.font1)
        self.bt_bulb_green_btn.grid(row=1, column=1, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_yellow_btn = Button (self.lf_bulb, text = 'Yellow', width = 60, image = self.im_bulb_yellow_btn,font = self.font1)
        self.bt_bulb_yellow_btn.grid(row=1, column=2, padx=btn_bulb_padx, pady=btn_bulb_pady)
        self.bt_bulb_blue_btn = Button (self.lf_bulb, text = 'Blue', width = 60, image = self.im_bulb_blue_btn,font = self.font1)
        self.bt_bulb_blue_btn.grid(row=2, column=0, padx=btn_bulb_pady)
        
        # motion frame
        btn_motion_padx = 0
        btn_motion_pady = 3
        self.lf_motion = LabelFrame(self.frame_motion, text = 'Head Motion', font = self.font1)
        self.lf_motion.pack(side=tkinter.LEFT, padx=lfs_padx)
        # botões com os movimentos
        btn_motion_w = 10
        self.bt_motion_up_left = Button (self.lf_motion, width = btn_motion_w, text = 'UP/LEFT',font = self.font1)
        self.bt_motion_up_left.grid(row=0, column=0, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_up = Button (self.lf_motion,  width = btn_motion_w, text = 'UP', font = self.font1)
        self.bt_motion_up.grid(row=0, column=1, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_2up = Button (self.lf_motion,  width = btn_motion_w, text = '2 x UP', font = self.font1)
        self.bt_motion_2up.grid(row=0, column=2, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_up_right = Button (self.lf_motion,  width = btn_motion_w, text = 'UP/RIGHT', font = self.font1)
        self.bt_motion_up_right.grid(row=0, column=3, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_left = Button (self.lf_motion,  width = btn_motion_w, text = 'LEFT', font = self.font1)
        self.bt_motion_left.grid(row=1, column=0, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_center = Button (self.lf_motion,  width = 2 * btn_motion_w + 5, height = 3,  text = 'CENTER', font = self.font1)
        self.bt_motion_center.grid(row=1, column=1, padx=btn_motion_padx, pady=btn_motion_pady, columnspan = 2, rowspan = 2)
        self.bt_motion_2left = Button (self.lf_motion,  width = btn_motion_w, text = '2 x LEFT', font = self.font1)
        self.bt_motion_2left.grid(row=2, column=0, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_right = Button (self.lf_motion,  width = btn_motion_w, text = 'RIGHT', font = self.font1)
        self.bt_motion_right.grid(row=1, column=3, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_2right = Button (self.lf_motion,  width = btn_motion_w, text = '2 x RIGHT', font = self.font1)
        self.bt_motion_2right.grid(row=2, column=3, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_down_left = Button (self.lf_motion,  width = btn_motion_w, text = 'DOWN/LEFT', font = self.font1)
        self.bt_motion_down_left.grid(row=3, column=0, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_down = Button (self.lf_motion,  width = btn_motion_w, text = 'DOWN', font = self.font1)
        self.bt_motion_down.grid(row=3, column=1, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_2down = Button (self.lf_motion,  width = btn_motion_w, text = '2 x DOWN', font = self.font1)
        self.bt_motion_2down.grid(row=3, column=2, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_down_right = Button (self.lf_motion,  width = btn_motion_w, text = 'DOWN/RIGHT', font = self.font1)
        self.bt_motion_down_right.grid(row=3, column=3, padx=btn_motion_padx, pady=btn_motion_pady)
        self.bt_motion_yes = Button (self.lf_motion, foreground="green", width = 2 * btn_motion_w + 5, height = 4, text = 'YES', font = self.font1)
        self.bt_motion_yes.grid(row=4, column=0, padx=btn_motion_padx, pady=btn_motion_pady + 2, columnspan=2, rowspan=2)
        self.bt_motion_no = Button (self.lf_motion, foreground="red", width = 2 * btn_motion_w + 5, height = 4, text = 'NO', font = self.font1)
        self.bt_motion_no.grid(row=4, column=2, padx=btn_motion_padx, pady=btn_motion_pady + 2, columnspan=2, rowspan=2)


        # label frame tts
        self.lf_tts = LabelFrame(self.frame_tts, text = 'Text-To-Speech (TTS) - IBM Watson Service', font = self.font1)
        self.lf_tts.pack(side=tkinter.LEFT, padx=lfs_padx)
        
        self.lbl_voice_options = tkinter.Label(self.lf_tts, bg="gray70", width="20", font = self.font1, text="Voice Options", padx=5, pady=2)
        self.lbl_voice_options.grid(row=0, column=0)
        
        self.Lb_voices = Listbox(self.lf_tts, width= 21, height=12)
        self.Lb_voices.insert(1, "en-US_AllisonV3Voice")
        self.Lb_voices.insert(2, "en-US_EmmaExpressive")
        self.Lb_voices.insert(3, "en-US_MichaelExpressive")
        self.Lb_voices.insert(4, "en-US_HenryV3Voice")
        self.Lb_voices.insert(5, "pt-BR_IsabelaV3Voice")
        self.Lb_voices.insert(6, "es-ES_LauraV3Voice")
        self.Lb_voices.insert(7, "es-ES_EnriqueV3Voice")
        self.Lb_voices.grid(row=1, column=0,  rowspan=2, padx=5) #expand=True, fill=tkinter.BOTH
        self.Lb_voices.selection_set(4)

        tkinter.Label(self.lf_tts, width="30", font = self.font1, text="Text to speech:", pady=2).grid(row=0, column=1)
        self.msg_tts_text = Text(self.lf_tts, height = 10, width=35)
        self.msg_tts_text.grid(row=1, column=1)
        self.bt_send_tts = Button (self.lf_tts, width=32, text = 'SEND (Speak)', font = self.font1)
        self.bt_send_tts.grid(row=2, column=1)


        # Canva para a imagem do EVA WoZ
        self.canvas_woz = Canvas(self.frame_canvas_woz) # o canvas e' necessario para usar imagens com transparencia
        self.canvas_woz.pack(side=tkinter.LEFT)
        self.canvas_woz.create_image(95, 120, image = self.eva_woz)


    

        # define o frame para o menu de botões
        self.frame_botoes = tkinter.Frame(master=self.frame_centro)
        self.frame_botoes.pack(pady=15, padx=10)

        # define o frame para o terminal
        self.frame_terminal = tkinter.Frame(master=self.frame_centro)
        self.frame_terminal.pack(fill=tkinter.X)


        # cria a tabela de memoria
        # define as propriedads da tabela com o mapa de memoria de $
        tkinter.Label(self.frame_memory, bg="gray70", width="48", font = self.font1, text="System Variables $ (Memory Map)", pady=1).pack()

        # define o estilo das tabelas
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 8), rowheight=15) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Arial', 8,'bold')) # Modify the font of the headings
        self.tab_dollar = ttk.Treeview(self.frame_memory, style="mystyle.Treeview", height=18)
        self.tab_dollar.pack()

        self.tab_dollar['columns']= ('Index', 'Content', "Source")
        self.tab_dollar.column("#0", width=0,  stretch=NO)
        self.tab_dollar.column("Index",anchor=CENTER, width=45)
        self.tab_dollar.column("Content",anchor=CENTER, width=200)
        self.tab_dollar.column("Source",anchor=CENTER, width=90)

        self.tab_dollar.heading("#0",text="",anchor=CENTER)
        self.tab_dollar.heading("Index",text="Index",anchor=CENTER)
        self.tab_dollar.heading("Content",text="Content",anchor=CENTER)
        self.tab_dollar.heading("Source",text="Source",anchor=CENTER)

        # label so pra separar as tabelas
        tkinter.Label(self.frame_memory, text="", font = ('Arial', 6)).pack()

        # define as propriedades da tabela com o mapa de memoria de variaveis do usuario
        tkinter.Label(self.frame_memory, width="48", bg="gray70", font = self.font1, text="User Variables (Memory Map)", pady=1).pack()
        self.tab_vars = ttk.Treeview(self.frame_memory, style="mystyle.Treeview", height=13)
        self.tab_vars.pack()

        self.tab_vars['columns']= ('Var', 'Value')
        self.tab_vars.column("#0", width=0,  stretch=NO)
        self.tab_vars.column("Var", anchor=CENTER, width=152)
        self.tab_vars.column("Value", anchor=CENTER, width=182)

        self.tab_vars.heading("#0",text="",anchor=CENTER)
        self.tab_vars.heading("Var", text="Var",anchor=CENTER)
        self.tab_vars.heading("Value",text="Value",anchor=CENTER)

        
        # desenha o eva e a lampada desligada
        self.canvas.create_image(160, 262, image = self.eva_image)
        self.canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        self.canvas.create_image(340, 285, image = self.bulb_image)


        # criacao dos botoes da interface com usuário
        self.bt_padx = 8 # ajuste de espaçamento entre botões
        self.bt_power = Button (self.frame_botoes, text = "Power On", font = self.font1)
        self.bt_power.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_import = Button (self.frame_botoes, text = "Import Script File...", font = self.font1, state = DISABLED)
        self.bt_import.pack(side=tkinter.LEFT, padx=self.bt_padx)

        self.lf = LabelFrame(self.frame_botoes, text = 'Running Mode', font = self.font1)
        self.lf.pack(side=tkinter.LEFT, padx=self.bt_padx)

        self.bt_run_sim = Button (self.lf, text = "Simulator", image = self.im_bt_play, font = self.font1, state = DISABLED, compound = LEFT)
        self.bt_run_sim.pack(side=tkinter.LEFT, padx=self.bt_padx, pady=2)
        self.bt_run_robot = Button (self.lf, text = "EVA Robot", image = self.im_bt_play, font = self.font1, state = DISABLED, compound = LEFT)
        self.bt_run_robot.pack(side=tkinter.LEFT, padx=self.bt_padx, pady=2)

        self.bt_stop = Button (self.frame_botoes, text = "Stop", font = self.font1, image = self.im_bt_stop, state = DISABLED, compound = LEFT)
        self.bt_stop.pack(side=tkinter.LEFT, padx=self.bt_padx)
        self.bt_clear = Button (self.frame_botoes, text = "Clear Terminal", font = self.font1, state = NORMAL, compound = LEFT)
        self.bt_clear.pack(side=tkinter.LEFT, padx=self.bt_padx)


        # Add a Scrollbar(horizontal)
        self.v=Scrollbar(self.frame_terminal, orient='vertical')
        self.v.pack(side=RIGHT, fill='y')

        # Terminal text configuration
        self.terminal = Text (self.frame_terminal, fg = "cyan", bg = "black", height = "32", width = "125", yscrollcommand=self.v.set)
        self.terminal.configure(font = ("Arial", 9))
        self.terminal.tag_configure("error", foreground="red")
        self.terminal.tag_configure("motion", foreground="orange")
        self.terminal.tag_configure("tip", foreground="yellow")
        self.v.config(command=self.terminal.yview)
        # limpa, desenha e coloca terminal no frame dele
        self.terminal.delete('1.0', END)
        # criando terminal text
        self.terminal.insert(INSERT, "=============================================================================================================================\n")
        self.terminal.insert(INSERT, "                                                                                                                         Eva Simulator for EvaML\n")
        self.terminal.insert(INSERT, "                                                                                    Version 2.0 - UFF / MidiaCom / CICESE / Google Research - [2023]\n")
        self.terminal.insert(INSERT, "=============================================================================================================================")

        self.terminal.pack()

        # Desenha o eva e a lampada desligada
        # Defining the image files
        self.eva_image = PhotoImage(file = "images/eva.png") 
        self.bulb_image = PhotoImage(file = "images/bulb.png")
        self.canvas.create_image(160, 262, image = self.eva_image)
        self.canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        self.canvas.create_image(340, 285, image = self.bulb_image)
