import { addOrRemoveClass } from "./general_functions.mjs";
import { NICKNAME, EMAIL, PASSWORD, CHECK_DATA_FOR_UNIQUENESS, REGISTRATION, DATA } from "./constantStorage.mjs";

const itemForm = document.querySelectorAll(".registration__form__item");
const inputForm = document.querySelectorAll(".registration__form__item__input");
const informationError = document.querySelectorAll(".info-error");


itemForm.forEach((item) => {
    item.addEventListener("mousedown", e => {
        if (!e.target.classList.contains("registration__form__item__input")) {
            e.preventDefault();
        }
        item.querySelector(".registration__form__item__input").focus();
    });
});

inputForm.forEach((item) => {
    item.addEventListener("blur", () => {
        const labelForm = document.querySelectorAll(".registration__form__item__label");
        for (let i = 0; i < inputForm.length; ++i) {
            if (inputForm[i].value.length === 0) {
                labelForm[i].classList.remove("_active");
            }
        }
        let indexInputForm = [...inputForm].indexOf(item);
        validate(item, indexInputForm);
    });

    item.addEventListener("focus", () => {
        let indexInputForm = [...inputForm].indexOf(item);
        item.closest(".registration__form__item").querySelector(".registration__form__item__label").classList.add("_active");
        addOrRemoveClass("_error", "remove", item, informationError[indexInputForm]);
    });
});


document.querySelectorAll(".showHidePasswordBtn").forEach((currentButton) => { // Кнопка показать/скрыть пароль
    currentButton.addEventListener("mousedown", e => {
        e.preventDefault();
        let currentInput = currentButton.closest(".registration__form__item").querySelector(".registration__form__item__input");
        if (currentInput.getAttribute("type") === "password") {
            currentInput.setAttribute("type", "text");
        } else {
            currentInput.setAttribute("type", "password");
        }
        currentButton.classList.toggle("_icon-eye-blocked");
    });
});



document.querySelector(".registration__form__item__submit").addEventListener("click", e => {
    e.preventDefault();
    inputForm.forEach((inputField, index) => {
        validate(inputField, index);
    });
    let correctData = Array.from(itemForm).every(inputField => {
        return !inputField.classList.contains("_error") && inputField.querySelector(".registration__form__item__input").value.length > 0;
    });
    if (correctData) {
        e.target.classList.add("registration__form__item__submit_disabled");
        setTimeout(registration, 15000);
    }
});


function validate(input, indexErrorInfo) {
    const regularEmail = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    const regularPassword = /^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{8,}$/;
    const regularNickname = /^[a-z0-9_-]{5,15}$/i;


    addOrRemoveClass("_error", "remove", informationError[indexErrorInfo], itemForm[indexErrorInfo]);

    if (input.classList.contains("required") && input.value.length === 0) {
        informationError[indexErrorInfo].innerHTML = "Required field";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains("_nickname")) {
        if (!regularNickname.test(String(input.value))) {
            informationError[indexErrorInfo].innerHTML = "Wrong format";
            addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
        }

        checkingForUniquenessData(input).then(coincidence => {
            console.log(coincidence)
            if (coincidence) {
                informationError[indexErrorInfo].innerHTML = "Already taken";
                addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
            }
        });

    }
    else if (input.classList.contains("_email")) {
        if (!regularEmail.test(String(input.value))) {
            informationError[indexErrorInfo].innerHTML = "Invalid email address";
            addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
        }

        checkingForUniquenessData(input).then(coincidence => {
            if (coincidence) {
                informationError[indexErrorInfo].innerHTML = "This email is registered.";
                addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
            }
        });
    }
    else if (input.classList.contains("_password")) {
        const inputPassword = document.querySelectorAll("._password");

        if (!regularPassword.test(String(input.value))) {
            informationError[indexErrorInfo].innerHTML = "Wrong format";
            addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
        }

        if (inputPassword[0].value != inputPassword[1].value && inputPassword[0].value.length > 0 && inputPassword[1].value.length > 0) {
            inputForm.forEach((element, index) => {
                if (element.id === "psw-repeat") {
                    informationError[index].innerHTML = "Passwords don't match";
                    addOrRemoveClass("_error", "add", informationError[index], itemForm[index]);
                }
            });
        }
        else {
            itemForm.forEach((element, index) => {
                if (element.querySelector('#psw-repeat')) {
                    addOrRemoveClass("_error", "remove", element, informationError[index]);
                }
            });
        }
    }
}

async function checkingForUniquenessData(input) {
    let requestedData = {
        type: [CHECK_DATA_FOR_UNIQUENESS],
        [DATA]: {
            [input.name]: String(input.name),
        },
    }

    try {
        const response = await fetch('/registration', {
            method: 'POST',
            body: JSON.stringify(requestedData),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const answer = await response.json();
        console.log(answer)
        if (answer.type === "OK_CODE") {
            return false;
        }
        return true;
    } catch (err) {
        console.error(err);
    }
}

async function registration() {
    let sentData = {
        type: [REGISTRATION],
        [DATA]: {
            [NICKNAME]: document.querySelector("._nickname").value,
            [EMAIL]: document.querySelector("._email").value,
            [PASSWORD]: document.querySelector("._password").value,
        },
    };
    try {
        const response = await fetch('/registration', {
            method: 'POST',
            body: JSON.stringify(sentData),
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (response.ok) {
            window.location.href = "/";
        }
    } catch (err) {
        console.error(err);
    }
}