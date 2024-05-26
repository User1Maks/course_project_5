import psycopg2
from config import config


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, dbname: str, params: dict):
        self.params = params
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self._create_database(dbname)
        self.cur = self.conn.cursor()

        self._create_tables()

    @classmethod
    def load_params(cls) -> dict:
        """Загрузка параметров подключения к базе данных"""
        params_config = config()
        return params_config

    def _create_database(self, database_name: str) -> None:
        """Создание БД"""

        conn = self.conn

        try:
            with conn:
                conn.autocommit = True
                cur = conn.cursor()
                with cur:
                    cur.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                        FROM pg_stat_activity
                        WHERE pg_stat_activity.datname = '{database_name}'
                            AND pid <> pg_backend_pid()""")
                    cur.execute(f'DROP DATABASE {database_name}')
                    cur.execute(f"""CREATE DATABASE  {database_name}
                    WITH
                    OWNER = postgres
                    TEMPLATE = template0
                    ENCODING = 'UTF8'
                    LOCALE_PROVIDER = 'libc'
                    CONNECTION LIMIT = -1
                    IS_TEMPLATE = False;""")

        finally:
            conn.close()

    def _create_tables(self):
        """Создание таблиц employers и vacancies"""

        conn = self.conn

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (                    
                    employers_id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    alternate_url TEXT,
                    vacancies_url TEXT,
                    industries TEXT
                    );
                """)

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (                    
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

    def insert_data(self, employers: list, vacancies: list) -> None:
        """Заполнение таблиц данными"""

        with self.conn:
            for employer in employers:
                self.cur.execute(f"""
                INSERT INTO employers(employers_id, employer_name, 
                description,  alternate_url, vacancies_url, industries
                )
                VALUES (%s, %s, %s, %s, %s, %s)""",
                                 employer.to_list())
        with self.conn:
            for vacancy in vacancies:
                self.cur.execute(f"""
                    INSERT INTO vacancies(vacancy_id, employer_id, vacancy_name,
                    salary_from, salary_to, currency, requirement,
                    responsibility, employment, address, publication_date,
                    link_to_vacancy) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)""",
                                 vacancy.to_list())

    def get_companies_and_vacancies_count(self):
        """Метод для получения списка всех компаний и количество вакансий у
        каждой компании"""

        with self.conn:
            self.cur.execute(f"""SELECT name, COUNT(vacancy_id) 
            FROM employers
            INNER JOIN vacancies USING(employer_id);""")

    def get_all_vacancies(self):
        """Метод для получает списка всех вакансий с указанием названия
        компании, названия вакансии и зарплаты и ссылки на вакансию."""

        with self.conn:
            self.cur.execute(f"""""")


if __name__ == '__main__':
    print(DBManager.load_params())
