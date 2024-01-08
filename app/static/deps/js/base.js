//  D:\Python\myProject\bookshelves\app\static\deps\js\base.js

//Простой скрипт для реализации параллакса
window.addEventListener('scroll', function () {
    var scrolled = window.scrollY;
    var wrapper = document.querySelector('.wrapper');
    wrapper.style.backgroundPositionY = -(scrolled * 0.25) + 'px'; // Скорость может быть настроена здесь
});

//---------------------------

// Реализуем залипание header Если прокрутка больше или равна его положения
function initStickyHeader() {
    // Получаем ссылку на элемент header
    const header = document.querySelector('.header-container');

    // Получаем начальное положение header от верха страницы
    const initialOffset = header.offsetTop;

    // Функция для обработки события скроллинга
    function handleScroll() {
        // Если прокрутка больше или равна начальному положению header
        if (window.pageYOffset >= initialOffset) {
            // Добавляем класс .fixed
            header.classList.add('fixed');
        } else {
            // Убираем класс .fixed
            header.classList.remove('fixed');
        }
    }

    // Добавляем обработчик события скроллинга
    window.addEventListener('scroll', handleScroll);
}

// Вызываем функцию при загрузке страницы
document.addEventListener('DOMContentLoaded', initStickyHeader);