import psycopg2


class HeadHunter:
    """
    Класс для работы с API сайта HeadHunter. Получения данных о работодателях
    и их вакансий.
    """

    def __init__(self):
        """
        Конструктор класса  HeadHunter
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'currency': 'RUR',
                       'per_page': 100}
        self.vacancies = []
