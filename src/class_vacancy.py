from datetime import datetime


class Vacancy:

    def __init__(self, vacancy_id: int, employer_id: int, name: str,
                 salary_from: int, salary_to: int, requirement: str,
                 responsibility: str, employment: str, address: str,
                 currency: str, publication_date: str, link_to_vacancy: str):
        """
        Конструктор класса Vacancies.
        :param vacancy_id: ID вакансии.
        :param employer_id: ID компании.
        :param name: Должность.
        :param salary_from: Минимальная зарплата.
        :param salary_to: Максимальная зарплата.
        :param currency: Валюта.
        :param requirement: Требования к вакансии.
        :param responsibility: Описание обязанностей.
        :param employment: Занятость.
        :param address: Адрес.
        :param publication_date: Дата публикации вакансии.
        :param link_to_vacancy: Ссылка на вакансию.
        """

        self.vacancy_id = vacancy_id
        self.employer_id = employer_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility
        self.employment = employment
        self.address = address
        self.publication_date = publication_date
        self.link_to_vacancy = link_to_vacancy

    @classmethod
    def convert_to_vacancy(cls, list_vacancies):
        """
        Класс метод для создания экземпляров класса из словарей формата Response,
        получаемых с API hh.ru
        """
        returned_list = []
        for vacancy in list_vacancies:
            vacancy_id = vacancy['id']
            name = Vacancy.check_data_str(vacancy['name'])
            salary_from = Vacancy.check_data_int(
                vacancy.get('salary').get('from'))
            salary_to = Vacancy.check_data_int(vacancy.get('salary').get('to'))
            currency = Vacancy.check_data_str(
                vacancy.get('salary').get('currency'))
            employer_id = Vacancy.check_data_int(
                vacancy.get('employer').get('id'))
            requirement = Vacancy.check_data_str(
                vacancy.get('snippet').get('requirement'))
            responsibility = Vacancy.check_data_str(
                vacancy.get('snippet').get('responsibility'))
            publication_date = Vacancy._date_formatting(
                (vacancy.get('published_at'), {}) or None)
            employment = Vacancy.check_data_str(
                vacancy.get('employment').get('name'))
            address = Vacancy.check_data_str(vacancy.get('address').get('raw'))
            link_to_vacancy = Vacancy.check_data_str(
                vacancy.get('alternate_url'))

            vacancy_object = cls(vacancy_id, name, salary_from, salary_to,
                                 currency, employer_id, requirement,
                                 responsibility, publication_date, employment,
                                 address, link_to_vacancy)

            returned_list.append(vacancy_object)
            return vacancy_object

    @staticmethod
    def check_data_str(value) -> str or None:
        """Валидатор для проверки строковых значений"""
        if value:
            return value
        return None

    @staticmethod
    def check_data_int(value) -> int:
        """Валидатор для целых чисел"""
        if value:
            return value
        return 0

    def to_list(self) -> list:
        """
         Метод для возвращения полного списка атрибутов экземпляра
         класса Vacancy
        """

        return [self.vacancy_id, self.employer_id, self.name, self.salary_from,
                self.salary_to, self.currency, self.requirement,
                self.responsibility, self.publication_date, self.employment,
                self.address, self.link_to_vacancy]

    @staticmethod
    def _date_formatting(date) -> datetime.strftime:
        """
        Метод для конвертации даты из формата "2024-05-17T18:00:26+0300"
        в "17.05.2024 18:00"
        :return: datetime
        """
        date_format = datetime.fromisoformat(date)
        date_format = date_format.strftime('%d.%m.%Y %H:%M')
        return date_format

    def __print_salary(self) -> str or None:
        """
        Метод для корректного выведения заработной платы(ЗП) пользователю.
        Если ЗП указана в объявлении с диапазоном, тогда
        выводится диапазон ЗП. Если одного из параметров нет, тогда выводится
        тот, который есть. В случае отсутствия информации выводится 'Не указана'
        :return: Строку содержащую информацию о зарплате.
        """
        if self.salary_from and self.salary_to:
            return f'{self.salary_from} - {self.salary_to} {self.currency}'
        elif {self.salary_from} and not self.salary_to:
            return f'{self.salary_from} {self.currency}'
        elif not {self.salary_from} and {self.salary_to}:
            return f'{self.salary_to} {self.currency}'
        else:
            return None

    def __str__(self) -> str:
        """ Метод для вывода информации класса Vacancy"""
        return (
            f'\nДолжность: {self.name}\n'
            f'Зарплата: {self.__print_salary()}\n'
            f'Требования к вакансии: {self.requirement}\n'
            f'Описание обязанностей: {self.responsibility}\n'
            f'Занятость: {self.employment}\n'
            f'Адрес: {self.address}\n'
            f'Дата публикации вакансии: {self.publication_date}\n'
            f'Ссылка на вакансию: {self.link_to_vacancy}\n'
        )

    def __repr__(self) -> str:
        """ Метод для отладки класса Vacancy"""
        return (
            f'\n{self.__class__.__name__}:\n'
            f'ID вакансии: {self.vacancy_id}\n'
            f'ID компании: {self.employer_id}\n'
            f'Должность: {self.name}\n'
            f'Зарплата: {self.__print_salary()}\n'
            f'Валюта: {self.currency}\n'
            f'Требования к вакансии: {self.requirement}\n'
            f'Описание обязанностей: {self.responsibility}\n'
            f'Занятость: {self.employment}\n'
            f'Адрес: {self.address}\n'
            f'Дата публикации вакансии: {self.publication_date}\n'
            f'Ссылка на вакансию: {self.link_to_vacancy}\n'
        )
