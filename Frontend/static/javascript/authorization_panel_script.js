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
    checkingForUniquenessData();
    let correctData = Array.from(itemForm).every(inputField => {
        return !inputField.classList.contains("_error") && inputField.querySelector(".authorization__form__item__input").value.length > 0;
    });
    if (correctData) {
        authorization();
    } else {
        inputForm.forEach((inputField, index) => {
            validate(inputField, index);
        });
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

function checkingForUniquenessData() {
    const request = new XMLHttpRequest();  // Получение объетка запроса
    request.open("POST", "/authorization");
    request.setRequestHeader("Content-Type", "application/json");

    let data = {
        type: "authorization",
        email: inputForm[0].value,
        password: inputForm[1].value,
        remember_me: document.querySelector('.checkRemeber').checked, // Проверка checkbox "Запомнить меня" true/false
    }

    request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции authorization()
        if (request.readyState === 4 && request.status === 200) { // Успешное получение данных с сервера
            answer = JSON.parse(request.responseText);
            if (answer["type"] === "ERROR_CODE") {
                console.log("Ошибка");
                itemForm.forEach((element, index) => {
                    informationError[index].innerHTML = "The data you used to sign in is invalid."
                    addOrRemoveClass("_error", "remove", element, informationError[index]);
                });
            } else {
                itemForm.forEach((element, index) => {
                    addOrRemoveClass("_error", "remove", element, informationError[index]);
                });
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

function authorization() {
    const request = new XMLHttpRequest();  // Получение объетка запроса
    request.open("POST", "/authorization");
    request.setRequestHeader("Content-Type", "application/json");
    let data = {
        type: "authorization",
        email: document.getElementById("email").value,
        password: document.getElementById("psw").value,
        remember_me: document.querySelector('.checkRemeber').checked,
    }
    request.send(JSON.stringify(data));  // Отправка данных

    request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции authorization()
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
            } else {
                console.log("Error")
            }
        }
    }
}