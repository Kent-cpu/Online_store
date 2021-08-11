import math
import time

import werkzeug.security

from Backend.ConstantStorage import *
from Backend.SQLiteErrorCods import *
import sqlite3
from flask import g


class Database:

    def __init__(self, database_path):
        self.db_path = database_path

    def connect_db(self):
        connect = sqlite3.connect(self.db_path)
        return connect

    def get_db(self):
        if not hasattr(g, "link_db"):
            g.link_db = self.connect_db()
        return g.link_db

    def close_db(self):
        if hasattr(g, "link_db"):
            g.link_db.close()

    def get_user_by_nickname(self, user_nickname):
        try:
            g.link_db.commit()
            cursor = g.link_db.cursor()
            cursor.execute("SELECT * FROM Users WHERE nickname = ? LIMIT 1", (user_nickname,))
            res = cursor.fetchall()
            print(res)
            if not res:
                return False
            return res[0]
        except sqlite3.Error as error:
            return False

    def get_user_by_email(self, user_email):
        try:
            cursor = g.link_db.cursor()
            cursor.execute("SELECT * FROM Users WHERE email = ? LIMIT 1", (user_email,))
            res = cursor.fetchall()
            if not res:
                return False
            return res[0]
        except sqlite3.Error as error:
            return False

    def check_for_uniqueness(self, key, value):
        try:
            cursor = g.link_db.cursor()
            if key == NICKNAME:
                count = """SELECT * FROM Users WHERE nickname LIKE ?;"""
            else:
                count = """SELECT * FROM Users WHERE email LIKE ?;"""
            cursor.execute(count, (value,))
            count = len(cursor.fetchall())
            if count > 0:
                return [UNIQUE_FIELD_ERROR_CODE, f"{key};"]
            else:
                return [OK_CODE, get_code_info(OK_CODE)]
        except Exception:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    def add_data_to_table(self, data):
        try:
            cursor = g.link_db.cursor()
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
                cursor.execute(sqlite_insert_with_param, (data[0], data[1], data[2], math.floor(time.time()),))
                g.link_db.commit()
            return [OK_CODE, get_code_info(OK_CODE)]
        except sqlite3.IntegrityError as error:
            if str(error) == "UNIQUE constraint failed: Users.email":
                return [UNIQUE_FIELD_ERROR_CODE, f"{EMAIL}"]
            elif str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_CODE, f"{NICKNAME}"]
            else:
                return [ERROR_CODE, get_code_info(ERROR_CODE)]
        except BaseException:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    def check_user_password(self, user_id, password):
        user = self.get_user_by_email(user_id)
        if user:
            if werkzeug.security.check_password_hash(user[3], password):
                return user
            else:
                return False
        else:
            return False

    def create_db(self):
        database_connection = sqlite3.connect(self.db_path)
        file = open(str((Path(Path.cwd()) / "Database" / "SQLite_db.sql").resolve()))
        database_connection.executescript(file.read())
        database_connection.commit()
        database_connection.close()
