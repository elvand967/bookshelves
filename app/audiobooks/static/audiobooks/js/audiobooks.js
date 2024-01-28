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
    var atLeastOneFilled = Array.from(inputs).some(input => input.value.trim() !== '');

    resetButton.disabled = !atLeastOneFilled;
    submitButton.disabled = !atLeastOneFilled;

    if (buttonReset) {
        inputs.forEach(function (input) {
            input.value = '';
        });
        resetButton.disabled = true;
        submitButton.disabled = true;
    }
    // Добавление или удаление класса в зависимости от состояния кнопок
    if (resetButton.disabled) {
        resetButton.classList.remove('button_active');
    } else {
        resetButton.classList.add('button_active');
    }

    if (submitButton.disabled) {
        submitButton.classList.remove('button_active');
    } else {
        submitButton.classList.add('button_active');
    }


}
