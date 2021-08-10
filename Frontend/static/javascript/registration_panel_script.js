const itemForm = document.querySelectorAll(".registration__form__item");
const inputForm = document.querySelectorAll(".registration__form__item__input");
const informationError = document.querySelectorAll(".info-error");
let data = {
    type: "",
    text: "",
};

itemForm.forEach((item) => {
    item.addEventListener("mousedown", e => {
        if (!e.target.classList.contains("registration__form__item__input")) {
            e.preventDefault();
        }
        item.querySelector(".registration__form__item__input").focus();
    })
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
    let correctData = Array.from(itemForm).every(inputField => {
        return !inputField.classList.contains("_error") && inputField.querySelector(".registration__form__item__input").value.length > 0;
    });
    if (correctData) {
        registration();
    } else {
        inputForm.forEach((inputField, index) => {
            validate(inputField, index);
        });
    }
});


function validate(input, indexErrorInfo) {
    const regularEmail = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    const regularPassword = /^(?=.*\d)(?=.*[A-Z]).{8,}$/;
    const regularNickname = /^[a-z0-9_-]{5,15}$/i;

    /^(?=.{5,20}$)[a-zA-Z][a-zA-Z0-9]*(?: [a-zA-Z0-9]+)*$/;

    if (input.classList.contains("required") && input.value.length === 0) {
        informationError[indexErrorInfo].innerHTML = "Required field";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains("_nickname") && !regularNickname.test(String(input.value))) {
        informationError[indexErrorInfo].innerHTML = "Wrong format";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    }
    else if (input.classList.contains("_email") && !regularEmail.test(String(input.value))) {
        informationError[indexErrorInfo].innerHTML = "Invalid email address";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains("_password") && !regularPassword.test(String(input.value))) {
        informationError[indexErrorInfo].innerHTML = "Wrong format";
        addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains("_password")) {
        const inputPassword = document.querySelectorAll("._password");
        let indexInputPassword = [...inputForm].indexOf(inputPassword[1]);
        if (inputPassword[0].value != inputPassword[1].value && inputPassword[0].value.length > 0 && inputPassword[1].value.length > 0) {
            informationError[indexInputPassword].innerHTML = "Passwords don't match";
            addOrRemoveClass("_error", "add", informationError[indexInputPassword], itemForm[indexInputPassword]);
        } else {
            for (let i = 0; i < inputPassword.length; ++i) {
                addOrRemoveClass("_error", "remove", informationError[indexInputPassword - i], itemForm[indexInputPassword - i]);
            }
        }
    } else if (input.classList.contains("_email") || input.classList.contains("_nickname")) {
        checkingForUniquenessData(input, indexErrorInfo);
    } else {
        addOrRemoveClass("_error", "remove", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    }
}

function checkingForUniquenessData(input, indexErrorInfo) {
    const request = new XMLHttpRequest();  // Получение объетка запроса
    request.open("POST", "/registration");
    request.setRequestHeader("Content-Type", "application/json");
    if (input.classList.contains("_email")) {
        data["type"] = "email";
        data["text"] = String(input.value);
    } else if (input.classList.contains("_nickname")) {
        data["type"] = "nickname";
        data["text"] = String(input.value);
    }

    request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции registration()
        if (request.readyState === 4 && request.status === 200) { // Успешное получение данных с сервера
            answer = JSON.parse(request.responseText);
            if (answer["type"] === "ERROR_CODE") {
                if (answer["text"] === "email;" && input.classList.contains("_email")) {
                    informationError[indexErrorInfo].innerHTML = "This email is registered. Enter another.";
                    addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
                } else if (answer["text"] === "nickname;" && input.classList.contains("_nickname")) {
                    informationError[indexErrorInfo].innerHTML = "Already taken";
                    addOrRemoveClass("_error", "add", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
                }
            } else {
                addOrRemoveClass("_error", "remove", informationError[indexErrorInfo], itemForm[indexErrorInfo]);
            }
        }
    }
    request.send(JSON.stringify(data));
}


function addOrRemoveClass(className, action, ...args) {
    for (let i = 0; i < args.length; ++i) {
        if (action === "add") {
            args[i].classList.add(className);
        } else if (action === "remove") {
            args[i].classList.remove(className);
        }
    }
}

function registration() {
    const request = new XMLHttpRequest();  // Получение объетка запроса
    request.open("POST", "/registration");
    request.setRequestHeader("Content-Type", "application/json");
    let result = {
        type: "registration",
        nickname: document.getElementById("nickname").value,
        email: document.getElementById("email").value,
        password: document.getElementById("psw").value,
    }
    request.send(JSON.stringify(result));  // Отправка данных

    request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции registration()
        if (request.readyState === 4 && request.status === 200) { // Успешное получение данных с сервера
            answer = request.responseText;  // Получение переданных данных в виде строки
            console.log(answer)
            if (answer === "1000") {  // Успешно
                console.log("Correct");
            } else if (answer.startsWith("1002:")) { // Ошибка Уникальности
                answer = answer.substr(answer.indexOf(":") + 1)  // Парсим, нужно переделать
                index = answer.indexOf(";")
                while (index != -1) {
                    console.log(answer.slice(0, index))
                    answer = answer.substr(index + 1)
                    index = answer.indexOf(";")
                }
                console.log(request.responseText)
            } else {
                console.log("Error")
            }
        }
    }
}