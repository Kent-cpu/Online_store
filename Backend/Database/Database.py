import sqlite3
# from Backend.SQLiteErrorCods impfrSQLiteErrorCods


from SQLiteErrorCods import *


class Database:

    def __init__(self, database_name):
        self.sqlite_insert_with_param = """INSERT INTO Users
                                                              (nickname, email, password)
                                                              VALUES
                                                              (?, ?, ?);"""
        self.database_name = "Users_database.db"
        # database_users_table = '''CREATE TABLE Users (
        #                                        id INTEGER PRIMARY KEY,
        #                                        nickname text NOT NULL UNIQUE,
        #                                        email text NOT NULL UNIQUE,
        #                                        password text NOT NULL);'''
        # self.database.add_table(database_users_table)

    def add_table(self, sqlite_create_table_query):
        try:
            database_connection = sqlite3.connect(
                "Backend/Database/" + self.database_name)
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
            database_connection = sqlite3.connect(
                "Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            count_of_nickname = """SELECT * FROM Users WHERE nickname LIKE ?;"""
            cursor.execute(count_of_nickname, (data[0],))
            count_of_nickname = len(cursor.fetchall())
            count_of_email = """SELECT * FROM Users WHERE email LIKE ?;"""
            cursor.execute(count_of_email, (data[1],))
            count_of_email = len(cursor.fetchall())
            print(count_of_nickname)
            print(count_of_email)
            if count_of_nickname > 0 and count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_COD, "nickname;email;"]
            elif count_of_nickname > 0:
                return [UNIQUE_FIELD_ERROR_COD, "nickname;"]
            elif count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_COD, "email;"]
            else:
                cursor.execute(self.sqlite_insert_with_param, data)
                database_connection.commit()
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()
            return [OK_COD, "OK"]
        except sqlite3.IntegrityError as error:
            print(error)
            if str(error) == "UNIQUE constraint failed: Users.email":
                return [UNIQUE_FIELD_ERROR_COD, "email"]
            elif str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_COD, "nickname"]
            else:
                return ERROR_COD
        except sqlite3.Error as error:
            print(error)
        return ERROR_COD

    def get_all_data(self):
        try:
            database_connection = sqlite3.connect(
                "Backend/Database/" + self.database_name)
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
            database_connection = sqlite3.connect(
                "Backend/Database/" + self.database_name)
            cursor = database_connection.cursor()
            cursor.execute("DELETE FROM Users;")
            database_connection.commit()
        except sqlite3.OperationalError as error:
            print(error)
            return ERROR_COD
        except sqlite3.Error as error:
            print(error)
            return ERROR_COD
