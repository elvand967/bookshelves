// D:\Python\myProject\bookshelves\app\audiobooks\static\audiobooks\js\audiobooks.js

//// аккордеон Вертикального меню
//document.addEventListener("DOMContentLoaded", function() {
//    var categoryHeaders = document.querySelectorAll(".category-header");
//
//    categoryHeaders.forEach(function(header) {
//        header.addEventListener("click", function() {
//            var subcategoryList = this.nextElementSibling;
//            subcategoryList.style.display = subcategoryList.style.display === "none" ? "block" : "none";
//        });
//    });
//});


// Фиксация выбора вертикального меню
document.addEventListener("DOMContentLoaded", function () {
    var categoryHeaders = document.querySelectorAll(".category-header");

    categoryHeaders.forEach(function (header) {
        header.addEventListener("click", function () {
            var subcategoryList = this.nextElementSibling;
            subcategoryList.style.maxHeight = subcategoryList.style.maxHeight === "0px" ? subcategoryList.scrollHeight + "px" : "0px";

            // Учет выбора: добавляем класс 'selected' и убираем его у предыдущего выбранного элемента
            var selectedElement = document.querySelector(".selected");
            if (selectedElement) {
                selectedElement.classList.remove("selected");
            }
            this.classList.add("selected");
        });
    });
});



// Функция form name="search", формы `поиск`
// Активация/деактивация кнопок сброс и поиск
// в зависимости наличия заполненных полей input type="text"
function updateSearchButton(buttonReset = false) {
    var inputs = document.forms['search'].querySelectorAll('input[type="text"]');
    var resetButton = document.forms['search'].querySelector('button[name="reset"]');
    var submitButton = document.forms['search'].querySelector('button[name="submit"]');

    var atLeastOneFilled = Array.from(inputs).some(function (input) {
        return input.value.trim() !== '';
    });

    resetButton.disabled = !atLeastOneFilled;
    submitButton.disabled = !atLeastOneFilled;

    if (buttonReset) {
        inputs.forEach(function (input) {
            input.value = '';
        });
        resetButton.disabled = true;
        submitButton.disabled = true;
    }
}

// Функция для второй формы ()
// Функция form name="ratings", формы `сортировки по рейтингам`
// Активация/деактивация кнопки сброс
// в зависимости наличия заполненных полей select.option value="..."
function updateResetButton(formId) {
    // Получаем все селекторы внутри указанной формы
    var form = document.forms[formId];
    var selectors = form.querySelectorAll('select');

    // Получаем кнопку "Сброс"
    var resetButton = form.querySelector('button[type="reset"]');

    // Флаг, указывающий, есть ли хотя бы один выбранный селектор
    var atLeastOneSelected = false;

    // Проходим по всем селекторам
    selectors.forEach(function (selector) {
        // Получаем соответствующий label
        var label = form.querySelector('label[for="' + selector.id + '"]');

        // Проверяем, имеет ли текущий селектор выбранное значение
        if (selector.value.trim() !== '') {
            atLeastOneSelected = true;
            // Устанавливаем цвет для label и селектора при выборе значения
            label.style.color = '#5E68F6'; // Или любой другой цвет
            selector.style.color = '#5E68F6';
        } else {
            // Устанавливаем цвет по умолчанию для label и селектора при отсутствии выбранного значения
            label.style.color = '#808080';
            selector.style.color = '#808080';
        }
    });

    // Активируем/деактивируем кнопку "Сброс" в зависимости от наличия выбранных селекторов
    resetButton.disabled = !atLeastOneSelected;
}

// Вызываем функцию для инициализации состояния кнопки "Сброс" при загрузке страницы
updateResetButton('ratings');