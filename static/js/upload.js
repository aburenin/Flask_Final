import {reload_page_without_cache} from "/static/js/admin_project.js";

const dropArea = document.querySelector('.drop-section');
const listSection = document.querySelector('.list-section');
const listContainer = document.querySelector('.list');
const fileSelector = document.querySelector('.file-selector');
const fileSelectorInput = document.querySelector('.file-selector-input');

// Загрузка файлов через кнопку
fileSelector.addEventListener('click', () => fileSelectorInput.click());
fileSelectorInput.addEventListener('change', async () => {
    const promises = Array.from(fileSelectorInput.files).map(file => {
        if (typeValidation(file.type)) {
            return uploadFile(file);
        }
    }).filter(Boolean);
    finishPromises(promises);
});

// Когда файл находится над зоной загрузки
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    [...e.dataTransfer.items].forEach((item) => {
        if (typeValidation(item.type)) {
            dropArea.classList.add('drag-over-effect');
        }
    });
});

// Когда файл уходит из зоны загрузки
dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('drag-over-effect');
});

// Когда файл сбрасывают в зону загрузки
dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('drag-over-effect');

    const promises = [];
    if (e.dataTransfer.items) {
        [...e.dataTransfer.items].forEach((item) => {
            if (item.kind === 'file') {
                const file = item.getAsFile();
                if (typeValidation(file.type)) {
                    promises.push(uploadFile(file)); // Добавляем загрузку в массив промисов
                }
            }
        });
    } else {
        [...e.dataTransfer.files].forEach((file) => {
            if (typeValidation(file.type)) {
                promises.push(uploadFile(file));
            }
        });
    }

    // Ждем завершения всех загрузок перед дальнейшими действиями
    finishPromises(promises);
});

// Проверка типа файла
function typeValidation(type) {
    const splitType = type.split('/')[0];
    return type === 'application/pdf' || splitType === 'image';
}

// Функция загрузки файла
async function uploadFile(file) {
    listSection.classList.add('show');
    let li = document.createElement('li');
    li.classList.add('in-prog');
    li.innerHTML = `
        <div class="col">
            <img src="/static/img/${iconSelector(file.type)}" alt="">
        </div>
        <div class="col">
            <div class="file-name">
                <div class="name">${file.name}</div>
                <span>0%</span>
            </div>
            <div class="file-progress">
                <span></span>
            </div>
            <div class="file-size">${(file.size / (1024 * 1024)).toFixed(2)} MB</div>
        </div>
        <div class="col">
            <svg xmlns="http://www.w3.org/2000/svg" class="cross" height="20px" viewBox="0 -960 960 960" width="20px" fill="#183153">
                <path d="m291-240-51-51 189-189-189-189 51-51 189 189 189-189 51 51-189 189 189 189-51 51-189-189-189 189Z"/>
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" class="tick" height="20px" viewBox="0 -960 960 960" width="20px" fill="#2a951a">
                <path d="M384-357 192-549l51-51 141 141 333-333 51 51-384 384ZM240-192v-72h480v72H240Z"/>
            </svg>
        </div>`;
    listContainer.prepend(li);

    return new Promise((resolve, reject) => {
        let http = new XMLHttpRequest();
        let data = new FormData();
        const projectName = document.getElementById('uploadWindow').getAttribute('data-projectname');
        data.append('file', file);

        http.onload = () => {
            li.classList.add('complete');
            li.classList.remove('in-prog');
        };

        http.upload.onprogress = (e) => {
            let percent_complete = (e.loaded / e.total) * 100;
            li.querySelectorAll('span')[0].innerHTML = Math.round(percent_complete) + '%';
            li.querySelectorAll('span')[1].style.width = percent_complete + '%';
        };

        http.onreadystatechange = function () {
            if (http.readyState === XMLHttpRequest.DONE) {
                if (http.status === 200) {
                    resolve(http.responseText); // Успешная загрузка
                } else {
                    li.classList.add('error');
                    li.querySelector('.file-name span').innerText = 'Ошибка';
                    reject(new Error(`Ошибка: ${http.status} ${http.statusText}`));
                }
            }
        };

        http.open('POST', `${window.location.pathname}?projectName=${projectName}&action=addFotoToProject`, true);
        http.send(data);
    });
}

// Выбор иконки для файла
function iconSelector(type) {
    let splitType = (type.split('/')[0] === 'application') ? type.split('/')[1] : type.split('/')[0];
    return splitType + '.svg';
}

// Ожидание завершения всех загрузок
async function finishPromises(promises) {
    Promise.all(promises)
        .then(responses => {
            console.log('Все файлы загружены:', responses);
            reload_page_without_cache(2000); // Перезагрузка после завершения всех загрузок
        })
        .catch(error => {
            console.error('Ошибка при загрузке одного или нескольких файлов:', error);
        });
}