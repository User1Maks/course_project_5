from datetime import datetime

from src.clasess_abstract import ABCVacancy


class Vacancy(ABCVacancy):

    def __init__(self, vacancy_id: int, employer_id: int, name: str,
                 salary_from: int, salary_to: int, currency: str,
                 requirement: str, responsibility: str, employment: str,
                 address: str, publication_date: str, link_to_vacancy: str):
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
        self.publication_date = self._date_formatting(publication_date)
        self.link_to_vacancy = link_to_vacancy

    @classmethod
    def convert_to_vacancy(cls, list_vacancies: list) -> list:
        """
        Класс метод для создания экземпляров класса Vacancy из словарей формата
        Response, получаемых с API hh.ru
        """
        returned_list = []
        for vacancy in list_vacancies:
            vacancy_id = vacancy['id']
            employer_id = vacancy.get('employer')['id']
            name = vacancy.get('name')
            salary_from = (vacancy.get('salary') or {}).get('from')
            salary_to = (vacancy.get('salary') or {}).get('to')
            currency = (vacancy.get('salary') or {}).get('currency')
            requirement = vacancy.get('snippet').get('requirement')
            responsibility = vacancy.get('snippet').get('responsibility')
            employment = (vacancy.get('employment').get('name'))
            address = (vacancy.get('address') or {}).get('raw')
            publication_date = (vacancy.get('published_at', {}) or 'Не найдено')
            link_to_vacancy = (vacancy.get('alternate_url'))

            vacancy_object = cls(vacancy_id, employer_id, name, salary_from,
                                 salary_to, currency, requirement,
                                 responsibility, employment, address,
                                 publication_date, link_to_vacancy)

            returned_list.append(vacancy_object)
        return returned_list

    @staticmethod
    def check_data_str(value) -> str:
        """Валидатор для проверки строковых значений"""
        if value:
            return value
        return 'Не найдено'

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
                self.responsibility, self.employment, self.address,
                self.publication_date, self.link_to_vacancy]

    @staticmethod
    def _date_formatting(data):
        """
        Метод для конвертации даты из формата "2024-05-17T18:00:26+0300"
        в "17.05.2024 18:00"
        :return: datetime
        """

        date_format = datetime.fromisoformat(data)
        date_format = date_format.strftime('%d.%m.%Y %H:%M')
        return date_format

    def __print_salary(self) -> str:
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
            return 'Не найдено'

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

    def __eq__(self, other):  # – для равенства ==
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from == other.salary_from
        return self.salary_from == other

    def __ne__(self, other):  # – для неравенства !=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from != other.salary_from
        return self.salary_from != other

    def __lt__(self, other):  # – для оператора меньше <
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from < other.salary_from
        return self.salary_from < other

    def __le__(self, other):  # – для оператора меньше или равно <=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from <= other.salary_from
        return self.salary_from <= other

    def __gt__(self, other):  # – для оператора больше >
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from > other.salary_from
        return self.salary_from > other

    def __ge__(self, other):  # – для оператора больше или равно >=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from >= other.salary_from
        return self.salary_from >= other

    def __repr__(self) -> str:
        """ Метод для отладки класса Vacancy"""
        return (
            f'\n\n{self.__class__.__name__}:\n'
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
            f'Ссылка на вакансию: {self.link_to_vacancy}'
        )
