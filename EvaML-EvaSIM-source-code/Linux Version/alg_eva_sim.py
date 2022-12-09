import xml.etree.ElementTree as ET

# variaveis da vm
script_file = "script01_EvaML.xml"
tree = ET.parse(script_file)  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")

def run_command(node):
    print("Executando o comando: ", node.tag)
    return

def run_script():
    fila_links = []
    anterior = -1
    fila_links.append(links_node[0])
    while(len(fila_links)) != 0:
        link = fila_links.pop(0)
        if anterior != link.attrib["from"]: # não foi executado na passada anterior
            print("Executa o comando com id: ", link.attrib["from"])
        else:
            if len(fila_links) == 0:
                print("Executa o comando com id: ", link.attrib["from"])
            else:
                pass
        
        anterior = link.attrib["from"] # armazena o id do comando que foi executado

        # busca link ou links que tenham "from" igual ao "to" do comando que acabou de ser executado e o(s) coloca(m) na fila
        for i in range(len(links_node)):
            if links_node[i].attrib["from"] == link.attrib["to"]:
                fila_links.append(links_node[i])
    
    print("Executa o comando final com id: ", link.attrib["to"])
    print("Fim...")


run_script()
