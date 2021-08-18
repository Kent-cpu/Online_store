import { addOrRemoveClass } from "./general_functions.mjs";

import { EMAIL, PASSWORD, AUTHORIZATION, DATA, REMEMBER_ME } from "./constantStorage.mjs";



const itemForm = document.querySelectorAll(".authorization__form__item");
const inputForm = document.querySelectorAll(".authorization__form__item__input");
const informationError = document.querySelectorAll(".info-error");

itemForm.forEach((item) => {
    item.addEventListener("mousedown", e => {
        if (!e.target.classList.contains("authorization__form__item__input")) {
            e.preventDefault();
        }
        item.querySelector(".authorization__form__item__input").focus();
    })
});

inputForm.forEach((item) => {
    item.addEventListener("blur", () => {
        const labelForm = document.querySelectorAll(".authorization__form__item__label");
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
        item.closest(".authorization__form__item").querySelector(".authorization__form__item__label").classList.add("_active");
        addOrRemoveClass("_error", "remove", item, informationError[indexInputForm]);
    });
});


document.querySelectorAll(".showHidePasswordBtn").forEach((currentButton) => { // Кнопка показать/скрыть пароль
    currentButton.addEventListener("mousedown", e => {
        e.preventDefault();
        let currentInput = currentButton.closest(".authorization__form__item").querySelector(".authorization__form__item__input");
        if (currentInput.getAttribute("type") === "password") {
            currentInput.setAttribute("type", "text");
        } else {
            currentInput.setAttribute("type", "password");
        }
        currentButton.classList.toggle("_icon-eye-blocked");
    });
});



document.querySelector(".authorization__form__item__submit").addEventListener("click", e => {
    e.preventDefault();
    inputForm.forEach((input, index) => {
        validate(input, index);
    });

    let correctData = Array.from(itemForm).every(inputField => {
        return !inputField.classList.contains("_error") && inputField.querySelector(".authorization__form__item__input").value.length > 0;
    });

    if (correctData) {
        authorization();
    }
});


function validate(input, indexErrorInfo) {
    if (input.classList.contains("required") && input.value.length === 0) {
        informationError[indexErrorInfo].innerHTML = "Required field";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else {
        addOrRemoveClass("_error", "remove", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    }
}


async function authorization() {
    let requestedData = {
        type: AUTHORIZATION,
        [DATA]: {
            [EMAIL]: document.querySelector("._email").value,
            [PASSWORD]: document.querySelector("._password").value,
            [REMEMBER_ME]: document.querySelector('.checkRemeber').checked,
        },
    };

    try {
        const response = await fetch('/authorization', {
            method: 'POST',
            body: JSON.stringify(requestedData),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const userData = await response.json();
        console.log(userData)
        if (userData.type === "OK_CODE") {
            window.location.href = "/";
        } else {
            itemForm.forEach((input, index) => {
                informationError[index].innerHTML = "The data you used to sign in is invalid."
                addOrRemoveClass("_error", "add", input, informationError[index]);
            });
        }
    } catch (err) {
        console.log(err);
    }
}