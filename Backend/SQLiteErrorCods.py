from typing import Final

OK_CODE: Final = 1000  #
ERROR_CODE: Final = 1001  #
UNIQUE_FIELD_ERROR_CODE: Final = 1002  #
CODE_DICT: Final = {OK_CODE: "OK", ERROR_CODE: "Error", UNIQUE_FIELD_ERROR_CODE: "Error getting a copy of a unique field"}  # Расшифровка кодов


def get_code_info(code):
    try:
        return CODE_DICT.get(code["ERROR"])
    finally:
        return "ERROR"
