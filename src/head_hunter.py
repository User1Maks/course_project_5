import json

import requests


class HeadHunterEmployer:
    """
    Класс для работы с API сайта HeadHunter. Получение данных о
    работодателе
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/employers'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'text': '', 'locale': 'RU', 'per_page': 100,
                       'only_with_salary': True}
        self.employers = []

    def load_employers(self, keyword: str):
        """
        Загружаем список работодателей для выбора 10 из них
        :param keyword: Слово для поиска компании
        """
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers,
                                    params=self.params)
            employers = response.json()['items']
            self.employers.extend(employers)
            self.params['page'] += 1
        return self.employers


class HeadHunterVacancy:
    """Класс для работы с API сайта HeadHunter. Получения данных о вакансиях"""

    def __init__(self, employer_id):
        """
        Конструктор класса  HeadHunter
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'area': 113, 'currency': 'RUR',
                       'per_page': 100, 'employer_id': employer_id}
        self.vacancies = []

    def load_vacancies(self):
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers,
                                    params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies
