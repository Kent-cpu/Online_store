document.querySelectorAll('.faq-accordion__item-trigger').forEach(titleAccordion => {
    titleAccordion.addEventListener('click', (e) => {
        e.target.closest('.faq-accordion__item').classList.toggle('faq-accordion__item--active');
    })
});

