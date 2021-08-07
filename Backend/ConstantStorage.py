from typing import Final

SERVER_HOST = "192.168.100.20"  # Хост сервера
SERVER_PORT = "5005"  # Порт сервера
DATABASE_PATH: Final = "Backend/Database/Users_database.db"  # Путь до базы данных
REQUEST_TYPE: Final = "type"  # Ключ к словарю для типа переданных данных
OK_CODE_ANSWER: Final = "OK_CODE"  # Значение по ключу REQUEST_TYPE
ERROR_CODE_ANSWER: Final = "ERROR_CODE"  # Значение по ключу REQUEST_TYPE
CODE_ANSWER: Final = "code"  # Ключ к словарю для данных типа код
TEXT_ANSWER: Final = "text"  # Ключ к словарю для данных типа текст
VALUE_ANSWER: Final = "text"  # Ключ к словарю для данных
DATA_FROM_SERVER: Final = "data"  # Ключ к словарю для типа переданных данных(JSON, все переданные данные)
EMAIL: Final = "email"  # Ключ к словарю для данных типа email + константа
NICKNAME: Final = "nickname"  # Ключ к словарю для данных типа nickname + константа
PASSWORD: Final = "password"  # Ключ к словарю для данных типа password + константа
REGISTRATION: Final = "registration"  # Ключ к словарю для данных типа текст
SHUTDOWN: Final = "shutdown"  # константа

sqlite_insert_with_param ="""INSERT INTO Users
                                        (nickname, email, password)
                                                VALUES
                                        (?, ?, ?);"""  # Формат ввода в базу данных
