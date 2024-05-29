import json
import os
from config import ROOT_DIR
from src.class_dbmanager import DBManager


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


def working_with_a_database():
    """Функция для работы с базой данных"""

    db_manager = DBManager()

    while True:
        user_input = input('Главное меню работы с базой данных (БД)\n'
                           '1 - получить список всех компаний и количество '
                           'вакансий у каждой компании\n'
                           '2- получить список всех вакансий с указанием '
                           'названия компании, названия вакансии и зарплаты и '
                           'ссылки на вакансию\n'
                           '3 - получить среднюю зарплату по вакансиям\n'
                           '4 - получить список всех вакансий, у которых '
                           'зарплата выше средней по всем вакансиям\n'
                           '5 - получить список всех вакансий, в названии '
                           'которых содержатся переданные в метод слова, '
                           'например python\n'
                           '6 - завершить работу\n'
                           )
        list_user_input = ['1', '2', '3', '4', '5', '6']
        if user_input not in list_user_input:
            print('Выберите действие и введите цифру соответсвующую '
                  'описанию действия')
            continue

        elif user_input == '1':
            list_data = db_manager.get_companies_and_vacancies_count()
            for employer in list_data:
                print(f'Название кампании: {employer[0]}\n'
                      f'Количество вакансий кампании: {employer[1]}\n'
                      f'------------------------------------------')

        elif user_input == '2':
            list_data = db_manager.get_all_vacancies()
            for vacancy in list_data:
                print(f'Название кампании: {vacancy[0]}\n'
                      f'Название вакансии: {vacancy[1]}\n'
                      f'Зарплата от {vacancy[2]} до {vacancy[3]} '
                      f'{vacancy[4]}\n'
                      f'Ссылка на вакансию: {vacancy[5]}\n'
                      f'------------------------------------------')

        elif user_input == '3':
            list_data = db_manager.get_avg_salary()
            print(f'Средняя заработная плата: {list_data}')

        elif user_input == '4':
            list_data = db_manager.get_vacancies_with_higher_salary()
            for vacancy in list_data:
                print(f'Название вакансии: {vacancy[0]}\n'
                      f'Заработная плата от {vacancy[1]} до {vacancy[2]}\n'
                      f'------------------------------------------')

        elif user_input == '5':
            user_keyword = input('Введите слово для поиска: ')
            list_data = db_manager.get_vacancies_with_keyword(user_keyword)
            for employer in list_data:
                print(f'Название кампании: {employer[0]}\n'
                      f'Название вакансии: {employer[1]}\n'
                      f'------------------------------------------')
        elif user_input == '6':
            break
    db_manager.cur.close()
    db_manager.conn.close()


if __name__ == '__main__':
    print(working_with_a_database())
