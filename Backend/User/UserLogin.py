from Backend.ConstantStorage import *


class UserLogin:

    def from_db(self, user_nickname, db):
        self.__user = db.get_user_by_nickname(user_nickname)
        print(self.__user)
        return self

    def create(self, user):
        self.__user = user
        print(self.__user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user[1]

    def get_nickname(self):
        return str(self.__user[1]) if self.__user else "No nickname"

    def get_email(self):
        return str(self.__user[2]) if self.__user else "No email"

    def get_account_creation_time(self):
        return str(self.__user[5]) if self.__user else "Not created"

    def get_avatar(self, app):
        img = None
        if self.__user and not self.__user[4]:
            try:
                with app.open_resource(str(Path(
                        Path(app.root_path) / ".." / "Frontend" / "static" / "img" / "default_img" / "default_avatar.png").resolve()),
                                       "rb") as f:
                    img = f.read()
            except FileNotFoundError as error:
                print(str(Path(
                    Path(app.root_path) / ".." / "Frontend" / "static" / "img" / "default_img" / "default_avatar.png").resolve()) + ": Not found")
        else:
            img = self.__user[AVATAR]

        return img
