from configparser import ConfigParser
import os

ROOT_DIR = os.path.dirname(__file__)
path_to_ini = os.path.join(ROOT_DIR, 'database.ini')


def config(filename=path_to_ini, section="postgresql") -> dict:
    # create a parser - создать парсер
    parser = ConfigParser()
    # read config file - прочитать файл конфигурации
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section,
                                                               filename))
    return db


