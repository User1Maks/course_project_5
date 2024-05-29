import psycopg2
from config import config


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, dbname: str, params: dict):
        self.dbname = dbname
        self.params = params
        self._create_database()
        self.conn = psycopg2.connect(dbname=dbname, **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

        self._create_tables()

    def conn_close(self):
        """Метод для закрытия курсора"""
        self.conn.close()
        print('База данных и таблицы успешно созданы')

    def _create_database(self) -> None:
        """Создание БД"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            with cur:
                cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{self.dbname}'
                        AND pid <> pg_backend_pid()""")
                cur.execute(f'DROP DATABASE IF EXISTS {self.dbname}')
                cur.execute(f"""CREATE DATABASE  {self.dbname}
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

        self.conn = self.conn
        self.cur = self.conn.cursor()
        with self.cur:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                description TEXT,
                alternate_url TEXT,
                vacancies_url TEXT,
                industries TEXT
                );
            """)

            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id) NOT NULL,
                vacancy_name VARCHAR(100),
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(3),
                requirement TEXT,
                responsibility TEXT,
                employment VARCHAR(100),
                address TEXT,
                publication_date DATE,
                link_to_vacancy TEXT
                )
            """)

    def insert_data(self, employers: list, vacancies: list) -> None:
        """Заполнение таблиц данными"""

        self.conn = self.conn
        self.cur = self.conn.cursor()

        for employer in employers:
            with self.conn:
                self.cur.execute(f"""
                INSERT INTO employers(employer_id, employer_name, 
                description,  alternate_url, vacancies_url, industries
                )
                VALUES (%s, %s, %s, %s, %s, %s)""",
                                 employer.to_list())

        for vacancy in vacancies:
            try:
                with self.conn:
                    self.cur.execute(f"""
                    INSERT INTO vacancies(vacancy_id, employer_id, 
                    vacancy_name, salary_from, salary_to, currency, 
                    requirement, responsibility, employment, address, 
                    publication_date, link_to_vacancy) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s)""",
                                     vacancy.to_list())
            except psycopg2.errors.UniqueViolation:
                print(f'Вакансии с повторяющимися ID. Данные вакансии'
                      f'не будут записаны в БД:{vacancy}')

    def get_companies_and_vacancies_count(self):
        """Метод для получения списка всех компаний и количество вакансий у
        каждой компании"""

        with self.conn:
            self.cur.execute(f"""SELECT employer_name, COUNT(vacancy_id) 
            FROM employers
            INNER JOIN vacancies USING(employer_id)
            GROUP BY employer_name;""")
            return self.cur.fetchall()

    def get_all_vacancies(self):
        """Метод для получает списка всех вакансий с указанием названия
        компании, названия вакансии и зарплаты и ссылки на вакансию."""

        with self.conn:
            self.cur.execute(f""" SELECT employer_name, vacancy_name, 
            salary_from, salary_to, currency, vacancies_url
            FROM vacancies
            INNER JOIN employers USING(employer_id);""")
            return self.cur.fetchall()

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""
        with self.conn:
            self.cur.execute(f"""SELECT (AVG(salary_from) + AVG(salary_to)) / 2 
            AS average_salary
            FROM vacancies
            WHERE salary_from > 0 AND salary_to > 0;""")
            return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Метод для получения списка всех вакансий, у которых зарплата выше
         средней по всем вакансиям"""
        with self.conn:
            self.cur.execute(f"""SELECT vacancy_name, salary_from, salary_to
            FROM vacancies
            WHERE (salary_from + salary_to)/2 >
            (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS average_salary
            FROM vacancies
            WHERE salary_from > 0 AND salary_to > 0);
            """)
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Метод для получения списка всех вакансий, в названии которых
        содержатся переданные в метод слова, например python
        :param keyword: слово для поиска вакансий
        """
        self.conn = self.conn
        self.cur = self.conn.cursor()

        with self.conn:
            self.cur.execute(f"""SELECT employer_name, vacancy_name
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE vacancy_name LIKE '%{keyword}%'
            OR requirement LIKE '%{keyword}%'
            OR responsibility LIKE '%{keyword}%'
            """)
            return self.cur.fetchall()


if __name__ == '__main__':
    param = config()
    db_manager = DBManager('cw5', param)
    print(db_manager.get_vacancies_with_keyword('python'))
