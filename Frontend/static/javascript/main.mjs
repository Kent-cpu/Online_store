import { REQUESTED_DATA, USER_INFO } from "./constantStorage.mjs"

"use strict"



document.addEventListener("DOMContentLoaded", (e) => {
    postDataUser();

    async function postDataUser() {
        let requestedData = {
            type: USER_INFO,
            [REQUESTED_DATA]: ["nickname"],
        };

        try {
            const response = await fetch('/shop', {
                method: 'POST',
                body: JSON.stringify(requestedData),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const userData = await response.json();
            console.log(userData)
            showOrHideProfile(userData);
        } catch (err) {
            console.log(err);
        }
    }

    function showOrHideProfile(userData) {
        if (userData.data.is_login) {
            document.querySelector('.user-profile').style.display = "block";
            document.querySelector('.user-profile__nickname').innerHTML = userData.requested_data.nickname;
        } else {
            document.querySelector('.btn-wrapper').style.display = "block";
        }
    }

    document.querySelectorAll('.faq-accordion__item-trigger').forEach(titleAccordion => {
        titleAccordion.addEventListener('click', (e) => {
            e.target.closest('.faq-accordion__item').classList.toggle('faq-accordion__item--active');
        })
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".user-profile")) {
            document.querySelector('.user-profile__list').classList.remove('user-profile__list_open');
            document.querySelector('.user-profile__trigger').classList.remove('user-profile__trigger_open');
        }
    });

    document.querySelector('.user-profile').addEventListener('click', () => {
        document.querySelector('.user-profile__list').classList.toggle('user-profile__list_open');
        document.querySelector('.user-profile__trigger').classList.toggle('user-profile__trigger_open');
    });

    document.querySelector('.exit-profile').addEventListener('click', () => {
        window.location.href = '/logout';
    });
});







