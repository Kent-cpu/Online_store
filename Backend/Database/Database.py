import sys
sys.path.append('..')
from Backend.ConstantStorage import *
from Backend.SQLiteErrorCods import *
import sqlite3


class Database:

    def __init__(self):
        self.sqlite_insert_with_param = """INSERT INTO Users
                                                              (nickname, email, password)
                                                              VALUES
                                                              (?, ?, ?);"""
        # database_users_table = '''CREATE TABLE Users (
        #                                        id INTEGER PRIMARY KEY,
        #                                        nickname text NOT NULL UNIQUE,
        #                                        email text NOT NULL UNIQUE,
        #                                        password text NOT NULL);'''
        # self.database.add_table(database_users_table)

    def connect_db(self):
        connect = sqlite3.connect(DATABASE_PATH)
        # connect.row_factory = sqlite3.Row
        return connect

    def add_table(self, sqlite_create_table_query):
        try:
            database_connection = self.connect_db()
            cursor = database_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            database_connection.commit()
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()
        except sqlite3.OperationalError as error:
            return ERROR_CODE
        except sqlite3.Error:
            return ERROR_CODE
        return OK_CODE

    def check_for_uniqueness(self, key, value):
        try:
            database_connection = self.connect_db()
            cursor = database_connection.cursor()
            if key == NICKNAME:
                count = """SELECT * FROM Users WHERE nickname LIKE ?;"""
            else:
                count = """SELECT * FROM Users WHERE email LIKE ?;"""
            cursor.execute(count, (value,))
            count = len(cursor.fetchall())
            if database_connection:
                database_connection.close()
            if count > 0:
                return [UNIQUE_FIELD_ERROR_CODE, f"{key};"]
            else:
                return [OK_CODE, get_code_info(OK_CODE)]
        except Exception:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    def add_data_to_table(self, data):
        try:
            database_connection = self.connect_db()
            cursor = database_connection.cursor()
            count_of_nickname = """SELECT * FROM Users WHERE nickname LIKE ?;"""
            cursor.execute(count_of_nickname, (data[0],))
            count_of_nickname = len(cursor.fetchall())
            count_of_email = """SELECT * FROM Users WHERE email LIKE ?;"""
            cursor.execute(count_of_email, (data[1],))
            count_of_email = len(cursor.fetchall())
            if count_of_nickname > 0 and count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_CODE, f"{NICKNAME};{EMAIL}"]
            elif count_of_nickname > 0:
                return [UNIQUE_FIELD_ERROR_CODE, f"{NICKNAME};"]
            elif count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_CODE, f"{EMAIL};"]
            else:
                cursor.execute(sqlite_insert_with_param, data)
                database_connection.commit()
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()
            return [OK_CODE, get_code_info(OK_CODE)]
        except sqlite3.IntegrityError as error:
            if str(error) == "UNIQUE constraint failed: Users.email":
                return [UNIQUE_FIELD_ERROR_CODE, f"{EMAIL}"]
            elif str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_CODE, f"{NICKNAME}"]
            else:
                return [ERROR_CODE, get_code_info(ERROR_CODE)]

    def get_all_data(self):
        try:
            database_connection = self.connect_db()
            cursor = database_connection.cursor()
            sqlite_select_query = """SELECT * from Users"""
            cursor.execute(sqlite_select_query)
            return cursor.fetchall()
        except sqlite3.OperationalError:
            return ERROR_CODE
        except sqlite3.Error:
            return ERROR_CODE

    def clear_table(self, name):
        try:
            database_connection = self.connect_db()
            cursor = database_connection.cursor()
            cursor.execute("DELETE FROM ?;", (name,))
            database_connection.commit()
        except sqlite3.OperationalError:
            return ERROR_CODE
        except sqlite3.Error:
            return ERROR_CODE
