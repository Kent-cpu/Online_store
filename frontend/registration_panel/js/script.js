const itemForm = document.querySelectorAll('.registration__form__item');
const inputForm = document.querySelectorAll('.registration__form__item__input');
const labelForm = document.querySelectorAll('.registration__form__item__label');
const passwordButton = document.querySelectorAll('._icon-eye');
const registrationButton = document.querySelector('.registration__form__item__submit');
const informationError = document.querySelectorAll('.info-error');
let correctData = false;


itemForm.forEach((item) => {
    item.addEventListener('mousedown', (e) => {
        e.preventDefault();
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
    correctData = Array.from(itemForm).every((element) => {
        return !element.classList.contains('_error');
    })
    if (correctData) {
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
    } else {
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