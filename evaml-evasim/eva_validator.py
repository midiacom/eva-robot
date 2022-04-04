from tkinter.tix import Tree
import xml.etree.ElementTree as ET
import xmlschema # xmlschema validation
from pprint import pprint

# schema validation
# este trecho de codigo valida o xml
# podem ocorrer dois tipos de erro (1) xml mal-formado (2) erro de validação
schema = xmlschema.XMLSchema("EvaML-Schema/evaml_schema.xsd")

def evaml_validator(evaml_file): # função que é chamado pelo mod. macro exp.
  global tree
  try:
    valido = True
    val = schema.iter_errors(evaml_file)
    for idx, validation_error in enumerate(val, start=1):
      print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')
      valido = False
  except Exception as e:
    print(val)
    print(e)
    return None
  else:
    if valido == True:
      # obj = schema.decode(evaml_file) # retorna uma estrutura tipo dict com o XML processado (com a inserção dos valores default do schema)
      # xml_validado_element = schema.encode(obj, path="evaml") # codifica a estrutura em obj para um etree.element
      # xml_validade_string = xmlschema.etree_tostring(xml_validado_element, namespaces=False) # converte o etree.element para um xml em string
      # print(xml_validade_string)
      # with open("_xml_validated.xml", "w") as text_file: # grava o xml processado (temporario) em um arquivo para ser importado pelo parser
      #   text_file.write(xml_validade_string)
      return ET.parse(evaml_file) #
    else:
      return None
