//  D:\Python\myProject\bookshelves\app\static\deps\js\base.js

//Простой скрипт для реализации параллакса
window.addEventListener('scroll', function () {
    var scrolled = window.scrollY;
    var wrapper = document.querySelector('.wrapper');
    wrapper.style.backgroundPositionY = -(scrolled * 0.25) + 'px'; // Скорость может быть настроена здесь
});

//---------------------------

//// Реализуем залипание header Если прокрутка больше или равна его положения
//function initStickyHeader() {
//    // Получаем ссылку на элемент header
//    const header = document.querySelector('.header-container');
//
//    // Получаем начальное положение header от верха страницы
//    const initialOffset = header.offsetTop;
//
//    // Функция для обработки события скроллинга
//    function handleScroll() {
//        // Если прокрутка больше или равна начальному положению header
//        if (window.pageYOffset >= initialOffset) {
//            // Добавляем класс .fixed
//            header.classList.add('fixed');
//        } else {
//            // Убираем класс .fixed
//            header.classList.remove('fixed');
//        }
//    }
//
//    // Добавляем обработчик события скроллинга
//    window.addEventListener('scroll', handleScroll);
//}
//
//// Вызываем функцию при загрузке страницы
//document.addEventListener('DOMContentLoaded', initStickyHeader);

//---------------------------

//// Скрол
//document.addEventListener('DOMContentLoaded', function() {
//    const header = document.querySelector('.header-container');
//    const scrollToTopButtonContainer = document.querySelector('.buttons_scroll');
//    const scrollToTopButtonUp = document.getElementById('button_scroll_up');
//    const scrollToTopButtonDown = document.getElementById('button_scroll_down');
//
//    const initialOffset = header.offsetTop + header.clientHeight;
//
//    function toggleScrollButton() {
//        if (window.pageYOffset >= initialOffset) {
//            scrollToTopButtonContainer.style.display = 'block';
//
//        } else {
//            scrollToTopButtonContainer.style.display = 'none';
//
//        }
//    }
//
//    function scrollToTop() {
//        window.scrollTo({
//            top: 0,
//            behavior: 'smooth'
//        });
//    }
//
//    window.addEventListener('scroll', function() {
//        toggleScrollButton();
//    });
//
//    scrollToTopButtonContainer.addEventListener('click', scrollToTop);
//});


// Функция для настройки кнопок скроллинга
function setupScrollButtons() {
    // Получаем элементы DOM
    const header = document.querySelector('.header-container');
    const scrollToTopButtonContainer = document.querySelector('.buttons_scroll');
    const scrollToTopButtonDown = document.getElementById('button_scroll_down');
    const footer = document.querySelector('footer');

    // Получаем начальное положение низа header от верха страницы
    const initialOffset = header.offsetTop + header.clientHeight;

    // Функция для отображения/скрытия кнопок и обработки футера
    function toggleScrollButton() {
        if (window.pageYOffset >= initialOffset) {
            // Если прокрутка больше или равна начальному положению header,
            // отображаем кнопки и прижимаем их к нижнему краю
            scrollToTopButtonContainer.style.display = 'block';
            scrollToTopButtonContainer.classList.add('buttons_position');
            scrollToTopButtonDown.classList.remove('display_none');
        } else {
            // Иначе скрываем кнопки
            scrollToTopButtonContainer.style.display = 'none';
        }

        // Получаем координаты и размеры футера
        const footerRect = footer.getBoundingClientRect();
        const isFooterVisible = footerRect.top >= 0 && footerRect.top <= window.innerHeight;

        if (isFooterVisible) {
            // Если футер виден, убираем прижимание кнопок и скрываем кнопку "вниз"
            scrollToTopButtonContainer.classList.remove('buttons_position');
            scrollToTopButtonDown.classList.add('display_none');
        }
    }

    // Добавляем обработчик события скроллинга
    window.addEventListener('scroll', toggleScrollButton);
}

// Функция для плавной прокрутки вверх
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Функция для плавной прокрутки вниз (в конец страницы)
function scrollToBottom() {
    const body = document.body;
    const html = document.documentElement;

    // Получаем максимальную высоту страницы
    const height = Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight
    );

    // Прокручиваем вниз
    window.scrollTo({
        top: height,
        behavior: 'smooth'
    });
}

// Событие после полной загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    // Вызываем функцию настройки кнопок
    setupScrollButtons();

    // Получаем элементы кнопок
    const scrollToTopButtonUp = document.getElementById('button_scroll_up');
    const scrollToTopButtonDown = document.getElementById('button_scroll_down');

    // Добавляем обработчики кликов
    scrollToTopButtonUp.addEventListener('click', scrollToTop);
    scrollToTopButtonDown.addEventListener('click', scrollToBottom);
});
