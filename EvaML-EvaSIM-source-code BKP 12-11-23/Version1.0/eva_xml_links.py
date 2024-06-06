from platform import node
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
pilha = [] # pilha de nodes (enderecos)

###############################################################################
# aqui estão os métodos que geram os links que conectam os nós                #
###############################################################################

lista_links = [] # lista provisoria com os links gerados

def cria_link(node_from, node_to):
    # node stop como node_to
    if (node_to.tag == "stop"): # stop nao pode ser node_to
        return

    # node goto como node_from
    if (node_from.tag == "goto"): # goto nao pode ser node_from
        return


    # a conexão de um switch com outro elemento deve fazer com que o ultimo elemento de cada <case> seu (do switch) se conecte ao node_to
    # a concexão não ocorrerá caso o ultimo elemento de um <case> seja o <stop> ou seja um <goto>
    if node_from.tag == "switch":
        # Eu pensei que esse caso não funcionasse, mas ele funcionou tanto no robô quanto no EvaSIM
        for case_elem in node_from:
            qtd = len(case_elem)
            # só precisamos do ultimo elemento de cada bloco case/default
            if (qtd == 0): # case vazio, conecta o <case> ao node_to
                cria_link(case_elem, node_to)
            else:
                # caso do <stop> e do <goto>. Nesses casos ocorre um bypass
                if (case_elem[qtd -1].tag == "stop") or (case_elem[qtd -1].tag == "goto"):
                    pass
                else: # caso seja outro comando, cria a conexao do comando com o node_to
                    cria_link(case_elem[qtd -1], node_to)
        return

    # node <goto> com node_to. O node_to, é substituido pelo nó indicado no atrib. "target" do <goto>
    if node_to.tag == "goto":
        target_found = False # indica se o id referenciado no target foi encontrado
        for elem in script_node.iter(): # procura por target na interação
            if elem.get("id") != None:
                if elem.attrib["id"] == node_to.attrib["target"]:
                    # cria um link entre o no que queria se conectar ao goto (node_from) e o no para o qual o goto aponta
                    # isso trás mais flexibilidade à conexão de nós que se conectam a elementos goto
                    # com isso, um switch passou a poder ter o atributo id
                    cria_link(node_from, elem)
                    # lista_links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
                    target_found = True
        if not (target_found):
            # target id not found
            print('  Error -> The <goto> "target" attribute was not found:', node_to.attrib["target"])
            exit(1) # termina com erro
        return

    # "node_to" e' uma folha, que nao contem filhos. ex.: <wait>, <light>, <case> vazio e etc
    if len(node_to) == 0:
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for case_elem in node_to:
            # todas os cases passam a ter o atrib. "var" igual ao "var" do switch (node_to)
            # sempre havera conteudo em var do <switch>. Isso é garantido pelo xmlschema
            # restrição. "exact" e "contain" só podem ser usados com va="$"" no switch.
            if case_elem.tag == "case":
                case_elem.attrib["var"] = node_to.attrib["var"] # copia "var" do <switch> para <case>
                if case_elem.attrib["var"].isnumeric(): # var só pode conter vars e nunca números (ESSA RESTRIÇÃO FOI MINHA OPÇÃO)
                    print('  Error -> The use of constants of any type in the "var" attribute of the <switch> command is not allowed. Please, check var="' + node_to.attrib["var"] + '"')
                    exit(1) # termina com erro
                if ("$" not in case_elem.attrib["var"]) and (case_elem.attrib["op"] == "exact"):
                    # uso indevido de exact com outra variavel que não é o $
                    print('  Error -> The "exact" comparison type should only be used with var="$" and not with var="' + node_to.attrib["var"] + '"')
                    exit(1) # termina com erro
                if ("$" not in case_elem.attrib["var"]) and (case_elem.attrib["op"] == "contain"): 
                    # uso indevido de contain com outra variavel que não é o $
                    print('  Error -> The "contain" comparison type should only be used with var="$" and not with var="' + node_to.attrib["var"] + '"')
                    exit(1) # termina com erro
                # o uso de $ com indices, em var e em value, não é permitido no robô físico
                # uso indevido de $ com indice no atributo var do <switch>  
                if ("$" in case_elem.attrib["var"]) and (len(case_elem.attrib["var"]) > 1):
                    print('  Error -> Do not use "$" associated with an index in a "var" attribute of a <switch>, only use it in the texts of the <talk> command')
                    exit(1) # termina com erro 
                # uso indevido de $ com indice no atributo value do <case>  
                if ("$" in case_elem.attrib["value"]) and (len(case_elem.attrib["value"]) > 1):
                    print('  Error -> Do not use "$" associated with an index in a "value" attribute of a <case>, only use it in the texts of the <talk> command')
                    exit(1) # termina com erro 

            elif case_elem.tag == "default": # preenche o default com os parametros default
                # nao precisa de var="$" pois sendo do tipo exact, o robô físico sabe que var="$"
                # e no EvaSIM, um case (default) é sempre verdadeiro
                case_elem.attrib["value"] = ""
                case_elem.attrib["op"] = "exact"

            # gera o link de node_from (que veio na chamada) com o elem. (case ou default)
            #lista_links.append(node_from.attrib["key"] + "," + case_elem.attrib["key"])
            cria_link(node_from, case_elem)
            
    # processa os node_to do tipo <case>            
    elif (node_to.tag == "case") or (node_to.tag == "default"):
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        # caso o case não seja vazio, gera o link entre o <case> e o primeiro elemento e depois processa o conteudo do <case>
        if (len(node_to) == 0): # case o <case> seja vazio
            # nao conecta o <case>
            pass
        else: # verifica se o elemento node_from está antes do case, para evitar que os elementos dos cases gerem links que já foram gerados
            # caso o node_from esteja antes (key menor) blz! Cases esteja depois, apenas é gerado o link entre node_from e os cases,
            # sem o processamento dos elementos internos ao case, que já foram processados anteriormente
            if (node_to.attrib["child_proc"] == "false"): # verifica se o case/defalut já teve eus elementos processados
                node_to.attrib["child_proc"] = "true" # marca o case/default como já processado
                cria_link(node_to, node_to[0]) # conecta o <case> com o seu primeiro elemento filho
                link_process(node_to) # processa a lista de elem. do <case>


def link_process(node_list):

    qtd = len(node_list)

    for i in range(0, qtd-1): # processa uma lista de nós (dois a dois) A->B, B->C,...,Y->Z
        node_from = node_list[i]
        node_to = node_list[i+1]

        # emite um aviso caso haja elemento(s) após um <goto>
        # se esse elemento não for referenciado em outra parte do script, ele poderá ficar desconectado do fluxo.
        if node_from.tag == "goto":
            print("  WARNING - There are elements after the <goto>. These elements may not be reached.")

        # case especifico da tag <stop> que deve interromper a conexao dos do fluxo sendo processado
        # todos os elem. após um <stop> são removidos. O parser emite um aviso de remoção e os exibe no terminal.
        if (node_from.tag == "stop"):
            for s in range(i, qtd-1):
                if (node_list[i+1].get("id")) == None:
                    print("  WARNING - Removing unused (unreachable) commands ... <" + node_list[i+1].tag + ">")
                else:
                    # emite um aviso especial caso um elemento com id seja excluído.
                    print('  WARNING - Removing unused (unreachable) commands ... <' + node_list[i+1].tag + '>. ALERT! This element has an attribue "id" and it is "' + node_list[i+1].attrib["id"] + '"')
                    exit(1)
                node_list.remove(node_list[i+1])
            break
        else:
            cria_link(node_from, node_to)
        

def saida_links():
    # insere a tag links como ultimo elemento de root (<evaml>)
    # len(root) retorna o valor que sera o indice para o ultimo elemento
    tag_links = ET.Element("links") # cria a tag links (mae de varios links)
    root.insert(len(root), tag_links) #

    for i in range(len(lista_links)): # insere cada link como os atributos from e to, dentro do elemento <links>
        tag_link = ET.Element("link", attrib={"from" : lista_links[i].split(",")[0], "to" : lista_links[i].split(",")[1]})
        root[len(root) - 1].insert(i, tag_link)

# inserindo o elemento voice como primeiro elemento do script_node a ser processado
# neste caso, o elem. voice é inserido (temporriamente) para que ele seja sempre o primeiro elemento a ser processado
root.find("script").insert(0, root.find("settings").find("voice"))

# processa os links na lista de links auxiliar
link_process(script_node)

# gera os links no arquivo xml
saida_links()

# verifica se há elementos não referenciados nos links (exceto para: 'voice', 'script', 'switch', 'stop', 'goto')
links_node = root.find("links")
script_node = root.find("script")
excluded_nodes = set(['voice', 'script', 'switch', 'stop', 'goto'])
error = False
for elem in script_node.iter():
    encontrado = False
    for link in links_node.iter():
        if (elem.get("key") != None):
            if (elem.get("key") == link.get("to")):
                encontrado = True
                break
    if not (encontrado) and not (elem.tag in excluded_nodes):
        error = False # para que o erro interrompa o parser, trocar para True
        # a descontinuidade no grafo de execução, gera mais de um grafo, e faz com que o script não execute no robô, porém funciona no simulador
        error_msg = "  WARNING -> The element <" + elem.tag + "> is disconnected from the execution flow. Attributes: "
        for info in elem.attrib.items():
            error_msg += '('
            error_msg += ' = '.join(info)
            error_msg += '),'
        # o erro abaixo foi resolvido com a função que adiciona os defaults automaticamente no módulo de expansão de macros    
        # error_msg += '\n  WARNING: This may indicate the lack of a <default> element within a <switch>.'
        print(error_msg)

if error:
    exit(1)

print("step 03 - Creating the Elements <link>... (OK)")

# O elemento voice foi inserido ao script_node (list) para processamento, somente. 
# Agora será removido da seção script
script_node.remove(root.find("script").find("voice"))

# arquivo de saida
tree.write(root.attrib['name'] + "_EvaML.xml", "UTF-8") # versao para o EvaSIM


#tree.write("_xml_links.xml", "UTF-8") # versao para a etapa 4 do parser
