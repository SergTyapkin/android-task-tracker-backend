import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:
    initialized = False

    def __init__(self, config):
        self.config = config
        try:
            self.db = psycopg2.connect(
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"],
                dbname=config["database"]
            )
            self.db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.OperationalError as err:
            print(err)
            if err.args[0] == 2003:
                print('Неверный формат host')
            if err.args[0] == 1045:
                print('Неверное имя пользователя или пароль')
            if err.args[0] == 1049:
                print('Не найдена база данных')
                self.db = psycopg2.connect(
                    user=config["user"],
                    password=config["password"],
                    host=config["host"],
                    port=config["port"],
                )
                self.db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                print("Создание базы даных...")
                try:
                    self.cursor = self.db.cursor()
                    self.cursor.execute("CREATE DATABASE " + config["database"])
                    print("База данных создана. Перезапустите сервер.")
                except psycopg2.Error as error:
                    if error.pgcode == "42P04":
                        print("База данных уже существует")
                    else:
                        print("Ошибка при создании базы данных:")
                        print(error)
                    return
                finally:
                    self.cursor.close()
            exit()
            return

        try:
            with open('database/init.sql') as initFile:
                initText = initFile.read()
            cur = self.db.cursor()
            cur.execute(initText)
            cur.close()
            print("Таблицы созданы")
        except psycopg2.Error as error:
            print("Ошибка при создании таблиц:")
            print(error)
            return

        self.initialized = True

    def execute(self, request: str, values: list[any] = [], dictionary: bool = False):
        try:
            cur = self.db.cursor()
            cur.execute(request, values)
        except psycopg2.ProgrammingError as err:
            if err.args[0] == 1146:
                print('Таблицы не существует')
            if err.args[0] == 1064:
                print('Неверный синтаксис запроса')
            print(err)
            return err
        except psycopg2.OperationalError as err:
            if err.args[0] == 1054:
                print('Столбец не найден')
            print(err)
            return err

        try:
            print(request)
            response = cur.fetchall().copy()
            print(response)
            if dictionary:
                if len(response) == 0:
                    return {}
                response = dict(map(lambda key, val: (key[0], val), cur.description, response[0]))
                cur.close()
                return response
            columns = [desc[0] for desc in cur.description]
        except psycopg2.ProgrammingError as err:
            print(err)
            if dictionary:
                return {}
            return [], []

        cur.close()
        return response, columns
