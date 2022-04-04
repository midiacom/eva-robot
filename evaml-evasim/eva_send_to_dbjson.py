import sys
import json

def send_to_dbjson(script_id, script_name, output):
    print("==> Saving [" + script_name + "], id[" + script_id + "] into db.json")
    
    # read db.json
    dbfile = open('db.json', 'r')

    # transforma o arquivo de texto em um dict
    eva_db_dict = json.load(dbfile)

    # se o script já existe no bd, então apaga
    for item in range(len(eva_db_dict["interaccion"])):
        if eva_db_dict["interaccion"][item]['_id'] == script_id:
            #print("o script de id", eva_db_dict["interaccion"][item]['_id'], "será deletado")
            del(eva_db_dict["interaccion"][item])

    # output é uma string. a função json.loads transforma a string em um dict
    eva_db_dict["interaccion"].append(json.loads(output))

    # gera o arquivo
    with open('../db.json', 'w') as fp:
        json.dump(eva_db_dict, fp)

    #print("\nTotal scripts found:", len(eva_db_dict["interaccion"]))
