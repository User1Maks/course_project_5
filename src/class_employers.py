class Employers:

    def __init__(self, employers_id: int, name: str, description: str,
                 alternate_url: str, vacancies_url: str, industries: str):
        """

        :param employers_id: ID работодателя.
        :param name: Название компании.
        :param description: Описание компании.
        :param alternate_url: Ссылка на страницу компании на сайте hh.ru
        :param vacancies_url: Ссылка на вакансии компании.
        :param industries: Отрасли компании.
        """

        self.employers_id = employers_id
        self.name = name
        self.description = description
        self.alternate_url = alternate_url
        self.vacancies_url = vacancies_url
        self.industries = industries

    @classmethod
    def convert_to_employer(cls, list_employers: list) -> list:
        """
        Класс метод для создания экземпляров класса Employers из словарей
        формата Response, получаемых с API hh.ru
        """

        returned_list = []

        for employer in list_employers:
            employers_id = employer.get('id')
            name = employer.get('name')
            description = employer.get('description')
            alternate_url = employer.get('alternate_url')
            vacancies_url = employer.get('vacancies_url')
            try:
                industries = '; '.join(
                    [industry['name'] for industry in
                     employer.get('industries')])
            except TypeError:
                continue

            employer_object = cls(employers_id, name, description,
                                  alternate_url, vacancies_url, industries)

            returned_list.append(employer_object)

        return returned_list

    @staticmethod
    def check_data_str(value) -> str:
        """Валидатор для проверки строковых значений"""
        if value:
            return value
        return ''

    def to_list(self) -> list:
        """
        Метод для возвращения полного списка атрибутов экземпляра
        класса Employers
        """

        return [self.employers_id, self.name, self.description,
                self.alternate_url, self.vacancies_url, self.industries]

    def __str__(self) -> str:
        """ Метод для вывода информации класса Employers"""
        return (
            f'\nID работодателя: {self.employers_id}\n'
            f'Название компании: {self.name}\n'
            f'Описание компании: {self.description}\n'
            f'Ссылка на страницу компании на сайте hh.ru: '
            f'{self.alternate_url}\n'
            f'Ссылка на вакансии компании: {self.vacancies_url}\n'
            f'Отрасли компании: {self.industries}\n'
        )

    def __repr__(self) -> str:
        """ Метод для отладки класса Employers"""
        return (
            f'\n\n{self.__class__.__name__}:\n'
            f'ID работодателя: {self.employers_id}\n'
            f'Название компании: {self.name}\n'
            f'Описание компании: {self.description}\n'
            f'Ссылка на страницу компании на сайте hh.ru: '
            f'{self.alternate_url}\n'
            f'Ссылка на вакансии компании: {self.vacancies_url}\n'
            f'Отрасли компании: {self.industries}'
        )
