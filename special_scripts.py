from shutil import rmtree
import os


def clear_cache():
    """Удаляет папки '__py_cache__' при запуске бота"""
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            path = os.path.join(root, '__pycache__')
            rmtree(path)