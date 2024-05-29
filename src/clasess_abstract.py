from abc import ABC, abstractmethod


class ApiEmployers(ABC):
    """
     Абстрактный класс для работы с API сервиса с вакансиями. Является
     родительским классом для класса HeadHunterEmployers.
     """

    @abstractmethod
    def load_employers(self, list_ids_employers) -> list:
        """Метод для загрузки информации о работодателе по ID"""
        pass


class ApiVacancies(ABC):
    """
     Абстрактный класс для работы с API сервиса с вакансиями. Является
     родительским классом для класса HeadHunterVacancies.
    """

    @abstractmethod
    def load_vacancies(self, employer_ids) -> list:
        """Метод для загрузки вакансий по ID работодателя"""
        pass


class ABCEmployers(ABC):
    """
    Абстрактный класс для работы с данными о работодателях загружаемыми с
    сайта hh.ru. Является родительским классом для класса Employers.
    """

    @abstractmethod
    def __init__(self, employers_id: int, name: str, description: str,
                 alternate_url: str, vacancies_url: str, industries: str):
        pass

    @classmethod
    @abstractmethod
    def convert_to_employer(cls, list_employers: list) -> list:
        """
        Класс метод для создания экземпляров класса Employers из словарей
        формата Response, получаемых с API hh.ru
        """
        pass

    @abstractmethod
    def to_list(self) -> list:
        """
        Метод для возвращения полного списка атрибутов экземпляра
        класса Employers
        """
        pass


class ABCVacancy(ABC):
    """
    Абстрактный класс для работы с вакансиями загружаемыми с сайта hh.ru.
    Является родительским классом для класса Vacancy
    """

    @abstractmethod
    def __init__(self, vacancy_id: int, employer_id: int, name: str,
                 salary_from: int, salary_to: int, currency: str,
                 requirement: str, responsibility: str, employment: str,
                 address: str, publication_date: str, link_to_vacancy: str):
        pass

    @classmethod
    @abstractmethod
    def convert_to_vacancy(cls, list_vacancies: list) -> list:
        """
        Класс метод для создания экземпляров класса Vacancy из словарей формата
        Response, получаемых с API hh.ru
        """
        pass

    @abstractmethod
    def to_list(self) -> list:
        """
         Метод для возвращения полного списка атрибутов экземпляра
         класса Vacancy
        """
        pass

    @staticmethod
    @abstractmethod
    def _date_formatting(data):
        """
        Метод для конвертации даты из формата "2024-05-17T18:00:26+0300"
        в "17.05.2024 18:00"
        :return: datetime
        """
        pass


class ABCDBManager(ABC):
    """
    Абстрактный класс для создания БД, таблиц и их заполнение данными о
    вакансиях с сайта hh.ru. Является родительским для класса CreateDBManager.
    """

    @abstractmethod
    def conn_close(self):
        """Метод для закрытия курсора"""
        pass

    @abstractmethod
    def _create_database(self) -> None:
        """Создание БД"""
        pass

    @abstractmethod
    def _create_tables(self):
        """Создание таблиц employers и vacancies"""
        pass

    @abstractmethod
    def insert_data(self, employers: list, vacancies: list) -> None:
        """Заполнение таблиц employers и vacancies данными"""
        pass


class WorkDBManager(ABC):
    """
    Абстрактный класс для работы с БД. Является родительским для класса
    DBManager.
    """

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Метод для получения списка всех компаний и количество вакансий у
        каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Метод для получает списка всех вакансий с указанием названия
        компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """Метод для получения списка всех вакансий, у которых зарплата выше
         средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
        """
        Метод для получения списка всех вакансий, в названии которых
        содержатся переданные в метод слова, например python
        :param keyword: слово для поиска вакансий
        """
        pass
