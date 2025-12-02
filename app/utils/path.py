#para configurar o caminho dos recursos da planilha corretamente para o executavel criado com PyInstaller
# app/utils/paths.py
import sys
import os

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