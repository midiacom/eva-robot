import json
import xml.etree.ElementTree as ET
import re # expressão regular
from pprint import pprint

script = ""
comandos_json= ""
links = ""
links_json = ""
evaml = ""

def converte(json_file_name, tkinter):
  global script, comandos_json, links, links_json, evaml
  # lendo do arquivo json
  with open(json_file_name, 'r') as openfile:
    json_object = json.load(openfile) # é um dict.
      
  comandos_json = json_object["data"]["node"] # Lista de nós. Cada nó (um comando) é um dict. com os seus pares chave/valor do respectivo elemento.
  links_json = json_object["data"]["link"] # Lista de links. Cada link é um dict. com as chaves "from" e "to"

  # cria o elemento raiz <evaml> e seus subelementos
  evaml_atributos = {"name":json_object["nombre"]}
  evaml = ET.Element("evaml", evaml_atributos )
  #
  settings = ET.SubElement(evaml, "settings")
  # add os subelementos de settings com seus atributos
  for comando in comandos_json:
    voice_found = False # 
    if comando["type"] == "voice": # busca comando voice e seus atributos
      voice_atributos = {"tone":comando["voice"], "key":str(comando["key"])}
      comandos_json.remove(comando) # exclui voice para que ele não seja processado na proxima etapa
      voice_found = True
      voice = ET.SubElement(settings, "voice", voice_atributos)
      break
  
    if not voice_found: # voice precisa existir no JSON e precisa ser o primeiro elemento da VPL
      print("Oops! The Voice element is missing...") # it's required that the voice be the first element of VPL
      warning_message = "Sorry! I didn't find the Voice element.\n\nPlease the Voice element must be the first element of the script!\n\nThe EvaSIM will be closed!"
      tkinter.messagebox.showerror(title="Error!", message=warning_message)
      exit(1)

  # este elementos ficam com os valores default pois ainda não foram implementados no robô
  lightEffects_atributos = {"mode":"on"}
  lightEffects = ET.SubElement(settings, "lightEffects", lightEffects_atributos)

  audioEffects_atributos = {"mode":"on",  "vol":"100%"}
  audioEffects = ET.SubElement(settings, "audioEffects", audioEffects_atributos)

  # cria as outras secões do documento EvaML
  script = ET.SubElement(evaml, "script")
  links = ET.SubElement(evaml, "links")

  # chama as funções de processamento
  processa_nodes(script, comandos_json, tkinter) # converte os nós json para nós XML
  processa_links(links, links_json) # converte os links json para links XML


# processamentos dos comandos no arquivo json #######################################################################################
def processa_nodes(script, comandos_json, tkinter):
  for comando in comandos_json:

    # <light>
    if comando["type"] == "light":
      light_atributos = {"key" : str(comando["key"]), "state" : comando["state"].upper(), "color" : comando["lcolor"].upper()}
      ET.SubElement(script, "light", light_atributos)
  

    # <motion>
    elif comando["type"] == "mov":
      # mapeando os tipos de movimentos da cabeça
      if   (comando["mov"] == "n"): motion_type = "YES"
      elif (comando["mov"] == "s"): motion_type = "NO"
      elif (comando["mov"] == "c"): motion_type = "CENTER"
      elif (comando["mov"] == "l"): motion_type = "LEFT"
      elif (comando["mov"] == "r"): motion_type = "RIGHT"
      elif (comando["mov"] == "u"): motion_type = "UP"
      elif (comando["mov"] == "d"): motion_type = "DOWN"
      elif (comando["mov"] == "a"): motion_type = "ANGRY"
      elif (comando["mov"] == "U"): motion_type = "2UP"
      elif (comando["mov"] == "D"): motion_type = "2DOWN"
      elif (comando["mov"] == "R"): motion_type = "2RIGHT"
      else: motion_type = "2LEFT"


      motion_atributo = {"key" : str(comando["key"]), "type" : motion_type}
      ET.SubElement(script, "motion", motion_atributo)


    # <audio>
    elif comando["type"] == "sound":
      audio_atributos = {"key" : str(comando["key"]), "source" : comando["src"], "block" : str(comando["wait"]).upper()}
      ET.SubElement(script, "audio", audio_atributos)


    # <evaEmotion>
    elif comando["type"] == "emotion":
      # mapeando os nomes da expressões (4 expressões)
      if (comando["emotion"] == "anger"): eva_emotion = "ANGRY"
      elif (comando["emotion"] == "joy"): eva_emotion = "HAPPY"
      elif (comando["emotion"] == "ini"): eva_emotion = "NEUTRAL"
      else: eva_emotion = "SAD"

      eva_emotion_atributos = {"key" : str(comando["key"]), "emotion" :eva_emotion}
      ET.SubElement(script, "evaEmotion", eva_emotion_atributos)

    # <leds>
    elif comando["type"] == "led":
      # mapeando os nomes da expressões (4 expressões)
      if (comando["anim"] == "anger"): animatiom = "ANGRY"
      elif (comando["anim"] == "joy"): animatiom = "HAPPY"
      elif (comando["anim"] == "escuchaT"): animatiom = "LISTEN"
      elif (comando["anim"] == "sad"): animatiom = "SAD"
      elif (comando["anim"] == "hablaT_v2"): animatiom = "SPEAK"
      elif (comando["anim"] == "stop"): animatiom = "STOP"
      elif (comando["anim"] == "surprise"): animatiom = "SURPRISE"

      led_atributos = {"key" : str(comando["key"]), "animation" :animatiom}
      ET.SubElement(script, "led", led_atributos)


    # <wait>
    elif comando["type"] == "wait":
      wait_atributos = {"key" : str(comando["key"]), "duration" : str(comando["time"])}
      ET.SubElement(script, "wait", wait_atributos)

    
    # <listen>
    elif comando["type"] == "listen":
      listen_atributos = {"key" : str(comando["key"])}
      ET.SubElement(script, "listen", listen_atributos)

    
    # <random>
    elif comando["type"] == "random":
      random_atributos = {"key" : str(comando["key"]), "min" : str(comando["min"]), "max" : str(comando["max"])}
      ET.SubElement(script, "random", random_atributos)


    # <talk>
    elif comando["type"] == "speak":
      speak_atributos = {"key" : str(comando["key"])}
      talk = ET.SubElement(script, "talk", speak_atributos)
      talk.text = comando["text"]


    # <userEmotion>
    elif comando["type"] == "user_emotion":
      user_emotion_atributos = {"key" : str(comando["key"])}
      ET.SubElement(script, "userEmotion", user_emotion_atributos)


    # <counter>
    elif comando["type"] == "counter":
      # mapping operations types
      if (comando["ops"] == "assign"): op = "="
      elif (comando["ops"] == "rest"): op = "%"
      elif (comando["ops"] == "mul"): op = "*"
      elif (comando["ops"] == "sum"): op = "+"
      elif (comando["ops"] == "div"): op = "/"

      counter_atributos = {"key" : str(comando["key"]), "var" : comando["count"], "op" : op , "value" : str(comando["value"])}
      ET.SubElement(script, "counter", counter_atributos)



    # <if>
    elif comando["type"] == "if":
      exp_logica = comando["text"] # string com a expressao logica do condition
      tag = "case" # temos esta variável aqui, para que, caso seja necessário, criemos o elemento default.
      # mapping "op" types
      if (comando["opt"]) == 4: # exact é sempre comparado com $
        var = "$"
        op = "exact" # exact
        value = exp_logica # neste não tem exp. logica no conteudo, só uma string
        if (value == ""): # caso op seja exact e value "", fica definido aqui o "condicion" como <default>. Isso gera uma restrição na construção de scripts usando a VPL
          tag = "default"
      elif (comando["opt"]) == 2: # contain com $
        op = "contain"
        value = comando["text"]
        var = "$"
      elif (comando["opt"]) == 5: # comparacao matemática
        if ("==" in exp_logica): # faz o map. e retira da expressão, restando apenas os operandos separados por espaçoes vazios
          op = "eq"
          exp_logica = exp_logica.replace("==", "  ")
        elif (">=" in exp_logica):
          op = "gte"
          exp_logica = exp_logica.replace(">=", "  ")
        elif ("<=" in exp_logica):
          op = "lte"
          exp_logica = exp_logica.replace("<=", "  ")
        elif ("!=" in exp_logica):
          op = "ne"
          exp_logica = exp_logica.replace("!=", "  ")
        elif (">" in exp_logica):
          op = "gt"
          exp_logica = exp_logica.replace(">", "  ")
        elif ("<" in exp_logica):
          op = "lt"
          exp_logica = exp_logica.replace("<", "  ")

        # com opt igual 5, comando["text"] tem algo desse tipo #x == 2 ou $ == 2(comparação matematica)
        if ("$" in exp_logica):
          var = "$" # dolar é o primeiro operando.
        else:
          # a exp. logica tem um ou dois operandos do tipo #n
          # a expressão regular retorna uma lista de #x, #y e etc
          var = (re.findall(r'\#[a-zA-Z]+[0-9]*', exp_logica)) 
        
        if (type(var) == str): # type str indica que var é $, caso contrário var é uma lista resultante da expressao regular
          # pegando o "value". tenta ler um numero
          value = (re.findall(r'[0-9]+', exp_logica))
          if (len(value) == 0): # não encontrou um numero na expressao
            # se não é um captura a var #n no oprando da direita
            value = re.findall(r'\#[a-zA-Z]+[0-9]*', exp_logica)[0] # captura a variavel do tipo #n e coloca em value. neste caso precisa ir com #
          else: # encontrou o numero. lembrando que a exp. regular retorna uma lista
            value = value[0] # entao value[0] é a string retornada pela exp. regular
        else: # neste caso $ não está na exp. e var é um lista. precisamos verificar se tem um ou dois elementos
          print(len(var))
          if (len(var) == 1): # o operando da esquerda é uma var #n
            var = var[0][1:] # pegamos a variavle sem o #
            value = (re.findall(r'[0-9]+', exp_logica))[0] # neste caso value só pode ser um número
          else: # var tem dois elementos, ou seja, os dois operandos sao do tipo #n #m
            var = var[0][1:] # pegamos a variable sem o #
            value = var[1] # uma var em value precisa ir com o caracter #
      if_atributos = {"key" : str(comando["key"]), "op" : op, "value" : value, "var" : var}
      ET.SubElement(script, tag , if_atributos)

    # Todos os comandos suportados foram testados
    else:
      warning_message = """Sorry, an unsupported VPL element was found. Please, check your JSON script!

=========================
  Supported VPL Elements List
=========================
        
* Voice
* Random
* Wait
* Talk
* Light
* Motion
* evaEmotion
* Audio
* Led
* Counter
* Condition
* Listen
* userEmotion

The EvaSIM will be closed..."""

      tkinter.messagebox.showerror(title="Error!", message=warning_message)
      exit(1)


# processamentos dos links no arquivo json #######################################################################################################
def processa_links(links, links_json):
  for link in links_json:
    link_atributos = {"from" : str(link["from"]), "to" : str(link["to"])}
    ET.SubElement(links, "link", link_atributos)

  # gera o arquivo XML no disco
  xml_processed = ET.tostring(evaml, encoding="unicode")#.decode('utf8')
  print("Processando XML..............")
  with open("_json_to_evaml_converted.xml", "w") as text_file: # grava o xml processado (temporario) em um arquivo para ser importado pelo parser
      text_file.write(xml_processed)


