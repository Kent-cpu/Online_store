from typing import Final
from pathlib import Path

SERVER_HOST = "192.168.100.20"  # Хост сервера
SERVER_PORT = "5005"  # Порт сервера
DATABASE_PATH: Final = str((Path(Path.cwd())/"Database"/"Users_database.db").resolve())  # Путь до базы данных
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
AVATAR: Final = "avatar"
ACCOUNT_CREATION_TIME: Final = "account_creation_time"
IS_LOGIN: Final = "is_login"
REGISTRATION: Final = "registration"  # Ключ к словарю для данных типа текст
AUTHORIZATION: Final = "authorization"
USER_INFO: Final = "user_info"
REQUESTED_DATA: Final = "requested_data"
REMEMBER_ME: Final = "remember_me"
SHUTDOWN: Final = "shutdown"  # константа
