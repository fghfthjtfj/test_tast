// --- Вспомогательные функции ---

// Получение CSRF-токена из куков
const getCookie = (name) => {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
};

// Универсальная AJAX-функция (GET/POST/DELETE)
const ajaxRequest = (url, method = 'GET', data = null) => {
    const headers = {
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
    };

    const options = { method, headers };

    if (data) {
        options.body = data instanceof FormData ? data : JSON.stringify(data);
    }

    return fetch(url, options).then(response => {
        const type = response.headers.get('content-type');
        return type.includes('application/json') ? response.json() : response.text();
    });
};


function initAdsJS() {
    initToggleBorder('.active-list-switch');

    const adsDiv = document.getElementById('ads-page-div');
    const formDiv = document.getElementById('form-div');


    initAdCreation(formDiv, adsDiv);
    initEditButtons(formDiv, adsDiv);
    initChangeButtons(formDiv, adsDiv);
    initCancelProposalButtons();
    initIncomeCancelProposalButtons();
    initAcceptProposalButtons();
    initFilterHandlers();
}

const initIncomeCancelProposalButtons = () => {
    document.querySelectorAll('.proposal-income-cancel-button').forEach(button =>
        button.addEventListener('click', () => {
            ajaxRequest(`/ads/proposal/manage/${button.dataset.adId}/cancel/`, 'POST')
                .then(data => {
                    if (data.status === 'rejected') {
                        console.log('Входящая заявка отменена');
                        loadContent(1);
                    } else {
                        console.error('Ошибка:', data.message);
                    }
                });
        })
    );
};

// --- Инициализация кнопок принятия входящих заявок ---
const initAcceptProposalButtons = () => {
    document.querySelectorAll('.proposal-accept-button').forEach(button =>
        button.addEventListener('click', () => {
            ajaxRequest(`/ads/proposal/manage/${button.dataset.adId}/accept/`, 'POST')
                .then(data => {
                    if (data.status === 'accepted') {
                        console.log('Заявка принята');
                        loadContent(1);
                    } else {
                        console.error('Ошибка:', data.message);
                    }
                });
        })
    );
};


// --- Инициализация создания объявлений ---
const initAdCreation = (formDiv, adsDiv) => {
    const createAdBtn = document.getElementById('create-ad');

    createAdBtn.addEventListener('click', () => {
        ajaxRequest('/ads/manage/')
            .then(html => {
                formDiv.innerHTML = html;
                initSurveyFormJS(adsDiv);
            });
    });
};

// --- Инициализация кнопок редактирования ---
const initEditButtons = (formDiv, adsDiv) => {
    document.querySelectorAll('.edit-button').forEach(button =>
        button.addEventListener('click', () => {
            ajaxRequest(`/ads/manage/${button.dataset.adId}/`)
                .then(html => {
                    formDiv.innerHTML = html;
                    initSurveyFormJS(adsDiv);
                });
        })
    );
};

// --- Инициализация кнопок обмена ---
const initChangeButtons = (formDiv, adsDiv) => {
    document.querySelectorAll('.change-button').forEach(button =>
        button.addEventListener('click', () => {
            ajaxRequest(`/ads/proposal/manage/?receiver=${button.dataset.adId}`)
                .then(html => {
                    formDiv.innerHTML = html;
                    initSurveyFormJS(adsDiv);
                });
        })
    );
};

// --- Инициализация отмены заявок ---
const initCancelProposalButtons = () => {
    document.querySelectorAll('.proposal-cancel-button').forEach(button =>
        button.addEventListener('click', () => {
            ajaxRequest(`/ads/proposal/manage/${button.dataset.adId}/`, 'DELETE')
                .then(data => {
                    if (data.status === 'deleted') {
                        console.log('Заявка удалена');
                        loadContent(1);
                    } else {
                        console.error('Ошибка:', data.message);
                    }
                });
        })
    );
};

// --- Инициализация фильтра объявлений ---
const initFilterHandlers = () => {
    const setFiltersButton = document.getElementById('set-filters-button');
    const searchInput = document.querySelector('.filter-form input[placeholder="Поиск"]');
    const select = document.getElementById('category-select');
    const filterViewDiv = document.getElementById('filters-view-div');
    const adsViewDiv = document.getElementById('ads-view-div');

    setFiltersButton.addEventListener('click', () => {
        const params = new URLSearchParams();

        if (select.value && select.value !== 'all') params.append('category', select.value);
        if (searchInput.value) params.append('search', searchInput.value);

        ajaxRequest(`/ads/?${params.toString()}`)
            .then(html => {
                const newAdsList = new DOMParser().parseFromString(html, 'text/html').querySelector('.ads-list');
                document.querySelector('.ads-list').innerHTML = newAdsList.innerHTML;
                toggleVisibility(null, filterViewDiv);
                toggleBlur(null, adsViewDiv);
            });
    });

    const filterButton = document.getElementById('filter-button');
    const filterCrossImg = document.getElementById('filter-cross-img');

    filterButton.addEventListener('click', () => {
        toggleVisibility(filterViewDiv, null);
        toggleBlur(adsViewDiv, null);
    });

    filterCrossImg.addEventListener('click', () => {
        toggleVisibility(null, filterViewDiv);
        toggleBlur(null, adsViewDiv);
    });
};

// --- Инициализация форм объявлений и заявок ---
function initSurveyFormJS(backPage) {
    const formDiv = document.getElementById('form-div');
    const form = formDiv.querySelector('#ad-form, #proposal-form');

    toggleVisibility(formDiv, null);
    toggleBlur(backPage, null);

    formDiv.querySelector('#cross-img').addEventListener('click', () => {
        toggleVisibility(null, formDiv);
        toggleBlur(null, backPage);
    });

    iphoneFix(Array.from(form.querySelectorAll('input, textarea, select')));

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        ajaxRequest(form.action, 'POST', new FormData(form))
            .then(data => {
                if (data.status === 'ok') {
                    console.log('Форма сохранена');
                    toggleVisibility(null, formDiv);
                    toggleBlur(null, backPage);
                    loadContent(1);
                } else {
                    formDiv.innerHTML = data.form_html;
                    initSurveyFormJS(backPage);
                }
            });
    });

    const deleteBtn = form.querySelector('.cancel-ad-button');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            ajaxRequest(`/ads/manage/${deleteBtn.dataset.adId}/`, 'DELETE')
                .then(data => {
                    if (data.status === 'deleted') {
                        console.log('Объявление удалено');
                        toggleVisibility(null, formDiv);
                        toggleBlur(null, backPage);
                        loadContent(1);
                    } else {
                        console.error('Ошибка:', data.message);
                    }
                });
        });
    }
}

// --- Переключение активного состояния ---
function initToggleBorder(selector) {
    document.querySelector(selector).addEventListener('click', (e) => {
        if (!e.target.matches('.select-with-border')) return;

        document.querySelectorAll(`${selector} .select-with-border`)
            .forEach(el => el.classList.toggle('active-border', el === e.target));

        const targetClass = e.target.dataset.showBlock;
        document.querySelectorAll('[data-toggle-block]')
            .forEach(block => block.classList.toggle('hidden', !block.classList.contains(targetClass)));
    });
}
