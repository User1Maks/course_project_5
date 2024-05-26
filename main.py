from src.class_employers import Employers
from src.class_vacancy import Vacancy
from src.head_hunter import HeadHunterEmployers, HeadHunterVacancies
from src.class_dbmanager import DBManager
from utils.functions import default_employers_id
from config import config


def main():
    # # Подключение к API employers
    # hh_api_employers = HeadHunterEmployers()
    #
    # # Получения списка API по умолчанию
    # list_employers_api = default_employers_id()
    #
    # # Получения списка работодателей
    # list_employers = Employers.convert_to_employer(
    #     hh_api_employers.load_employers(list_employers_api))
    #
    # # Подключение к API vacancies
    # hh_api_vacancies = HeadHunterVacancies()
    #
    # # Получение списка вакансий выбранных компаний
    # list_vacancies = Vacancy.convert_to_vacancy(
    #     hh_api_vacancies.load_vacancies(list_employers_api))

    # Создание БД
    params = config()
    user_input_db = input('Введите название БД: ')
    db_manager = DBManager(user_input_db, params)
    db_manager


if __name__ == '__main__':
    main()
