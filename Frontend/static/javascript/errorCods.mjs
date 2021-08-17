const OK_CODE = 1000;
const ERROR_CODE = 1001;
const UNIQUE_FIELD_ERROR_CODE = 1002;
const USER_DOES_NOT_EXIT_ERROR_COD = 1003;
CODE_MAP.set(OK_CODE, "OK")
    .set(ERROR_CODE, "Error")
    .set(UNIQUE_FIELD_ERROR_CODE, "Error getting a copy of a unique field")
    .set(USER_DOES_NOT_EXIT_ERROR_COD, "This user does not exist"); // Расшифровка кодов


function get_code_info(code) {
    if CODE_MAP.has(code) {
        return CODE_MAP.get(code);
    }
    else {
        return "ERROR";
    }
}