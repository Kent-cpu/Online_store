import math
import time
import sys
import werkzeug.security
import sys
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

    @staticmethod
    def close_db():
        if hasattr(g, "link_db"):
            g.link_db.close()

    @staticmethod
    def get_user_by_nickname(user_nickname):
        try:
            cursor = g.link_db.cursor()
            cursor.execute("SELECT * FROM Users WHERE nickname = ? LIMIT 1", (user_nickname,))
            res = cursor.fetchall()[0]
            if not res:
                print("NO")
                return False
            return res
        except sqlite3.Error as error:
            print(error)
            return False

    @staticmethod
    def get_user_by_email(user_email):
        try:
            cursor = g.link_db.cursor()
            cursor.execute("SELECT * FROM Users WHERE email = ? LIMIT 1", (user_email,))
            res = cursor.fetchall()[0]
            if not res:
                return False
            return res
        except sqlite3.Error as error:
            return False

    @staticmethod
    def check_for_uniqueness(key_value_dict):
        try:
            answer = []
            for key in key_value_dict.keys():
                if key == NICKNAME:
                    count = """SELECT * FROM Users WHERE nickname LIKE ?;"""
                elif key == EMAIL:
                    count = """SELECT * FROM Users WHERE email LIKE ?;"""
                else:
                    continue
                cursor = g.link_db.cursor()
                cursor.execute(count, (key_value_dict[key],))
                count = len(cursor.fetchall())
                if count > 0:
                    answer.append(key)
            if len(answer) > 0:
                return [UNIQUE_FIELD_ERROR_CODE, answer]
            else:
                return [OK_CODE, get_code_info(OK_CODE)]
        except Exception:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    @staticmethod
    def add_user(data):
        try:
            cursor = g.link_db.cursor()
            count_of_nickname = """SELECT * FROM Users WHERE nickname LIKE ?;"""
            cursor.execute(count_of_nickname, (data[0],))
            count_of_nickname = len(cursor.fetchall())
            count_of_email = """SELECT * FROM Users WHERE email LIKE ?;"""
            cursor.execute(count_of_email, (data[1],))
            count_of_email = len(cursor.fetchall())
            if count_of_nickname > 0 and count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_CODE, [NICKNAME, EMAIL]]
            elif count_of_nickname > 0:
                return [UNIQUE_FIELD_ERROR_CODE, [NICKNAME]]
            elif count_of_email > 0:
                return [UNIQUE_FIELD_ERROR_CODE, [EMAIL]]
            else:
                cursor.execute("""INSERT INTO Users 
                (nickname, email, password, avatar, time)
                VALUES
                (?, ?, ?, NULL, ?);""", (data[0], data[1], data[2], math.floor(time.time()),))
                g.link_db.commit()
            return [OK_CODE, get_code_info(OK_CODE)]
        except sqlite3.IntegrityError as error:
            if str(error) == "UNIQUE constraint failed: Users.email":
                return [UNIQUE_FIELD_ERROR_CODE, [EMAIL]]
            elif str(error) == "UNIQUE constraint failed: Users.nickname":
                return [UNIQUE_FIELD_ERROR_CODE, [NICKNAME]]
            else:
                print(error)
                return [ERROR_CODE, get_code_info(ERROR_CODE)]
        except BaseException as error:
            print(error)
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    @staticmethod
    def update_user_avatar(img, user_nickname):
        if not img:
            return ERROR_CODE
        try:
            cursor = g.link_db.cursor()
            update_avatar = "UPDATE users SET avatar = ? WHERE nickname = ?"
            cursor.execute(update_avatar, (img, user_nickname))
            g.link_db.commit()
            return OK_CODE
        except sqlite3.Error as error:
            return ERROR_CODE
        except BaseException as error:
            print(error)
            return ERROR_CODE

    def check_user_password(self, user_id, password):
        answer = self.get_user_by_email(user_id)
        if answer:
            if werkzeug.security.check_password_hash(answer[3], password):
                return answer
            else:
                return False
        else:
            return False

    @staticmethod
    def get_post(url_post):
        try:
            cursor = g.link_db.cursor()
            cursor.execute("SELECT title, text FROM Posts WHERE URL = ?")
            res = cursor.fetchall()[0]
            if res:
                return res
        except sqlite3.Error:
            return False, False
        return False, False

    def create_db(self):
        database_connection = sqlite3.connect(self.db_path)
        file = open(str((Path(Path.cwd()) / "Database" / "SQLite_db.sql").resolve()))
        database_connection.executescript(file.read())
        database_connection.commit()
        database_connection.close()
