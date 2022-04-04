import xml.etree.ElementTree as ET
import xmlschema # xmlschema validation
from pprint import pprint

schema = xmlschema.XMLSchema("EvaML-Schema/evaml_schema.xsd")

evaml_file = "teste3.xml"
result = schema.to_dict(evaml_file, converter=xmlschema.JsonMLConverter)
      #pprint(result)
def cria_xml(lista, parent):
  if type(lista) != list: # é apenas uma string ( tag = lista)
    ET.SubElement(parent, lista)
  else:
    tag = lista[0] # primeiro elem sempre é a tag

    if len(lista) == 2: # possui tag e (atributos ou lista de elem.)
      if type(lista[1]) == dict: # verifica se o segundo elemento é o dic. de atributos
        ET.SubElement(parent, tag, lista[1]) # cria o elem com seus atributos
      # elif type(lista[1]) == str:
      #   ET.SubElement(parent, lista[1]) # caso seja uma tag com texto
      else: # se não é dict então element list
        no = ET.SubElement(parent, tag) # anexa o Nó em parent
        cria_xml(lista[1], no) # coloca a element list em lista[1] no Nó
    elif len(lista) >= 3:
      if type(lista[1]) == dict: # # verifica se o segundo elemento é o dic. de atributos
        ET.SubElement(parent, tag, lista[1]) # anexa o elem com seus atributos em parent
        for i in (range(len(lista) - 2)):
          cria_xml(lista[i + 2], parent)
      else: # se não é dict então element list
        for i in (range(len(lista) - 1)):
          cria_xml(lista[i + 1], parent)
  #ET.dump(parent)

if len(result) == 4: # nao possui a secao de macros (tag, atrib, settings e script) 
  evaml = ET.Element(result[0], result[1]) # cria o elemento raiz evaml e com seus atributos
  settings = ET.SubElement(evaml, result[2][0])
  cria_xml(result[2], settings)
  script = ET.SubElement(evaml, result[3][0])
  cria_xml(result[3], script)
  xml_processed = ET.tostring(evaml, encoding='utf8').decode('utf8')
  with open("_xml_validated.xml", "w") as text_file: # grava o xml processado (temporario) em um arquivo para ser importado pelo parser
    text_file.write(xml_processed)
  pprint(xml_processed)
  ET.dump(evaml)


    