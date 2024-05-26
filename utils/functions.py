import json
import os
import psycopg2
from config import ROOT_DIR, config


# conn = psycopg2.connect(
#     host='localhost',  # 127.0.0.1
#     database='HeadHunter',  # dbname
#     user='postgres',
#     password='sql'
# )
# try:
#     with conn:
#         with conn.cursor() as cur:
#             pass
#
#
# finally:
#     conn.close()

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


def create_database(database_name: str, params: dict) -> None:
    """Создание БД и таблиц, для сохранения данных о работодателе и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{database_name}'
            AND pid <> pg_backend_pid()""")
    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE  {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                employers_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                alternate_url TEXT,
                vacancies_url TEXT,
                industries TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employers_id) NOT NULL,
                name VARCHAR(100),
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(3),
                requirement TEXT,
                responsibility TEXT,
                employment VARCHAR(100),
                address TEXT,
                publication_date VARCHAR(20),
                link_to_vacancy TEXT
                )

            """)

        conn.commit()

    finally:
        conn.close()


# def save_data_to_database(data: list[dict], database_name: str,
#                           params: dict) -> None:
#     """Сохранение данных о работодателе и вакансиях в БД"""
#     pass


param = config()

create_database('test', param)
