import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
output = ""
gohashid = 0

# percorre os elementos xml mapeando-os nos respectivos no modelo Json do Eva
def mapping_xml_to_json():
    global output
    # conjunto de nodes abstratos que nao sao mapeados no Json do robô
    excluded_nodes = set(['script', 'switch', 'stop', 'goto'])
    for elem in script_node.iter():
        if not(elem.tag in excluded_nodes):

            if (elem.tag == 'motion'):
                output += ",\n"
                output += motion_process(elem)

            if (elem.tag == 'audio'):
                output += ",\n"
                output += audio_process(elem)

            if (elem.tag == 'light'):
                output += ",\n"
                output += light_process(elem)

            if (elem.tag == 'led'):
                output += ",\n"
                output += led_process(elem)

            if (elem.tag == 'wait'):
                output += ",\n"
                output += wait_process(elem)

            if (elem.tag == 'talk'):
                output += ",\n"
                output += talk_process(elem)

            if (elem.tag == 'random'):
                output += ",\n"
                output += random_process(elem)

            if (elem.tag == 'listen'):
                output += ",\n"
                output += listen_process(elem)

            if (elem.tag == 'counter'):
                output += ",\n"
                output += counter_process(elem)

            if (elem.tag == 'evaEmotion'):
                output += ",\n"
                output += eva_emotion_process(elem)

            if (elem.tag == 'userEmotion'):
                output += ",\n"
                output += user_emotion_process(elem)

            if (elem.tag == 'case'):
                output += ",\n"
                output += case_process(elem)

            # default é um caso especial do comando case, onde value = ""
            if (elem.tag == 'default'):
                output += ",\n"
                output += case_process(elem)


# head processing (generates the head of json file)
def head_process(node):
    node.attrib["key"] = str(0)
    init = """{
  "_id": """ + '"' + node.attrib["id"] + '",' + """
  "nombre": """ + '"' + node.attrib['name'] + '",' + """
  "data": {
    "node": [
"""
    return init

# processing the settings nodes
# always be the first node in the interaccion
def settings_process(node):
    return voice_process(node.find("voice"))
    # processar lightEffects
    # processar audioEffects

# audio node processing #########################################################################
def audio_process(audio_command):
    global gohashid

    audio_source = audio_command.attrib['source']
    # audioEffects settings processing
    if root.find("settings").find("audioEffects") != None:
      if root.find("settings").find("audioEffects").attrib["mode"] == "OFF":
        # mode off implies the use of MUTED-SOUND file 
        audio_source = "MUTED-SOUND"

    audio_node = """      {
        "key": """ + audio_command.attrib["key"] + """,
        "name": "Audio",
        "type": "sound",
        "color": "lightblue",
        "isGroup": false,
        "src": """ + '"' + audio_source + '",' + """
        "wait": """ + audio_command.attrib['block'].lower() + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return audio_node

# counter node processing #########################################################################
def counter_process(counter_command):
    global gohashid

    if counter_command.attrib['op'] == "=":
      op_eva = "assign"
    elif counter_command.attrib['op'] == "+":
      op_eva = "sum"
    elif counter_command.attrib['op'] == "*":
      op_eva = "mul"
    elif counter_command.attrib['op'] == "/":
      op_eva = "div"
    elif counter_command.attrib['op'] == "%":
      op_eva = "rest"

    counter_node = """      {
        "key": """ + counter_command.attrib["key"] + """,
        "name": "Counter",
        "type": "counter",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "count": """ + '"' + counter_command.attrib['var'] + '",' + """
        "ops": """ + '"' + op_eva + '",' + """
        "value": """ + counter_command.attrib['value'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return counter_node


# light node processing #########################################################################
def light_process(light_command):
    global gohashid

    bulb_state = light_command.attrib['state']
    if bulb_state == "OFF": # a ideia é admitir a ausencia do parametro color quando o estado da lampada for off
      light_command.attrib['color'] = "BLACK" # mesmo se o atributo não tiver sido setado, ele será setado aqui
    
    if (bulb_state == "ON") and (light_command.get("color") == None): 
      light_command.attrib['color'] = "WHITE" # default color "white" mesmo se o atributo não tiver sido setado, ele será setado aqui
    
    color = light_command.attrib['color']
    color_map = {"WHITE":"#ffffff", "BLACK":"#000000", "RED":"#ff0000", "PINK":"#e6007e", "GREEN":"#00ff00", "YELLOW":"#ffff00", "BLUE":"#0000ff"}
    if color_map.get(color) != None:
        color = color_map.get(color)


    # lightEffects settings processing #########################################################################
    if root.find("settings").find("lightEffects") != None:
      if root.find("settings").find("lightEffects").attrib["mode"] == "OFF":
        # mode off implies bulb_state off 
        bulb_state = "OFF"

    light_node = """      {
        "key": """ + light_command.attrib["key"] + """,
        "name": "Light",
        "type": "light",
        "color": "#ffa500",
        "isGroup": false,
        "group": "",
        "lcolor": """ + '"' + color + '",' + """
        "state": """ + '"' + bulb_state.lower() + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return light_node


# listen node processing 
####################################################################################### falta implementar os filtros
def listen_process(listen_command):
    global gohashid
    
    listen_node = """      {
        "key": """ + listen_command.attrib["key"] + """,
        "name": "Listen",
        "type": "listen",
        "color": "#ffff00",
        "isGroup": false,
        "opt": "",
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return listen_node


# motion type processing #########################################################################
def motion_process(motion_command):
    global gohashid

    # mapping 
    if motion_command.attrib['type'] == "YES": # 
      type = "n" # nao esta errado nao!!! yes é mapeado como "n" no robô
    elif motion_command.attrib['type'] == "NO":
      type = "s"
    elif motion_command.attrib['type'] == "CENTER":
      type = "c"
    elif motion_command.attrib['type'] == "LEFT":
      type = "l"
    elif motion_command.attrib['type'] == "RIGHT":
      type = "r"
    elif motion_command.attrib['type'] == "UP":
      type = "u"
    elif motion_command.attrib['type'] == "DOWN":
      type = "d"
    elif motion_command.attrib['type'] == "ANGRY":
      type = "a" # isso mesmo! Nao sei porque usa "a" para raiva
    elif motion_command.attrib['type'] == "2UP":
      type = "U"
    elif motion_command.attrib['type'] == "2DOWN":
      type = "D"
    elif motion_command.attrib['type'] == "2RIGHT":
      type = "R"
    elif motion_command.attrib['type'] == "2LEFT":
      type = "L"
    
    motion_node = """      {
        "key": """ + motion_command.attrib["key"] + """,
        "name": "Motion",
        "type": "mov",
        "color": "lightblue",
        "isGroup": false,
        "mov": """ + '"' + type + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return motion_node


# led animation processing #########################################################################
def led_process(led_command):
    global gohashid

    # mapping 
    if led_command.attrib['animation'] == "STOP": # just to show what is happening here
      animation = "stop"
    elif led_command.attrib['animation'] == "LISTEN":
      animation = "escuchaT"
    elif led_command.attrib['animation'] == "SPEAK":
      animation = "hablaT_v2"
    elif led_command.attrib['animation'] == "ANGRY":
      animation = "anger"
    elif led_command.attrib['animation'] == "HAPPY":
      animation = "joy"
    elif led_command.attrib['animation'] == "SAD":
      animation = "sad"
    elif led_command.attrib['animation'] == "SURPRISE":
      animation = "surprise"
    
    led_node = """      {
        "key": """ + led_command.attrib["key"] + """,
        "name": "Leds",
        "type": "led",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "anim": """ + '"' + animation + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return led_node


# talk node processing #########################################################################
def talk_process(talk_command):
    global gohashid

    # verifica se os atributos foram definidos
    if (talk_command.text == None):
      print("  Error -> There is a <talk> command without a text.")
      exit(1)
    
    talk_command.text = talk_command.text.replace("\n", " ") # remove os "enters", caso existam
    talk_command.text = talk_command.text.replace("\t", " ") # remove os "tabs", caso existam

    talk_node = """      {
        "key": """ + talk_command.attrib["key"] + """,
        "name": "Talk",
        "type": "speak",
        "color": "#00ff00",
        "isGroup": false,
        "text": """ + '"' + talk_command.text + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return talk_node


# voice node processing #########################################################################
def voice_process(voice_command):
  global gohashid
  voice_node = """      {
        "key": """ + voice_command.attrib["key"] + """,
        "name": "Voice",
        "type": "voice",
        "color": "#0020ff",
        "isGroup": false,
        "voice": """ + '"' + voice_command.attrib['tone'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
  gohashid += 1
  return voice_node

# userEmotion node processing #########################################################################
def user_emotion_process(user_emotion_command):
  global gohashid
  user_emotion_node = """      {
        "key": """ + user_emotion_command.attrib["key"] + """,
        "name": "User_Emotion",
        "type": "user_emotion",
        "color": "lightgreen",
        "isGroup": false,
        "group": "",
        "vision": "capture",
        "__gohashid": """ + str(gohashid) + """
      }"""
  gohashid += 1
  return user_emotion_node


# eva_emotion node processing #########################################################################
def eva_emotion_process(eva_emotion_command):
    global gohashid

    # speed 0 é o valor default. Não vejo necessidade de implementar isso

    if eva_emotion_command.attrib['emotion'] == "HAPPY": # compatibiliza com o Eva. O Eva usa joy.
      eva_emotion_command.attrib['emotion'] = "joy"

    if eva_emotion_command.attrib['emotion'] == "ANGRY": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "anger"

    if eva_emotion_command.attrib['emotion'] == "NEUTRAL": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "ini"

    # attrib emotion "SAD" é o mesmo para "sad" para o robo
    # o lower (só transforma para caixa baixa)

    eva_emotion_node = """      {
        "key": """ + eva_emotion_command.attrib["key"] + """,
        "name": "Eva_Emotion",
        "type": "emotion",
        "color": "lightcoral",
        "isGroup": false,
        "group": "",
        "emotion": """ + '"' + eva_emotion_command.attrib['emotion'].lower() + '",' + """
        "level": 0,
        "speed": 0,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return eva_emotion_node


# random node processing #########################################################################
def random_process(random_command):
    global gohashid

    random_node = """      {
        "key": """ + random_command.attrib["key"] + """,
        "name": "Random",
        "type": "random",
        "color": "pink",
        "isGroup": false,
        "group": "",
        "min": """ + random_command.attrib['min'] + ',' + """
        "max": """ + random_command.attrib['max'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return random_node


# condition node (case and default) processing #########################################################################
def case_process(case_command):
  global gohashid
  
  # traducao dos operadores lógicos. Nós usamos o mesmo padrão que NCL
  if case_command.attrib['op'] == "lt":  op = "<"
  if case_command.attrib['op'] == "gt":  op = ">"
  if case_command.attrib['op'] == "eq":  op = "=="
  if case_command.attrib['op'] == "lte": op = "<="
  if case_command.attrib['op'] == "gte": op = ">="
  if case_command.attrib['op'] == "ne":  op = "!=" # preciso verificar este.parece que os mexicanos nao implementaram o not.
    
  # verifica qual o tipo de comparacao para $. Exact ou contain
  if case_command.attrib["op"] == "exact":
    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 4,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return case_node

  elif case_command.attrib["op"] == "contain": # se é "contain"
    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 2,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return case_node

  else: # testando um valor em relacao a outra variavel qualquer
    # é preciso que haja um espaço entre os operandos e o operador. ex #x == 1
    # opt": 5 é comparacao matematica, isto é, com operadores do tipo ==, >, <, >=, <= ou !=

    tralha1 = '"#'
    if case_command.attrib["var"] == "$":
      tralha1 = '"'
    # if case_command.attrib['value'] == "$" or case_command.attrib['value'].isnumeric():
    #   tralha2 = ' '

    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + tralha1 + case_command.attrib['var'] + ' ' + op + ' ' + case_command.attrib['value'] + '",' + """
        "opt": 5,
        "__gohashid": """ + str(gohashid) + """
        }"""
    gohashid += 1
    return case_node


# wait node processing #########################################################################
def wait_process(wait_command):
    global gohashid

    wait_node = """      {
        "key": """ + wait_command.attrib["key"] + """,
        "name": "Wait",
        "type": "wait",
        "color": "lightblue",
        "isGroup": false,
        "time": """ + wait_command.attrib['duration'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return wait_node
        

def saida_links():
    node_links = root.find("links")
    # verifica se há links a processar
    if len(node_links) == 0:
      print('  Error -> No execution flow found. Please, check your code.')
      exit(1)
    output ="""
    ],
    "link": [""" + """
      { 
        "from": """ + node_links[0].attrib["from"] + "," + """
        "to": """ + node_links[0].attrib["to"] + "," + """
        "__gohashid": 0
      }"""

    for i in range(len(node_links) - 1):
        output += """,
      { 
        "from": """ + node_links[i+1].attrib["from"] + "," + """
        "to": """ + node_links[i+1].attrib["to"] + "," + """
        "__gohashid": """ + str(i + 1) + """
      }"""

    output += """
    ]
  }
}"""
  
    return output


print("step 04 - Mapping XML nodes and links to a JSON file... (OK)")

# gerando o cabeçalho do Json
# onde são inseridos o id e o nome da interação baseados nos dados xml
output += head_process(root) # usa os atributos id e name da tag <evaml>

# o proximo comando pega o parametro do elemento voice (timbre) e gera o primeiro elem. do script Json
output += settings_process(root.find("settings"))

# processamento da interação
mapping_xml_to_json() # nova versao

# mapeia os links xml para json
output += saida_links()

# criação de um arquivo físico da interação em json
file_out = open(root.attrib['name'] + '.json', "w")
file_out.write(output)
# file_out.write(output.encode('utf-8')) para rodar no raspberry
file_out.close()

