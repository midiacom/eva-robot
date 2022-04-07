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


# expande as macros   
macro_expander(script_node, macros_node)

if _error == 1:
    exit(1)

print("Step 01 - Processing Macros... (OK)")

if macros_node != None:
    root.remove(macros_node) # remove a secao de macros, caso ela exista

# gera o arquivo com as macros expandidas (caso existam) para a proxima etapa
tree.write("_macros.xml", "UTF-8")

