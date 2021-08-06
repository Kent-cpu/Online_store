from typing import Final

SERVER_HOST = "192.168.100.20"
SERVER_PORT = "5005"
DATABASE: Final = "Backend/Database/Users_database.db"
REQUEST_TYPE: Final = "type"
OK_CODE_ANSWER: Final = "OK_CODE"
ERROR_CODE_ANSWER: Final = "ERROR_CODE"
CODE_ANSWER: Final = "code"
TEXT_ANSWER: Final = "text"
DATA_FROM_SERVER: Final = "data"
EMAIL: Final = "email"
NICKNAME: Final = "nickname"
PASSWORD: Final = "password"
REGISTRATION: Final = "registration"
SHUTDOWN: Final = "shutdown"
KEY: Final = "key"

sqlite_insert_with_param ="""INSERT INTO Users
                                        (nickname, email, password)
                                                VALUES
                                        (?, ?, ?);"""
