from src.class_employers import Employers
from src.class_vacancy import Vacancy
from src.head_hunter import HeadHunterEmployers, HeadHunterVacancies
from src.class_dbmanager import CreateDBManager
from utils.functions import default_employers_id, working_with_a_database


def main():
    # Подключение к API employers
    hh_api_employers = HeadHunterEmployers()

    # Получения списка API по умолчанию
    list_employers_api = default_employers_id()

    # Получения списка работодателей
    list_employers = Employers.convert_to_employer(
        hh_api_employers.load_employers(list_employers_api))

    # Подключение к API vacancies
    hh_api_vacancies = HeadHunterVacancies()

    # Получение списка вакансий выбранных компаний
    list_vacancies = Vacancy.convert_to_vacancy(
        hh_api_vacancies.load_vacancies(list_employers_api))

    # Создание БД по умолчанию cw5 и таблиц employers и vacancies
    db_manager = CreateDBManager()

    # Заполнение таблиц данными
    db_manager.insert_data(list_employers, list_vacancies)

    # Закрытие курсора
    db_manager.conn_close()

    # Работа с БД
    working_with_a_database()


if __name__ == '__main__':
    main()
