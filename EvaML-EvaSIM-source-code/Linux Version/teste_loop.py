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
# Processamento (loop)                                                        #
###############################################################################
def process_loop(script_node):
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: process_loop(script_node[i])
        if script_node[i].tag == "loop":
            print(i, script_node[i].tag)
            aux_element = copy.deepcopy(script_node[i]) # copia os elementos internos ao loop
            c = ET.Element("counter"); # cria o <counter>
            if script_node[i].get("id") != None:
                id_loop = script_node[i].attrib["id"];
                c.attrib["id"] = id_loop;
            var_loop = script_node[i].attrib["var"];
            times_loop = script_node[i].attrib["times"];
            c.attrib["var"] = var_loop;
            c.attrib["op"] = "=";
            c.attrib["value"] = "0"; # inicializa a variavel contadora com zero
            print("QWWWWW")
            script_node.remove(script_node[i]) # remove o elemento <loop>
            script_node.insert(i, c); # adiciona o <counter>

            s = ET.Element("switch"); # cria o elemento <switch>
            s.attrib["id"] = "_LOOP_ID_" + var_loop; # prefixo padrao do id automatico gerado para o loop _LOOP_ID_
            s.attrib["var"] = var_loop;
            script_node.insert(i + 1, s); # adiciona o <switch>, com seus filhos, ao elemento script

            cs = ET.Element("case");# cria o elemento <case>
            cs.attrib["op"] = "lt";
            cs.attrib["value"] = times_loop;

            c = ET.Element("counter"); # cria o <counter>
            c.attrib["var"] = var_loop;
            c.attrib["op"] = "+";
            c.attrib["value"] = "1";

            cs.insert(0, c);
            #cs.insert(1, aux_element); # aqui, o elemento pai (loop) vem junto, e isso é ruim pois queremos apenas seus filhos
            cs.extend(aux_element); # o extend adiciona apenas os filhos de loop

            g = ET.Element("goto"); # cria o <goto> que faz o loop acontecer
            g.attrib["target"] = "_LOOP_ID_" + var_loop; # prefixo padrao do id automatico gerado para o loop _LOOP_ID_

            cs.append(g); # adiciona o <goto> ao final do <case> 

            df = ET.Element("default") # cria o elemento <default> para o <case> do loop

            s.insert(0, cs);
            s.insert(1, df);

            process_loop(script_node)
            #ET.SubElement(cs, aux_element) # adiciona o conteudo do loop ao <case>
            #x = ET.SubElement(s, cs); # adiciona o case ao <switch>
            #script_node.insert(i + 1, s); # adiciona o <switch>, com seus filhos, ao elemento script 


####################
def print_tree(tree, tab):
    for i in range(len(tree)):
        print(" " * tab, tree[i].tag)
        if len(tree[i]) != 0:
            print_tree(tree[i], tab + 2)


# expande as macros   
macro_expander(script_node, macros_node)

process_loop(script_node)

print_tree(root, 2)

if _error == 1:
    exit(1)

print("Step 01 - Processing Macros... (OK)")

if macros_node != None:
    root.remove(macros_node) # remove a secao de macros, caso ela exista

# gera o arquivo com as macros expandidas (caso existam) para a proxima etapa
tree.write("_macros.xml", "UTF-8")

