#para configurar o caminho dos recursos da planilha corretamente para o executavel criado com PyInstaller
# app/utils/paths.py
import sys
import os
import shutil

def get_resource_path(relative_path):
    """
    Retorna o caminho absoluto para o recurso, funcionando tanto
    em desenvolvimento quanto após o build com PyInstaller.
    """
    try:
        # 1. Tenta pegar o caminho temporário do PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # 2. Se falhar (estamos em Dev), calcula a raiz baseada NESTE arquivo.
        # Estamos em: Projeto/app/utils/paths.py
        # Queremos:   Projeto/
        
        # Pega a pasta onde paths.py está (app/utils)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Sobe dois níveis para chegar na raiz (sai de utils, sai de app)
        base_path = os.path.dirname(os.path.dirname(current_dir))

    return os.path.join(base_path, relative_path)

def get_writable_path(filename):
    """
    Retorna o caminho para arquivos que precisam ser editáveis (como user.json).
    Usa AppData no Windows ou diretório home em outros sistemas.
    """
    if sys.platform == "win32":
        # Windows: usa AppData/Local
        app_data = os.getenv('LOCALAPPDATA')
        app_folder = os.path.join(app_data, 'RxHospitalar')
    else:
        # Linux/Mac: usa pasta oculta no home
        home = os.path.expanduser('~')
        app_folder = os.path.join(home, '.rxhospitalar')
    
    # Cria a pasta se não existir
    os.makedirs(app_folder, exist_ok=True)
    
    file_path = os.path.join(app_folder, filename)
    
    # Se o arquivo não existe, copia do template
    if not os.path.exists(file_path):
        try:
            # Tenta copiar do pacote (recurso incluído no executável)
            template_path = get_resource_path(os.path.join('app', 'controllers', filename))
            if os.path.exists(template_path):
                shutil.copy2(template_path, file_path)
                print(f"[INFO] Arquivo {filename} criado em: {file_path}")
        except Exception as e:
            print(f"[AVISO] Não foi possível copiar template: {e}")
            # Cria um arquivo padrão se a cópia falhar
            if filename == 'user.json':
                import json
                default_data = {
                    "username": "admin",
                    "email": "admin@",
                    "password": "admin"
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)
                print(f"[INFO] Arquivo padrão {filename} criado em: {file_path}")
    
    return file_path