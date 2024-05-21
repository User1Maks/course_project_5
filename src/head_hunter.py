import json
import os
from pprint import pprint
from config import ROOT_DIR
import requests


class HeadHunterAPI:
    """Класс для работы с API сайта HeadHunter. Получения данных о вакансиях"""

    def __init__(self):
        """
        Конструктор класса  HeadHunterAPI
        """
        self.url = ''
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = ''
        self.vacancies = []
        self.employers = []

    def load_vacancies(self, employer_id) -> list:
        """Метод для загрузки вакансий по ID работодателя"""

        self.url = f'https://api.hh.ru/vacancies'
        self.params = {'page': 0, 'area': 113, 'currency': 'RUR',
                       'per_page': 100, 'employer_id': employer_id}

        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers,
                                    params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies

    @staticmethod
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

    def load_employers(self, list_ids_employers) -> list:
        """Метод для загрузки информации о работодателе по ID"""
        for employers_id in list_ids_employers:
            self.url = f'https://api.hh.ru/employers/{employers_id}'
            self.params = {'locale': 'RU', 'host': 'hh.ru'}
            response = requests.get(self.url, headers=self.headers,
                                    params=self.params)
            employer = response.json()
            self.employers.extend(employer)
            return self.employers


if __name__ == "__main__":
    list_emp1 = HeadHunterAPI().load_vacancies(1740)[:2]
    pprint(list_emp1[0])
