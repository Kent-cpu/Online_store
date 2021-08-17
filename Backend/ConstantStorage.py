from typing import Final
from pathlib import Path

SERVER_HOST = "192.168.100.20"  # Хост сервера
SERVER_PORT = "5005"  # Порт сервера
DATABASE_PATH: Final = str((Path(Path.cwd())/"Database"/"Users_database.db").resolve())  # Путь до базы данных
REQUEST_TYPE: Final = "type"  # Ключ к словарю для типа переданных данных
CHECK_DATA_FOR_UNIQUENESS: Final = "check_data_for_uniqueness"
REDIRECT: Final = "redirect"  # Тип переданных данных
REGISTRATION: Final = "registration"  # Тип переданных данных
AUTHORIZATION: Final = "authorization"  # Тип переданных данных
USER_INFO: Final = "user_info"  # Тип переданных данных
OK_CODE_ANSWER: Final = "OK_CODE"  # Тип переданных данных
ERROR_CODE_ANSWER: Final = "ERROR_CODE"  # Тип переданных данных
CODE_ANSWER: Final = "code"  # Ключ к словарю для данных типа код
TEXT_ANSWER: Final = "text"  # Ключ к словарю для данных типа текст
VALUE_ANSWER: Final = "text"  # Ключ к словарю для данных
DATA_FROM_SERVER: Final = "data"  # Ключ к словарю для типа переданных данных(JSON, все переданные данные)
EMAIL: Final = "email"  # Ключ к словарю для данных типа email + константа
NICKNAME: Final = "nickname"  # Ключ к словарю для данных типа nickname + константа
PASSWORD: Final = "password"  # Ключ к словарю для данных типа password + константа
AVATAR: Final = "avatar"  # Ключ к словарю для данных аватара
ACCOUNT_CREATION_TIME: Final = "account_creation_time"  # Ключ к словарю для данных времени создания аккаунта
IS_LOGIN: Final = "is_login"  # Ключ к словарю для данных об авторизации пользователя
FILE: Final = "file"  # Ключ к словарю для данных типа file
REQUESTED_DATA: Final = "requested_data"  # Запращиваемые данные
DATA: Final = "data"  # Переданные данные
REMEMBER_ME: Final = "remember_me"  # Ключ к словарю для данных поля запомнить_меня
SHUTDOWN: Final = "shutdown"  # константа
