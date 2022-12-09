"""
Nesta etapa, caso o script contenha o comando <useMacro>, o parser acusa um erro,
caso não  haja a seção macros e também, caso não haja macros definidas.
Ele também acusa um erro, caso o comando <useMacro> faça referência a uma macro que não foi definida.
O parser indica o nome da macro que não foi encontrada.
Uma definição de macro não pode ser vazia (isso não faria sentido).
Caso algum comando <useMacro> faça referência a uma macro com zero elementos o parser vai indicar o erro.
O parser substitui a tag <useMacro> com problema, por uma tag <error> indicando o tipo do erro,
nesse caso “undefined_macro”, o nome da macro não definida e escreve essa informação no no arquivo de saída da etapa.
 """

import copy # lib para a geracao de copias de objetos
import sys
import xml.etree.ElementTree as ET
import eva_validator # funcão de validacao xmlschema

_error = 0 # 0 indica que não houve falha na etapa. 

tree = eva_validator.evaml_validator(sys.argv[1]) # chama a funcao de validacao do modulo eva_validator

if tree == None: # tree == None indica que houve erro de validaçao, senão, tree tem o objeto xml carregado
    exit(1) # termina com erro

root = tree.getroot() # evaml root node
script_node = root.find("script")
macros_node = root.find("macros")

id_loop_number = 0  # id usado na criação dos ids dos loops

###############################################################################
# Processamento (expansao) das macros                                         #
###############################################################################

def macro_expander(script_node, macros_node):
    global _error
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: macro_expander(script_node[i], macros_node)
        if script_node[i].tag == "useMacro":
            if (macros_node == None): # testa se a seção macros foi criada
                print("  Error -> You are using <useMacro> but the section macros does not exist.")
                _error = 1 # falha
                break
            elif (len(macros_node) == 0): # nenhuma macro foi definida
                print("  Error -> You are using <useMacro> but no macro was defined.")
                _error = 1 # falha
                break
            match_macro = False
            for m in range(len(macros_node)):
                if macros_node[m].attrib["id"] == script_node[i].attrib["macro"]:
                    match_macro = True
                    if (len(macros_node[m])) == 0:
                        script_node[i].tag = "error"
                        _error = 1 # falha
                        script_node[i].attrib["type"] = "macro_is_empty"
                        script_node[i].attrib["macro_id"] = script_node[i].attrib["macro"]
                        print("  Error -> The <useMacro> references the macro", macros_node[m].attrib["id"], "that is empty." )
                        script_node[i].attrib.pop("macro")
                    else:
                        script_node.remove(script_node[i])

                    for j in range(len(macros_node[m])):
                        mac_elem_aux = copy.deepcopy(macros_node[m][j])
                        script_node.insert(i + j, mac_elem_aux)
                    break      
            if match_macro == False: # caso o nome da macro não seja encontrado nas macros
                script_node[i].tag = "error"
                _error = 1 # falha
                script_node[i].attrib["type"] = "undefined_macro"
                script_node[i].attrib["macro_id"] = script_node[i].attrib["macro"]
                print("  Error -> The <useMacro> references an element that is not a macro. Element ID:", script_node[i].attrib["macro"])
                script_node[i].attrib.pop("macro")  
            
            macro_expander(script_node, macros_node)


###############################################################################
# Processamento o comando (loop)                                              #
###############################################################################
def process_loop(script_node):
    global id_loop_number
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: process_loop(script_node[i])
        if script_node[i].tag == "loop":
            id_loop_number += 1 # var utilizada na criação de nomes de algumas variáveis automáticas. Comeca com 1
            loop_copy = copy.deepcopy(script_node[i]) # copia o elemento  <loop>
            c = ET.Element("counter") # cria o <counter> que inicializa a var de iteração com o valor zero
            if script_node[i].get("id") != None: # caso o <loop> seja alvo de um goto
                id_loop = script_node[i].attrib["id"] 
                c.attrib["id"] = id_loop
            if script_node[i].get("var") != None: 
                var_loop = script_node[i].attrib["var"] 
                c.attrib["var"] = var_loop
            else: # caso o usuario não defina uma variação para a iteração, a variavel default "ITERATION_VAR...." será criada
                # id_loop_number += 1 # var utilizada na criação de nomes de algumas variáveis automáticas. Comeca com 1
                var_loop = "ITERATION_VAR" + str(id_loop_number) 
            times_loop = script_node[i].attrib["times"] 
            c.attrib["var"] = var_loop 
            c.attrib["op"] = "=" 
            c.attrib["value"] = "1"  # inicializa a variavel contadora com zero

            script_node.remove(script_node[i]) # remove o elemento <loop> pois não é mais necessário (temos a sua cópia em )
            script_node.insert(i, c)  # adiciona o <counter> que inicializa a variavel de iteração

            s = ET.Element("switch")  # cria o elemento <switch>
            s.attrib["id"] = "LOOP_ID" + str(id_loop_number) + "_" + var_loop  # prefixo padrao do id automatico gerado para o loop _LOOP_ID_
            s.attrib["var"] = var_loop 
            script_node.insert(i + 1, s)  # adiciona o <switch>, com seus filhos, ao elemento script

            cs = ET.Element("case") # cria o elemento <case>
            cs.attrib["op"] = "lte" 
            cs.attrib["value"] = times_loop 

            ####
            ####



            #cs.insert(1, loop_copy)  # aqui, o elemento pai (loop) vem junto, e isso é ruim pois queremos apenas seus filhos
            cs.extend(loop_copy)  # o extend adiciona apenas os filhos de loop

            c = ET.Element("counter")  # cria o <counter> que incrementa a variável de iteração
            c.attrib["var"] = var_loop
            c.attrib["op"] = "+"
            c.attrib["value"] = "1"
            cs.append(c)

            g = ET.Element("goto")  # cria o <goto> que faz o loop acontecer
            g.attrib["target"] = "LOOP_ID" + str(id_loop_number) + "_" + var_loop  # prefixo padrao do id automatico gerado para o loop _LOOP_ID_

            cs.append(g)  # adiciona o <goto> (que gerar causa a repetição) ao final do <case> 

            df = ET.Element("default") # cria o elemento <default> para o <case> do loop

            s.insert(0, cs)  # insere o <case> com o corpo dentro do <switch>
            s.insert(1, df)  # insere o comando <default> que gera a conexão com o restante do script, evitando a descontinuidade

            process_loop(script_node) # o processamento de um loop muda a estrutura inicial do scriptnode e precisa ser revisitada

###############################################################################
# Insere <defaults> nos <cases>                                               #
###############################################################################
# esta função adiciona um <default> aos cases que não o tem.
# esta ação evita que em um grafo de execução (script) possa haver uma desconexão, gerando mais de um grafo
# isso acaba adicionando um <default> desnecessário em alguns casos, mas evita o problema da desconexão
# caso esta função seja desativada aqui, o parser emitirá um WARNING indicando a descontinuidade, caso haja alguma
# um script, que neste caso, possui dois grafos, é executado no EvaSIM, porém, não roda no robô físico
def default_process(script_node):
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: default_process(script_node[i])
        if script_node[i].tag == "switch":
            if script_node[i][len(script_node[i]) - 1].tag != "default":
                df = ET.Element("default") # cria o elemento <default> para o <case> do loop
                s = script_node[i]
                s.insert(len(script_node[i]), df)

#################### Funcao auxiliar para a impressao da arvore
def print_tree(tree, tab):
    for i in range(len(tree)):
        print(" " * tab, tree[i].tag)
        if len(tree[i]) != 0:
            print_tree(tree[i], tab + 2)


# expande as macros   
macro_expander(script_node, macros_node)

# processa os loops
process_loop(script_node)

# insere <defaults> nos <cases> que não os têm, eitando possíveis descontinuidades nos fluxos (grafos)
default_process(script_node)

#print_tree(root, 2)

if _error == 1:
    exit(1)

print("Step 01 - Processing Macros... (OK)")

if macros_node != None:
    root.remove(macros_node) # remove a secao de macros, caso ela exista

# gera o arquivo com as macros expandidas (caso existam) para a proxima etapa
tree.write("_macros.xml", "UTF-8")


