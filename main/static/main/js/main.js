function loadContent(tab, params = []) {
    var page = '';

    if (tab == '0') {
        page = 'main_screen';
    } else if (tab == '1') {
        page = '/ads';
    } else if (tab == '2') {
        page = '/profile';
    } else if (tab == '3') {
        page = '/leaders';
    } else if (tab == '4') {
        page = '/academy';
    } else if (tab == '5'){
        page = "/course";
    } else if (tab == '6'){
        page = 'challenge'
    } else if (tab == '7'){
        page = 'counter'
    }

    var loadingKey = 'loadingScreenShown_' + page;
    var fixInputs = false;
    var loadingTimeout;
    var loadingScreenHidden = false;

    // Проверяем, был ли экран загрузки уже показан для этой вкладки
    if (!sessionStorage.getItem(loadingKey)) {
        // Показываем экран загрузки
        var loadingScreen = document.getElementById('loading-screen');
        loadingScreen.style.display = 'flex';
        loadingScreen.style.opacity = '1'; // Для анимации, если необходимо

        // Запускаем таймер на 4 секунды для скрытия экрана загрузки
        loadingTimeout = setTimeout(function() {
            hideLoadingScreen(true); // Передаем true, чтобы указать, что это вызов по таймеру
        }, 4000);
        fixInputs = true;

    }

    // Функция для скрытия экрана загрузки
    function hideLoadingScreen(timeoutReached) {
        if (!loadingScreenHidden && !sessionStorage.getItem(loadingKey)) {
            loadingScreenHidden = true; // Устанавливаем флаг, что экран уже скрыт
            var loadingScreen = document.getElementById('loading-screen');
            // Скрываем экран загрузки после завершения анимации
            // явно запускаем анимацию opacity
        loadingScreen.style.opacity = '0';

        // после завершения transition скрываем элемент полностью
        setTimeout(function() {
            loadingScreen.style.display = 'none';
        }, 600); // время должно соответствовать CSS-переходу

            // Помечаем, что экран загрузки уже был показан для этой вкладки
            sessionStorage.setItem(loadingKey, 'true');

            // Очищаем таймер, если контент загрузился до истечения 4 секунд
            if (!timeoutReached) {
                clearTimeout(loadingTimeout);
            }
        }
    }

    if (params.length > 0) {
        let queryParams = params.map(param => param.split('=').map(encodeURIComponent).join('=')).join('&');
        page += (page.includes('?') ? '&' : '?') + queryParams;
    }


    var xhr = new XMLHttpRequest();
    xhr.open('GET', page, true);  // Используем URL с параметром
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Удаляем класс pressed у всех кнопок
            var buttons = document.getElementsByClassName('single-button');
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove('pressed');
            }
            // Добавляем класс pressed текущей кнопке
            var currentButton = document.getElementById('custom-button' + tab);
            if (currentButton){
                currentButton.classList.add('pressed');
            }

            var contentElement = document.getElementById('content');
            contentElement.innerHTML = xhr.responseText;
            history.pushState(null, '' + tab);



            if (tab == '0') {
                initHomeJS();
            } else if (tab == '1') {
                initAdsJS();
            } else if (tab == '2') {
                initProfileJS();
            } else if (tab == '3') {
                initLeadersJS();
            } else if (tab == '4') {
                initAcademyJS();
            } else if (tab == '5'){
                initCourseJS();
            } else if (tab == '6'){
                page = 'challenge'
            } else if (tab == '7'){
                page = 'counter'
            }


            // Проверяем, загружены ли все CSS файлы
            var cssPromises = [];
            var stylesheets = contentElement.getElementsByTagName('link');
            for (var i = 0; i < stylesheets.length; i++) {
                if (stylesheets[i].rel === 'stylesheet') {
                    cssPromises.push(new Promise(function(resolve, reject) {
                        stylesheets[i].onload = resolve;
                        stylesheets[i].onerror = reject;
                    }));
                }
            }

            // Ждем загрузки всех стилей
            if (cssPromises.length > 0) {
                Promise.all(cssPromises).then(function() {
                    hideLoadingScreen(false);

                }).catch(function(error) {
                    console.error('Ошибка загрузки стилей:', error);
                    hideLoadingScreen(false); // Даже если произошла ошибка, скрываем экран загрузки
                });
            } else {
                // Если стилей нет, скрываем экран загрузки сразу
                hideLoadingScreen(false);
            }
            const allInputs = document.querySelectorAll('input');
            const targetInputs = Array.from(document.querySelectorAll('input'));
            iphoneFix(targetInputs);


        }
    };
    xhr.send();


}

function iphoneFix(targetInputs) {
    const body = $('body');

    // Снимаем старые обработчики
    body.off('click.iphoneFix');
    targetInputs.forEach(input => $(input).off('click.iphoneFix'));
    $('textarea, select').off('click.iphoneFix');

    // Обработчик клика по body
    body.on('click.iphoneFix', function (event) {
        const isClickInsideTaskDesc = $(event.target).closest('#task-desc-text').length > 0;
        const isClickOnAnyTargetInput = targetInputs.some(input => $(event.target).is(input));
        const isClickOnTextareaOrSelect = $(event.target).is('textarea, select');

        if (!isClickInsideTaskDesc && !isClickOnAnyTargetInput && !isClickOnTextareaOrSelect) {
            document.activeElement.blur();
            console.log("blur");
        }
    });

    // Привязываем новый обработчик на каждый input
    targetInputs.forEach(input => {
        $(input).on('click.iphoneFix', function (event) {
            event.stopPropagation();
        });
    });

    // Добавляем обработчики на textarea и select
    $('textarea, select').on('click.iphoneFix', function (event) {
        event.stopPropagation();
    });
}



// Основная функция загрузки
window.onload = function() {
    sessionStorage.clear()
    loadContent(1);
};

// Отключаем вертикальные свайпы при открытии в Telegram Web App
if (window.Telegram && window.Telegram.WebApp) {
    window.Telegram.WebApp.disableVerticalSwipes();
    window.Telegram.WebApp.expand(); // Разворачиваем приложение на весь экран

}
function ShowAndHideLoadingScreen(loadingKey) {

    if (!sessionStorage.getItem(loadingKey)) {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.style.display = 'flex';
        // Скрываем экран загрузки после завершения анимации
        setTimeout(function() {
            loadingScreen.style.display = 'none';
        }, 600);
    }
    sessionStorage.setItem(loadingKey, 'true');
}

function toggleVisibility(blockToShow, blockToHide) {
    if (blockToHide){
        blockToHide.classList.add('hidden');
    }
    if (blockToShow){
        blockToShow.classList.remove('hidden');
    }
}

function toggleVisibilityMultiply(blockToShow, blocksToHide) {
    blocksToHide.forEach(block => block.classList.add('hidden'));
    if (blockToShow) blockToShow.classList.remove('hidden');
}

function toggleBlur(blockToBlur, blockToUnBlur) {
    if (blockToBlur){
        blockToBlur.classList.add('blurred');
    }
    if (blockToUnBlur){
        blockToUnBlur.classList.remove('blurred');
    }
}

function getToken(){
    const contentDiv = document.getElementById('content');
    const csrfToken = contentDiv.getAttribute('data-csrf-token');
    return csrfToken;
}

//if (window.visualViewport) {
//    // Сохраняем начальную высоту при первом вызове
//    const initialHeight = window.visualViewport.height;
//
//    window.visualViewport.addEventListener('resize', () => {
//        const currentHeight = window.visualViewport.height;
//        const offset = initialHeight - currentHeight;
//
//        // Смещаем body на рассчитанное значение
//        // Опционально: подгоняем высоту, если нужно
//        document.body.style.height = `${currentHeight}px`;
//    });
//}
