import sqlite3
from Backend.SQLiteErrorCods import *

#self.database_connection = sqlite3.connect("Backend/Database/" + self.database_name)
#self.cursor = self.database_connection.cursor()

class Database:

    def __init__(self, database_name, sqlite_insert_with_param):
        self.database_name = database_name
        self.sqlite_insert_with_param = sqlite_insert_with_param

    def add_table(self, sqlite_create_table_query):
        try:
            database_connection = sqlite3.connect("Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            database_connection.commit()
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()
        except sqlite3.OperationalError as error:
            return ERROR_COD
        except sqlite3.Error:
            return ERROR_COD
        return OK_COD

    def add_data_to_table(self, data):
        try:
            database_connection = sqlite3.connect("Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            cursor.execute(self.sqlite_insert_with_param, data)
            database_connection.commit()
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()
            return OK_COD
        except sqlite3.IntegrityError as error:
            if str(error) == "UNIQUE constraint failed: Users.email" and str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_COD, "email;nickname"]
            elif str(error) == "UNIQUE constraint failed: Users.email":
                return [UNIQUE_FIELD_ERROR_COD, "email"]
            elif str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_COD, "nickname"]
            else:
                return ERROR_COD
        except sqlite3.OperationalError as error:
            print(error)
            return ERROR_COD
        except sqlite3.Error as error:
            print(error)
        return ERROR_COD

    def get_all_data(self):
        try:
            database_connection = sqlite3.connect("Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            sqlite_select_query = """SELECT * from Users"""
            cursor.execute(sqlite_select_query)
            return cursor.fetchall()
        except sqlite3.OperationalError as error:
            print(error)
            return ERROR_COD
        except sqlite3.Error as error:
            print(error)
            return ERROR_COD

    def clear_table(self, name):
        try:
            database_connection = sqlite3.connect("Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            cursor.execute("DELETE FROM ?;", name)
            database_connection.commit()
        except sqlite3.OperationalError as error:
            print(error)
            return ERROR_COD
        except sqlite3.Error as error:
            print(error)
            return ERROR_COD
