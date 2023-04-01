#!/usr/bin/env python3
# EvaSIM - Software Simulador para o robô EVA
# Autor: Marcelo Marques da Rocha
# Labaratório MidiaCOM - Universidade Federal Fluminense

import platform

# seleciona o arquivo de definição da GUI para o sistema operacional host
if platform.system() == "Linux":
    print("Linux platform identified. Loading GUI formatting for Linux.")
    import gui_linux as EvaSIM_gui # definicoes da interface grafica de usuario (Linux)
    audio_ext = ".mp3" # extensão do audio utilizado pela biblioteca de audio no Linux
    ibm_audio_ext = "audio/mp3" # extensão do audio usado pra gerar os audios do watson
elif platform.system() == "Windows":
    print("Windows platform identified. Loading GUI formatting for Windows.")
    import gui_windows as EvaSIM_gui # definicoes da interface grafica de usuario (Windows)
    audio_ext = ".wav"
    ibm_audio_ext = "audio/wav"
else:
    print("Sorry, the current OS is not supported by EvaSIM.") # OS incompativel
    exit(1)

import hashlib
import re # expressões regulares
import os

import random as rnd
import xml.etree.ElementTree as ET

import eva_memory # modulo de memoria do EvaSIM
import json_to_evaml_conv # modulo de conversao de json para XML

from tkinter import *
from tkinter import filedialog as fd
import tkinter
# from  tkinter import ttk # usando tabelas

# modulo adaptador para a biblioteca de audio
# dependendo do OS importa e define uma função chamada "playsound"
from play_audio import playsound

import time
import threading

# from ibm_watson.text_to_speech_v1 import Voice
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# variaveis globais da vm
root = {}
script_node = {}
links_node = {}
fila_links =  [] # fila de links (comandos)
thread_pop_pause = False
play = False # estado do play do script. esta variavel tem influencia na func. link_process

# funcao de controle da variavel que bloqueia as janelas popups
def lock_thread_pop():
    global thread_pop_pause
    thread_pop_pause = True

def unlock_thread_pop():
    global thread_pop_pause
    thread_pop_pause = False


# watson config api key
with open("ibm_cred.txt", "r") as ibm_cred:
    ibm_config = ibm_cred.read().splitlines()
apikey = ibm_config[0]
url = ibm_config[1]
# setup watson service
authenticator = IAMAuthenticator(apikey)
# tts service
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)


# Create the Tkinter window
window = Tk()
gui = EvaSIM_gui.Gui(window) # Instancia da classe Gui dentro do módulo de definição da interface gráfica do usuário

font1 = gui.font1 # usa a mesma fonte definida no modulo GUI

# eva expressions images
im_eyes_neutral = PhotoImage(file = "images/eyes_neutral.png")
im_eyes_angry = PhotoImage(file = "images/eyes_angry.png")
im_eyes_sad = PhotoImage(file = "images/eyes_sad.png")
im_eyes_happy = PhotoImage(file = "images/eyes_happy.png")
im_eyes_on = PhotoImage(file = "images/eyes_on.png")
# matrix voice images
im_matrix_blue = PhotoImage(file = "images/matrix_blue.png")
im_matrix_green = PhotoImage(file = "images/matrix_green.png")
im_matrix_yellow = PhotoImage(file = "images/matrix_yellow.png")
im_matrix_white = PhotoImage(file = "images/matrix_white.png")
im_matrix_red = PhotoImage(file = "images/matrix_red.png")
im_matrix_grey = PhotoImage(file = "images/matrix_grey.png")
im_bt_play = PhotoImage(file = "images/bt_play.png")
im_bt_stop = PhotoImage(file = "images/bt_stop.png")


# funcao para escrever os dados da memoria na tabela de variaveis
def tab_load_mem_vars():
    for i in gui.tab_vars.get_children(): # limpa os valores da tabela
        gui.tab_vars.delete(i)

    for var_name in eva_memory.vars: # lê a memória inserindo os valoes na tabela
        gui.tab_vars.insert(parent='',index='end',text='', values=(var_name, eva_memory.vars[var_name]))


# funcao para escrever os dados da memoria na tabela mem dollar
def tab_load_mem_dollar():
    indice = 1 # indice para a variável dollar
    for i in gui.tab_dollar.get_children(): # limpa os valores da tabela
        gui.tab_dollar.delete(i)

    for var_dollar in eva_memory.var_dolar: # lê a memória inserindo os valoes na tabela
        if indice == len(eva_memory.var_dolar):
            var_name = "$"
        else:
            var_name = "$" + str(indice)

        gui.tab_dollar.insert(parent='',index='end',text='', values=(var_name, var_dollar[0], var_dollar[1]))
        indice = indice + 1


# Eva initialization function
def evaInit():
    gui.bt_power['state'] = DISABLED
    gui.bt_power.unbind("<Button-1>")
    evaEmotion("POWER_ON")
    gui.terminal.insert(INSERT, "\nstate: Initializing.")
    playsound("my_sounds/power_on" + audio_ext, block = True)
    gui.terminal.insert(INSERT, "\nstate: Speaking a greeting text.")
    playsound("my_sounds/greetings" + audio_ext, block = True)
    gui.terminal.insert(INSERT, '\nstate: Speaking "Load a script file and enjoy."')
    playsound("my_sounds/load_a_script" + audio_ext, block = True)
    gui.terminal.insert(INSERT, "\nstate: Entering in standby mode.")
    gui.bt_import['state'] = NORMAL
    gui.bt_import.bind("<Button-1>", importFileThread)
    evaMatrix("white")
    while gui.bt_run['state'] == DISABLED: # animacao da luz da matrix em stand by
        evaMatrix("white")
        time.sleep(0.5)
        evaMatrix("grey")
        time.sleep(0.5)


# Eva powerOn function
def powerOn(self):
    threading.Thread(target=evaInit, args=()).start()


# Ativa a thread que roda o script
def runScript(self):
    global play, fila_links
    # initialize the robot memory
    print("Intializing the robot memory...")
    eva_memory.var_dolar = []
    eva_memory.vars = {}
    eva_memory.reg_case = 0
    # Limpando as tabelas
    print("Clearing memory map tables...")
    tab_load_mem_dollar()
    tab_load_mem_vars()
    # initializing the memory of simulator
    fila_links =  []
    # buttons states
    gui.bt_run['state'] = DISABLED
    gui.bt_run.unbind("<Button-1>")
    gui.bt_import['state'] = DISABLED
    gui.bt_stop['state'] = NORMAL
    gui.bt_stop.bind("<Button-1>", stopScript)
    gui.bt_import.unbind("<Button-1>")
    play = True # ativa a var do play do script
    root.find("settings").find("voice").attrib["key"]
    busca_links(root.find("settings").find("voice").attrib["key"]) # o primeiro elemento da interação é o voice
    threading.Thread(target=link_process, args=()).start()

# Encerra a thread que roda o script
def stopScript(self):
    global play
    gui.bt_run['state'] = NORMAL
    gui.bt_run.bind("<Button-1>", runScript)
    gui.bt_stop['state'] = DISABLED
    gui.bt_stop.unbind("<Button-1>")
    gui.bt_import['state'] = NORMAL
    gui.bt_import.bind("<Button-1>", importFileThread)
    play = False # desativa a var de play do script. Faz com que o script seja interrompido

# import file thread
def importFileThread(self):
    threading.Thread(target=importFile, args=()).start()

# Eva Import Script function
def importFile():
    global root, script_node, links_node
    print("Importing a file...")
    # agora o EvaSIM pode ler json
    filetypes = (('evaML files', '*.xml *.json'), )
    script_file = fd.askopenfile(mode = "r", title = 'Open an EvaML Script File', initialdir = './', filetypes = filetypes)
    # imaginado que o cara vai ler um json ou um xml
    if (re.findall(r'\.(xml|json|JSON|XML)', str(script_file)))[0].lower() == "json": # leitura de json
        print("Convertendo e executando um arquivo do tipo JSON")
        #  script_file não é uma string e ainda possui infos além do caminho do arquivo
        # por isso precisa ser processada antes de ser passada para o modulo de conversão
        json_to_evaml_conv.converte(str(script_file).split("'")[1], tkinter)
        script_file = "_json_to_evaml_converted.xml" # arquivo json convertido para XML
    else: # leitura de um XML
        print("Executando um arquivo do tipo XML")
    # variaveis da vm
    tree = ET.parse(script_file)  # arquivo de codigo xml
    root = tree.getroot() # evaml root node
    script_node = root.find("script")
    links_node = root.find("links")
    gui.bt_run['state'] = NORMAL
    gui.bt_run.bind("<Button-1>", runScript)
    gui.bt_stop['state'] = DISABLED
    evaEmotion("NEUTRAL")
    gui.terminal.insert(INSERT, '\nstate: Script loaded.')
    gui.terminal.see(tkinter.END)


def clear_terminal(self):
    gui.terminal.delete('1.0', END)
    # criando terminal text
    gui.terminal.insert(INSERT, "=====================================================================================\n")
    gui.terminal.insert(INSERT, "                                                                Eva Simulator for EvaML\n")
    gui.terminal.insert(INSERT, "                                                Version 1.0 - UFF/MidiaCom/CICESE [2022]\n")
    gui.terminal.insert(INSERT, "=====================================================================================")


# conecta as callbacks aos botoes
# a utilizacao de um outro modulo para definir a GUI não permitiu que as callbacks fossem assiciadas aos botões no momento de suas criações
# a utilização do metodo bind para definir callbacks tem uma limitação
# o elemento, mesmo no estado "disable" continua a responder a eventos de click do mouse
# por isso, ao desabilitar um botão, é necessário utilizar "unbind" para desvincular a callback ao botão
# se o botão for colocado no estado "normal", a callback deverá ser redefinida utilizando-se o "bind" novamente
gui.bt_power.bind("<Button-1>", powerOn)
gui.bt_clear.bind("<Button-1>", clear_terminal)



# led "animations"
def ledAnimation(animation):
    if animation == "STOP": evaMatrix("grey")
    elif animation == "LISTEN": evaMatrix("green")
    elif animation == "SPEAK": evaMatrix("blue")
    elif animation == "ANGRY": evaMatrix("red")
    elif animation == "HAPPY": evaMatrix("green")
    elif animation == "SAD": evaMatrix("blue")
    elif animation == "SURPRISE": evaMatrix("yellow")
    else: print("wrong led animation option")


# set the Eva emotion
def evaEmotion(expression):
    if expression == "NEUTRAL":
        gui.canvas.create_image(156, 161, image = im_eyes_neutral)
    elif expression == "ANGRY":
        gui.canvas.create_image(156, 161, image = im_eyes_angry)
    elif expression == "HAPPY":
        gui.canvas.create_image(156, 161, image = im_eyes_happy)
    elif expression == "SAD":
        gui.canvas.create_image(156, 161, image = im_eyes_sad)
    elif expression == "POWER_ON": 
        gui.canvas.create_image(156, 161, image = im_eyes_on)
    else: 
        print("Wrong expression")
    time.sleep(1)


# set the Eva matrix
def evaMatrix(color):
    if color == "blue":
        gui.canvas.create_image(155, 349, image = im_matrix_blue)
    elif color == "red":
        gui.canvas.create_image(155, 349, image = im_matrix_red)
    elif color == "yellow":
        gui.canvas.create_image(155, 349, image = im_matrix_yellow)
    elif color == "green":
        gui.canvas.create_image(155, 349, image = im_matrix_green)
    elif color == "white":
        gui.canvas.create_image(155, 349, image = im_matrix_white)
    elif color == "grey":
        gui.canvas.create_image(155, 349, image = im_matrix_grey)
    else : 
        print("wrong color to matrix...")


# set the image of light (color and state)
def light(color, state):
    print("aqui ------------")
    color_map = {"WHITE":"#ffffff", "BLACK":"#000000", "RED":"#ff0000", "PINK":"#e6007e", "GREEN":"#00ff00", "YELLOW":"#ffff00", "BLUE":"#0000ff"}
    if color_map.get(color) != None:
        color = color_map.get(color)
    if state == "ON":
        gui.canvas.create_oval(300, 205, 377, 285, fill = color, outline = color )
        gui.canvas.create_image(340, 285, image = gui.bulb_image) # redesenha a lampada
    else:
        gui.canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        gui.canvas.create_image(340, 285, image = gui.bulb_image) # redesenha a lampada


# funcoes da maquina virtual
# executa os comandos
def exec_comando(node):
    if node.tag == "voice":
        gui.terminal.insert(INSERT, "\nstate: Selected Voice: " + node.attrib["tone"])
        gui.terminal.see(tkinter.END)
        gui.terminal.insert(INSERT, "\nTIP: If the <talk> command doesn't speak some text, try emptying the audio_cache_files folder", "tip")


    if node.tag == "motion":
        gui.terminal.insert(INSERT, "\nstate: Moving the head! Movement type: " + node.attrib["type"], "motion")
        gui.terminal.see(tkinter.END)
        print("Moving the head. Type:", node.attrib["type"])
        time.sleep(1) # Um tempo apenas simbólico. No robô, o movimento não bloqueia o script e demorar tempos distintos


    elif node.tag == "light":
        lightEffect = "ON"
        state = node.attrib["state"]
        # process lightEffects settings
        if root.find("settings").find("lightEffects") != None:
            if root.find("settings").find("lightEffects").attrib["mode"] == "OFF":
                lightEffect = "OFF"
        
        # caso a seguir, se o state é off, e pode não ter atributo color definido
        if state == "OFF":
            color = "black"
            if lightEffect == "OFF":
                message_state = "\nstate: Light Effects DISABLED."
            else:
                message_state = "\nstate: Turnning off the light."
            gui.terminal.insert(INSERT, message_state)
            gui.terminal.see(tkinter.END)
        else:
            color = node.attrib["color"]
            if lightEffect == "OFF":
                message_state = "\nstate: Light Effects DISABLED."
                state = "OFF"
            else:
                message_state = "\nstate: Turnning on the light. Color=" + color + "."
            gui.terminal.insert(INSERT, message_state)
            gui.terminal.see(tkinter.END) # autoscrolling
        light(color , state)
        time.sleep(1) # emula o tempo da lampada real


    elif node.tag == "wait":
        duration = node.attrib["duration"]
        gui.terminal.insert(INSERT, "\nstate: Pausing. Duration=" + duration + " ms")
        gui.terminal.see(tkinter.END)
        time.sleep(int(duration)/1000) # converte para segundos


    elif node.tag == "led":
        print(node.attrib["animation"])
        ledAnimation(node.attrib["animation"])
        gui.terminal.insert(INSERT, "\nstate: Matrix Leds. Animation=" + node.attrib["animation"])
        gui.terminal.see(tkinter.END)


    elif node.tag == "random":
        min = node.attrib["min"]
        max = node.attrib["max"]
        # verifica se min <= max
        if (int(min) > int(max)):
            gui.terminal.insert(INSERT, "\nError -> The 'min' attribute of the random command must be less than or equal to the 'max' attribute. Please, check your code.", "error")
            gui.terminal.see(tkinter.END)
            exit(1)

        eva_memory.var_dolar.append([str(rnd.randint(int(min), int(max))), "<random>"])
        gui.terminal.insert(INSERT, "\nstate: Generating a random number: " + eva_memory.var_dolar[-1][0])
        tab_load_mem_dollar()
        gui.terminal.see(tkinter.END)
        print("random command, min = " + min + ", max = " + max + ", valor = " + eva_memory.var_dolar[-1][0])


    elif node.tag == "listen":
        lock_thread_pop()
        ledAnimation("LISTEN")
        # função de fechamento da janela pop up para a tecla <return)
        def fechar_pop_ret(self): 
            print(var.get())
            eva_memory.var_dolar.append([var.get(), "<listen>"])
            gui.terminal.insert(INSERT, "\nstate: Listening : var=$" + ", value=" + eva_memory.var_dolar[-1][0])
            tab_load_mem_dollar()
            gui.terminal.see(tkinter.END)
            pop.destroy()
            unlock_thread_pop() # reativa a thread de processamento do script
        
        # função de fechamento da janela pop up par o botão ok
        def fechar_pop_bt(): 
            print(var.get())
            eva_memory.var_dolar.append([var.get(), "<listen>"])
            gui.terminal.insert(INSERT, "\nstate: Listening : var=$" + ", value=" + eva_memory.var_dolar[-1][0])
            tab_load_mem_dollar()
            gui.terminal.see(tkinter.END)
            pop.destroy()
            unlock_thread_pop() # reativa a thread de processamento do script
        # criacao da janela
        var = StringVar()
        pop = Toplevel(gui)
        pop.title("Listen Command")
        # Disable the max and close buttons
        pop.resizable(False, False)
        pop.protocol("WM_DELETE_WINDOW", False)
        w = 300
        h = 150
        ws = gui.winfo_screenwidth()
        hs = gui.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  
        pop.geometry('%dx%d+%d+%d' % (w, h, x, y))
        pop.grab_set()
        label = Label(pop, text="Eva is listening... Please, enter your answer!", font = ('Arial', 10))
        label.pack(pady=20)
        E1 = Entry(pop, textvariable = var, font = ('Arial', 10))
        E1.bind("<Return>", fechar_pop_ret)
        E1.pack()
        Button(pop, text="    OK    ", font = font1, command=fechar_pop_bt).pack(pady=20)
        # espera pela liberacao, aguardando a resposta do usuario
        while thread_pop_pause: 
            time.sleep(0.5)
        ledAnimation("STOP")


    elif node.tag == "talk":
        texto = node.text
        # substitui as variaveis através do texto. as variaveis devem existir na memoria
        if "#" in texto:
            # verifica se a memoria (vars) do robô está vazia
            if eva_memory.vars == {}:
                gui.terminal.insert(INSERT, "\nError -> No variables have been defined. Please, check your code.", "error")
                gui.terminal.see(tkinter.END)
                exit(1)

            var_list = re.findall(r'\#[a-zA-Z]+[0-9]*', texto) # gera lista de ocorrencias de vars (#...)
            for v in var_list:
                if v[1:] in eva_memory.vars:
                    texto = texto.replace(v, str(eva_memory.vars[v[1:]]))
                else:
                    # Se a variavel não existe na memoria do robô, exibe mensagem de erro.
                    print("================================")
                    error_string = "\nError -> The variable #" + v[1:] + " has not been declared. Please, check your code."
                    gui.terminal.insert(INSERT, error_string, "error")
                    gui.terminal.see(tkinter.END)
                    exit(1)

        # esta parte substitui o $, ou o $-1 ou o $1 no texto
        if "$" in texto: # verifica se tem $ no texto
            # verifica se var_dolar tem algum valor na memoria do robô
            if (len(eva_memory.var_dolar)) == 0:
                gui.terminal.insert(INSERT, "\nError -> The variable $ has no value. Please, check your code.", "error")
                gui.terminal.see(tkinter.END)
                exit(1)
            else: # encontra os padroes $ $n ou $-n no string e substitui pelos valores correspondentes
                dollars_list = re.findall(r'\$[-0-9]*', texto) # encontra os padroes do dolar e retorna uma lista com as ocorrencias
                dollars_list = sorted(dollars_list, key=len, reverse=True) # ordena a lista em ordem decrescente do len(do elemmento)
                for var_dollar in dollars_list:
                    if len(var_dollar) == 1: # é o dollar ($)
                        texto = texto.replace(var_dollar, eva_memory.var_dolar[-1][0])
                    else: # pode ser do tipo $n ou $-n
                        if "-" in var_dollar: # tipo $-n
                            indice = int(var_dollar[2:]) # var dollar é do tipo $-n. então pega somente o n e converte para int
                            texto = texto.replace(var_dollar, eva_memory.var_dolar[-(indice + 1)][0]) 
                        else: # tipo $n
                            indice = int(var_dollar[1:]) # var dollar é do tipo $n. então pega somente o n e converte para int
                            texto = texto.replace(var_dollar, eva_memory.var_dolar[(indice - 1)][0])
            
        # esta parte implementa o texto aleatorio gerado pelo uso do caractere /
        texto = texto.split(sep="/") # texto vira uma lista com a qtd de frases divididas pelo caract. /
        print(texto)
        ind_random = rnd.randint(0, len(texto)-1)
        gui.terminal.insert(INSERT, '\nstate: Speaking: "' + texto[ind_random] + '"')
        gui.terminal.see(tkinter.END)

        # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
        # Also, uses the voice tone attribute in file hashing
        hash_object = hashlib.md5(texto[ind_random].encode())
        file_name = "_audio_"  + root.find("settings")[0].attrib["tone"] + hash_object.hexdigest()

        # verifica se o audio da fala já existe na pasta
        if not (os.path.isfile("audio_cache_files/" + file_name + audio_ext)): # se nao existe chama o watson
            # Eva tts functions
            with open("audio_cache_files/" + file_name + audio_ext, 'wb') as audio_file:
                print("Aqui")
                try:
                    res = tts.synthesize(texto[ind_random], accept = ibm_audio_ext, voice = root.find("settings")[0].attrib["tone"]).get_result()
                    audio_file.write(res.content)
                except:
                    print("Voice exception")
                    gui.terminal.insert(INSERT, "\nError when trying to select voice tone, please verify the tone atribute.\n", "error")
                    gui.terminal.see(tkinter.END)
                    exit(1)
        ledAnimation("SPEAK")
        playsound("audio_cache_files/" + file_name + audio_ext, block = True) # toca o audio da fala
        ledAnimation("STOP")


    elif node.tag == "evaEmotion":
        emotion = node.attrib["emotion"]
        gui.terminal.insert(INSERT, "\nstate: Expressing an emotion: " + emotion)
        gui.terminal.see(tkinter.END)
        evaEmotion(emotion)


    elif node.tag == "audio":
        sound_file = "sonidos/" + node.attrib["source"] + ".wav"
        block = False # o play do audio não bloqueia a execucao do script
        if node.attrib["block"].lower() == "true":
            block = True
        message_audio = '\nstate: Playing a sound: "' + sound_file + '", block=' + str(block)

        # process audioEffects settings
        if root.find("settings").find("audioEffects") != None:
            if root.find("settings").find("audioEffects").attrib["mode"] == "OFF":
                # mode off implies the use of MUTED-SOUND file 
                sound_file = "my_sounds/MUTED-SOUND.wav"
                message_audio = "\nstate: Audio Effects DISABLED."

        gui.terminal.insert(INSERT, message_audio)
        gui.terminal.see(tkinter.END)
        ledAnimation("SPEAK")
        try:
            playsound(sound_file, block = block)
            ledAnimation("STOP")
        except Exception as e:
            # trata uma exceção. não achei exceções na documentação da biblioteca
            error_string = "\nError -> " + str(e) + "."
            gui.terminal.insert(INSERT, error_string, "error")
            gui.terminal.see(tkinter.END)
            exit(1)


    elif node.tag == "case": 
        global valor
        eva_memory.reg_case = 0 # limpa o flag do case
        valor = node.attrib["value"]
        valor = valor.lower() # as comparacoes não são case sensitive
        # trata os tipos de comparacao e operadores
        # caso 1 op="Exact"
        if node.attrib['op'] == "exact":
            # verifica se a memória de var_dolar tem algum valor
            if (len(eva_memory.var_dolar)) == 0:
                gui.terminal.insert(INSERT, "\nError -> The variable $ has no value. Please, check your code.", "error")
                gui.terminal.see(tkinter.END)
                exit(1)  

            # compara valor com o topo da pilha da variavel var_dolar
            print("valor ", valor, type(valor))
            if valor == eva_memory.var_dolar[-1][0].lower():
                print("case = true")
                eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
        
        # case 2 (tipo de op="contain")
        elif node.attrib['op'] == "contain":      
            # verifica se a memória de var_dolar tem algum valor
            if (len(eva_memory.var_dolar)) == 0:
                gui.terminal.insert(INSERT, "\nError -> The variable $ has no value. Please, check your code.", "error")
                gui.terminal.see(tkinter.END)
                exit(1)  

            # verifica se a string em valor está contida em $
            print("valor ", valor, type(valor))
            if valor in eva_memory.var_dolar[-1][0].lower(): 
                print("case = true")
                eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

        # caso 3 (COMPARAÇÃO MATEMÁTICA) 
        else:
            # funcao para obtencao de um operando a partir de $, n, #n, ou valor
            def get_op(st_var_value):
                # é uma constante?
                if st_var_value.isnumeric():
                    return int(st_var_value)

                # é $
                if st_var_value == "$":
                    # verifica se a memória de var_dolar tem algum valor
                    if (len(eva_memory.var_dolar)) == 0:
                        gui.terminal.insert(INSERT, "\nError -> The variable $ has no value. Please, check your code.", "error")
                        gui.terminal.see(tkinter.END)
                        exit(1)
                    return int(eva_memory.var_dolar[-1][0]) # retorna o valor de $ conv. para int

                # é uma variavel do tipo #n?
                if "#" in st_var_value:
                    # verifica se var #... NÂO existe na memória
                    if (st_var_value[1:] not in eva_memory.vars):
                        error_string = "\nError -> The variable #" + valor[1:] + " has not been declared. Please, check your code."
                        gui.terminal.insert(INSERT, error_string, "error")
                        gui.terminal.see(tkinter.END)
                        exit(1)
                    return int(eva_memory.vars[st_var_value[1:]])# retorna o valor de #n conv. para int
                
                # se não é numero, nem dolar , nem tem #, então é uma variavel deste tipo var="x" em <switch>
                # verifica se a variavel existe na memoria
                if (st_var_value not in eva_memory.vars):
                    error_string = "\nError -> The variable #" + valor[1:] + " has not been declared. Please, check your code."
                    gui.terminal.insert(INSERT, error_string, "error")
                    gui.terminal.see(tkinter.END)
                    exit(1)
                return int(eva_memory.vars[st_var_value])# retorna o valor de var n conv. para int

            # obtém os operandos para realizar a operações de comparação matemáticas
            # a restrição do não uso de constantes em var de <switch> foi garantida no parser
            op1 = get_op(node.attrib['var'])
            op2 = get_op(valor)

            # realiza as operações ==, >, <, >=, <= e != ) de comparação com os operandos 1 e 2
            if node.attrib['op'] == "eq": # 
                if op1 == op2: # é preciso retirar o # da variável
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

            elif node.attrib['op'] == "lt": # igualdade
                if op1 < op2:
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

            elif node.attrib['op'] == "gt": # igualdade
                if op1 > op2:
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
            
            elif node.attrib['op'] == "lte": # igualdade
                if op1 <= op2:
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

            elif node.attrib['op'] == "gte": # igualdade
                if op1 >= op2:
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

            elif node.attrib['op'] == "ne": # igualdade
                if op1 != op2:
                    print("case = true")
                    eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira          


    elif node.tag == "default": # default sempre será verdadeiro
        print("Default = true")
        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira


    elif node.tag == "counter":
        var_name = node.attrib["var"]
        var_value = int(node.attrib["value"])
        op = node.attrib["op"]
        # verifica se a operação é diferente de atribuição e verifica se var ... NÂO existe na memória
        if op != "=":
            if (var_name not in eva_memory.vars):
                error_string = "\nError -> The variable " + var_name + " has not been declared. Please, check your code."
                gui.terminal.insert(INSERT, error_string, "error")
                gui.terminal.see(tkinter.END)
                exit(1)

        if op == "=": # efetua a atribuicao
            eva_memory.vars[var_name] = var_value

        if op == "+": # efetua a adição
            eva_memory.vars[var_name] += var_value

        if op == "*": # efetua o produto
            eva_memory.vars[var_name] *= var_value

        if op == "/": # efetua a divisão (era /=) porem mudei para //= (divisão inteira)
            eva_memory.vars[var_name] //= var_value

        if op == "%": # calcula o módulo
            eva_memory.vars[var_name] %= var_value
        
        print("Eva ram => ", eva_memory.vars)
        gui.terminal.insert(INSERT, "\nstate: Counter : var=" + var_name + ", value=" + str(var_value) + ", op(" + op + "), result=" + str(eva_memory.vars[var_name]))
        tab_load_mem_vars() # entra com os dados da memoria de variaveis na tabela de vars
        gui.terminal.see(tkinter.END)


    elif node.tag == "userEmotion":
        global img_neutral, img_happy, img_angry, img_sad, img_surprised
        lock_thread_pop()

        def fechar_pop(): # função de fechamento da janela pop up
            print(var.get())
            eva_memory.var_dolar.append([var.get(), "<userEmotion>"])
            gui.terminal.insert(INSERT, "\nstate: userEmotion : var=$" + ", value=" + eva_memory.var_dolar[-1][0])
            tab_load_mem_dollar()
            gui.terminal.see(tkinter.END)
            pop.destroy()
            unlock_thread_pop() # reativa a thread de processamento do script

        var = StringVar()
        var.set("NEUTRAL")
        img_neutral = PhotoImage(file = "images/img_neutral.png")
        img_happy = PhotoImage(file = "images/img_happy.png")
        img_angry = PhotoImage(file = "images/img_angry.png")
        img_sad = PhotoImage(file = "images/img_sad.png")
        img_surprised = PhotoImage(file = "images/img_surprised.png")
        pop = Toplevel(gui)
        pop.title("userEmotion Command")
        # Disable the max and close buttons
        pop.resizable(False, False)
        pop.protocol("WM_DELETE_WINDOW", False)
        w = 697
        h = 250
        ws = gui.winfo_screenwidth()
        hs = gui.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  
        pop.geometry('%dx%d+%d+%d' % (w, h, x, y))
        pop.grab_set() # faz com que a janela receba todos os eventos
        Label(pop, text="Eva is analysing your face expression. Please, choose one emotion!", font = ('Arial', 10)).place(x = 146, y = 10)
        # imagens são exibidas usando os lables
        Label(pop, image=img_neutral).place(x = 10, y = 50)
        Label(pop, image=img_happy).place(x = 147, y = 50)
        Label(pop, image=img_angry).place(x = 284, y = 50)
        Label(pop, image=img_sad).place(x = 421, y = 50)
        Label(pop, image=img_surprised).place(x = 558, y = 50)
        Radiobutton(pop, text = "Neutral", variable = var, font = font1, command = None, value = "NEUTRAL").place(x = 35, y = 185)
        Radiobutton(pop, text = "Happy", variable = var, font = font1, command = None, value = "HAPPY").place(x = 172, y = 185)
        Radiobutton(pop, text = "Angry", variable = var, font = font1, command = None, value = "ANGRY").place(x = 312, y = 185)
        Radiobutton(pop, text = "Sad", variable = var, font = font1, command = None, value = "SAD").place(x = 452, y = 185)
        Radiobutton(pop, text = "Surprised", variable = var, font = font1, command = None, value = "SURPRISED").place(x = 575, y = 185)
        Button(pop, text = "     OK     ", font = font1, command = fechar_pop).place(x = 310, y = 215)
        # espera pela liberacao, aguardando a resposta do usuario
        while thread_pop_pause: 
            time.sleep(0.5)


def busca_commando(key): # keys são strings
	# busca em settings. Isto porque "voice" fica em settings e voice é sempre o primeiro elemento
	for elem in root.find("settings").iter():
		if elem.get("key") != None: # verifica se node tem atributo key
			if elem.attrib["key"] == key:
				return elem
	# busca dentro do script
	for elem in root.find("script").iter(): # passa por todos os nodes do script
		if elem.get("key") != None: # verifica se node tem atributo key
			if elem.attrib["key"] == key:
				return elem



# busca e insere na lista os links que tem att_from igual ao from do link
def busca_links(att_from):
    achou_link = False
    for i in range(len(links_node)):
        if att_from == links_node[i].attrib["from"]:
            fila_links.append(links_node[i])
            achou_link = True
    return achou_link


# executa os comandos que estão na pilha de links
def link_process(anterior = -1):
    global play
    print("play state............", play)
    gui.terminal.insert(INSERT, "\n---------------------------------------------------")
    gui.terminal.insert(INSERT, "\nstate: Starting the script: " + root.attrib["name"])
    gui.terminal.see(tkinter.END)
    global fila_links
    while (len(fila_links) != 0) and (play == True):
        from_key = fila_links[0].attrib["from"] # chave do comando a executar
        to_key = fila_links[0].attrib["to"] # chave do próximo comando
        print("from:", from_key, ", to_key:", to_key)
        comando_from = busca_commando(from_key).tag # Tag do comando a ser executado
        comando_to = busca_commando(to_key).tag # DEBUG

        # evita que um mesmo nó seja executado consecutivamente. Isso acontece com o nó que antecede os cases
        if anterior != from_key:
            exec_comando(busca_commando(from_key))
            anterior = from_key
            print("Ant: ", anterior, ", from: ", from_key)
        
        
        if (comando_from == "case") or (comando_from == "default"): # se o comando executado foi um case ou um default
            if eva_memory.reg_case == 1: # verifica a flag pra saber se o case foi verdadeiro
                fila_links = [] # esvazia a fila, pois o fluxo seguira deste no case em diante
                print("pulando comando = ", comando_from)
                # segue o fluxo do case de sucesso buscando o prox. link
                if not(busca_links(to_key)): # se nao tem mais link, o comando indicado por to_key é o ultimo do fluxo
                    exec_comando(busca_commando(to_key))
                    print("fim de bloco.............")
                    
            else:
                print("O elemento:", comando_from, " será removido da fila...")
                fila_links.pop(0) # se o case falhou, ele é retirado da fila e consequentemente seu fluxo é descartado
                print("false")
        else: # se o comando nao foi um case
            print("O elemento:", comando_from, " será removido da fila...")
            fila_links.pop(0) # remove o link da fila
            """ ####### inseri aqui
            if len(fila_links) == 0:
                exec_comando(busca_commando(from_key))
                print(from_key, to_key)
            ####### """
            if not(busca_links(to_key)): # como já comentado anteriormente
                exec_comando(busca_commando(to_key))
                print("fim de bloco.............")
    gui.terminal.insert(INSERT, "\nstate: End of script.")
    gui.terminal.see(tkinter.END)
    # restore the buttons states (run and stop)
    gui.bt_run['state'] = NORMAL
    gui.bt_run.bind("<Button-1>", runScript)
    gui.bt_import['state'] = NORMAL
    gui.bt_import.bind("<Button-1>", importFileThread)
    gui.bt_stop['state'] = DISABLED
    gui.bt_stop.unbind("<Button1>")


gui.mainloop()
