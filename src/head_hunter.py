import requests


class HeadHunterEmployers:
    """
    Класс для работы с API сайта HeadHunter. Получения данных о работодателях
    """

    def __init__(self):
        """
        Конструктор класса  HeadHunterEmployers
        """
        self.url = ''
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'locale': 'RU',
                       'area': 113, 'only_with_vacancies': True,
                       'host': 'hh.ru'}
        self.employers = []

    def load_employers(self, list_ids_employers) -> list:
        """Метод для загрузки информации о работодателе по ID"""

        for employers_id in list_ids_employers:
            self.url = f'https://api.hh.ru/employers/{employers_id}'
            response = requests.get(self.url, headers=self.headers,
                                    params=self.params)
            employer = response.json()
            self.employers.append(employer)
            print(f'Выполняется парсинг компании: {employer["name"]}')
        print(f'Выполняется загрузка вакансий...')

        return self.employers


class HeadHunterVacancies:
    """Класс для работы с API сайта HeadHunter. Получения данных о вакансиях"""

    def __init__(self):
        """
        Конструктор класса  HeadHunterVacancies
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = None
        self.vacancies = []

    def load_vacancies(self, employer_ids) -> list:
        """Метод для загрузки вакансий по ID работодателя"""

        for employer_id in employer_ids:

            self.params = {'page': 0, 'area': 113, 'currency': 'RUR',
                           'per_page': 100, 'employer_id': employer_id}

            while self.params.get('page') != 10:
                response = requests.get(self.url, headers=self.headers,
                                        params=self.params)
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
        return self.vacancies
