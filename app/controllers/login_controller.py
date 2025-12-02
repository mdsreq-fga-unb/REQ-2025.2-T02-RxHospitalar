#config user

import json
import os 
from app.utils.path import get_resource_path



def get_json_path():    return os.path.join(os.path.dirname(__file__), "user.json")
path_final_json = get_resource_path(get_json_path())

def get_user(username, password):
    path = path_final_json
    if not os.path.exists(path):
        print("[ERRO] Arquivo user.json não encontrado!")
        return False
    
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("username") == username and data.get("password") == password

    

def get_email():
    path = get_json_path()
    if not os.path.exists(path):
        return None
    
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("email")
        
def change_password(new_password):
    path = get_json_path()
    if not os.path.exists(path):
        print("[ERRO] Arquivo user.json não encontrado!")
        return False

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    data["password"] = new_password

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return True