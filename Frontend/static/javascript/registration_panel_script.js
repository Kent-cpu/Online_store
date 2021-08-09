const itemForm = document.querySelectorAll('.registration__form__item');
const inputForm = document.querySelectorAll('.registration__form__item__input');
const labelForm = document.querySelectorAll('.registration__form__item__label');
const passwordButton = document.querySelectorAll('._icon-eye');
const registrationButton = document.querySelector('.registration__form__item__submit');
const informationError = document.querySelectorAll('.info-error');
let date = {
    type: "",
    text: "",
};
let dateJson = "";

itemForm.forEach((item) => {
    item.addEventListener('mousedown', (e) => {
        if (!e.target.classList.contains('registration__form__item__input')) {
            e.preventDefault();
        }
        let currentInput = item.querySelector('.registration__form__item__input');
        currentInput.focus();
    })
});

inputForm.forEach((item) => {
    item.addEventListener('blur', () => {
        for (let i = 0; i < inputForm.length; ++i) {
            if (inputForm[i].value.length === 0) {
                labelForm[i].classList.remove('_active');
            }
        }
        let indexInputForm = [...inputForm].indexOf(item);
        validate(item, indexInputForm);
    })

    item.addEventListener('focus', () => {
        let indexInputForm = [...inputForm].indexOf(item);
        item.closest('.registration__form__item').querySelector('.registration__form__item__label').classList.add('_active');
        addOrRemoveClass('_error', 'remove', item, informationError[indexInputForm]);
    })

    item.addEventListener('keyup', (e) => {
        const request = new XMLHttpRequest();  // Получение объетка запроса
        request.open('POST', '/registration');
        request.setRequestHeader("Content-Type", "application/json");
        if (item.classList.contains('_email')) {
            date["type"] = "email";
            date["text"] = String(item.value);
        }

        request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции registration()
            if (request.readyState === 4 && request.status === 200) { // Успешное получение данных с сервера
                answer = request.responseText;  // Получение переданных данных в виде строки
                console.log(answer)
            }
        }
        dateJson = JSON.stringify(date);
        request.send(dateJson);
    });
})


passwordButton.forEach((currentButton) => {
    currentButton.addEventListener('mousedown', (e) => {
        e.preventDefault();
        let currentInput = currentButton.closest('.registration__form__item').querySelector('.registration__form__item__input');
        if (currentInput.getAttribute('type') === "password") {
            currentInput.setAttribute('type', 'text');
        } else {
            currentInput.setAttribute('type', 'password');
        }
        currentButton.classList.toggle('_icon-eye-blocked');
        return false;
    })

})



registrationButton.addEventListener('click', (e) => {
    e.preventDefault();
    let correctData = Array.from(itemForm).every((element) => {
        return !element.classList.contains('_error');
    })
    if (correctData) {
        registration()
        console.log("Зареган")
    } else {
        console.log("УУУ сука");
    }

})


function validate(input, indexErrorInfo) {
    const regularEmail = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    const regularPassword = /^(?=.*\d)(?=.*[A-Z]).{8,}$/;
    const informationError = document.querySelectorAll('.info-error');

    if (input.classList.contains('required') && input.value.length === 0) {
        informationError[indexErrorInfo].innerHTML = "Required field"
        addOrRemoveClass('_error', 'add', informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains('_email') && !regularEmail.test(String(input.value))) {
        informationError[indexErrorInfo].innerHTML = "Invalid email address";
        addOrRemoveClass('_error', 'add', informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains('_password') && !regularPassword.test(String(input.value))) {
        informationError[indexErrorInfo].innerHTML = "Wrong format";
        addOrRemoveClass('_error', 'add', informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    } else if (input.classList.contains('_password')) {
        const inputPassword = document.querySelectorAll('._password');
        if (inputPassword[0].value.length != 0 && inputPassword[1].value.length != 0 && inputPassword[0].value != inputPassword[1].value) {
            for (let i = 0; i < inputPassword.length; ++i) {
                let indexInputPassword = [...inputForm].indexOf(inputPassword[i]);
                informationError[indexInputPassword].innerHTML = "Passwords don't match";
                addOrRemoveClass('_error', 'add', informationError[indexInputPassword], itemForm[indexInputPassword]);
            }
        } else {
            for (let i = 0; i < inputPassword.length; ++i) {
                let indexInputPassword = [...inputForm].indexOf(inputPassword[i]);
                addOrRemoveClass('_error', 'remove', informationError[indexInputPassword], itemForm[indexInputPassword]);
            }
        }
    }
    else {
        addOrRemoveClass('_error', 'remove', informationError[indexErrorInfo], itemForm[indexErrorInfo]);
    }
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
    request.open('POST', '/registration');
    let result = {
        type: "registration",
        nickname: document.getElementById("nickname").value,
        email: document.getElementById("email").value,
        password: document.getElementById("psw").value,
    }


    request.onreadystatechange = function () {   // Функция активирующаяся при изменении статуса запроса, работает при завершение функции registration()
        if (request.readyState === 4 && request.status === 200) { // Успешное получение данных с сервера
            answer = request.responseText;  // Получение переданных данных в виде строки
            if (answer === "1000") {  // УСпешно
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
            } else {  // Ошибка
                console.log("Error")
            }
        }
    }
    request.send(JSON.stringify(result));  // Отправка данных
}