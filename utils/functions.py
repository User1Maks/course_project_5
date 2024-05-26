import json
import os
from config import ROOT_DIR


def default_employers_id() -> list:
    """
    Выбираем ID 10 компаний по умолчанию и возвращаем список.
    :return: Список ID работодателей выбранные по умолчанию из файла
    """
    path = os.path.join(ROOT_DIR, 'data', 'default_id_employers.json')

    list_ids_employers = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for employer_id in json.load(file):
                for id_emp in employer_id.values():
                    list_ids_employers.append(id_emp)
            return list_ids_employers
    except FileNotFoundError:
        print('Файл не найден')
