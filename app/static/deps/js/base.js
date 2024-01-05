//  D:\Python\myProject\bookshelves\app\static\deps\js\base.js

//Простой скрипт для реализации параллакса
window.addEventListener('scroll', function () {
    var scrolled = window.scrollY;
    var wrapper = document.querySelector('.wrapper');
    wrapper.style.backgroundPositionY = -(scrolled * 0.25) + 'px'; // Скорость может быть настроена здесь
});

// Простой скрипт для реализации параллакса
// window.addEventListener('scroll', function () {
//     var scrolled = window.scrollY;
//     var wrapper = document.querySelector('.wrapper');

//     // Получаем высоту фоновой картинки
//     var backgroundImageHeight = wrapper.offsetWidth * 1; // 2362:2362 (Предполагаемый аспект 16:9 (высота = ширина * 9/16))

//     // Проверяем, достигла ли фоновая картинка своего низа
//     if (scrolled < backgroundImageHeight) {
//         wrapper.style.backgroundPositionY = -(scrolled * 0.1) + 'px'; // Скорость может быть настроена здесь
//     }
// });

// // Простой скрипт для реализации параллакса
// window.addEventListener('scroll', function () {
//     var scrolled = window.scrollY;
//     var wrapper = document.querySelector('.wrapper');
    
//     // Получаем высоту контента на странице
//     var contentHeight = document.body.scrollHeight;

//     // Получаем высоту видимой области экрана браузера
//     var windowHeight = window.innerHeight;

//     // Рассчитываем высоту страницы, учитывая контент и скроллинг
//     var totalHeight = Math.max(contentHeight, windowHeight);

//     // Рассчитываем коэффициент скорости для скроллинга фоновой картинки
//     var speedCoefficient = totalHeight / contentHeight;

//     // Применяем коэффициент скорости к скроллу
//     wrapper.style.backgroundPositionY = -(scrolled * speedCoefficient) + 'px';
// });




