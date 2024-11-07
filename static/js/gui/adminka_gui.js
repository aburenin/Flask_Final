import {element} from "/static/js/support_functions.js"
// import {writeAlert} from "./gui_alert"


const projectName = window.location.pathname.split('/')[2]


export function createNewProjectLine(client) {
    const tableBody = document.querySelector('.table-body')

    const projectDiv = element('div', ['kunden-table'])
    projectDiv.setAttribute('data-clientID', client.id); // Используем ID клиента как уникальный идентификатор

    const clientName = element('div', ['client-name'])
    clientName.innerText = client.name

    const pathSize = element('div', ['path-size'])
    pathSize.innerText = client.path_size

    const project = element('div', ['client'])

    project.appendChild(clientName)
    project.appendChild(pathSize)

    // const projectICO = element('img', ['projects-table__item-cover', 'desktop'])
    // projectICO.src = window.location.origin + '/' + client.img_url

    const projectICO = element('div', ['projects-table__item-cover', 'desktop'])
    projectICO.style.backgroundImage = `url('${window.location.origin}/${client.img_url}')`;


    const projectInfo = element('div', ['kunden-info', 'table-block'])

    projectInfo.appendChild(projectICO)
    projectInfo.appendChild(project)

    projectDiv.appendChild(projectInfo)


    const more = element('span', ['more'])
    more.innerText = client.fotos_list
    const fotosList = element('div', ['fotos-list', 'table-block'])
    fotosList.appendChild(more)
    fotosList.setAttribute('_', "on click toggle .more")

    projectDiv.appendChild(fotosList)

    const shootingDate = element('div', ['shooting-date', 'table-block', 'desktop'])
    shootingDate.innerText = client.date.split('T')[0].split('-').reverse().join('-')

    projectDiv.appendChild(shootingDate)
    const projectOptions = element('div', ['kunden-options', 'table-block'])
    projectOptions.innerHTML = `<i class="fa-solid fa-gear fa-lg" style="color: #bfbfbf;"></i>
                <i class="fa-solid fa-trash-can fa-lg" style="color: #d60000;"
                   hx-get="/success/" hx-vals='{"text": "Точно удалить проект ?", "action": "project_delete", "clientID": "${client.id}"}'  
                   hx-target="body" hx-swap="beforeend"></i>`

    projectDiv.appendChild(projectOptions)

    tableBody.appendChild(projectDiv)

    _hyperscript.processNode(fotosList)
    htmx.process(projectOptions)

    return projectDiv
}


export async function modalNewClientBuilder() {
    const popupWindow = document.querySelector('#modalNewClient')

    const popupMainBody = element('div', ['modal-dialog']);


    const formNewProject = element('form', ['modal-content'])
    formNewProject.id = 'formNewProject'
    formNewProject.method = 'POST'

    const popupHeader = element('div', ['modal-header']);
    popupHeader.innerHTML = `<span>Добавление нового проекта</span>
                             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                             _="on click transition .modal-dialog's opacity to 0 over 150ms then remove .show from #modalNewClient remove event.target.closest('.modal-dialog')">
                             <i class="fa-solid fa-xmark fa-xl" aria-hidden="true"></i></button>`


    const popupBody = element('div', ['modal-body']);

    const projectName = document.createElement('div')
    projectName.classList.add('form-floating')
    const inputProjectName = document.createElement('input')
    inputProjectName.type = 'text'
    inputProjectName.classList.add('form-control')
    inputProjectName.id = 'ProjectName'
    inputProjectName.name = 'projectName'
    inputProjectName.placeholder = 'Название проекта'
    inputProjectName.required = 'true'
    inputProjectName.autocomplete = 'off'

    projectName.appendChild(inputProjectName)

    const projectPassw = document.createElement('div')
    projectPassw.classList.add('form-floating')
    const inputProjectPassw = document.createElement('input')
    inputProjectPassw.type = 'text'
    inputProjectPassw.classList.add('form-control')
    inputProjectPassw.id = 'ProjectPassword'
    inputProjectPassw.name = 'projectPassword'
    inputProjectPassw.placeholder = 'Пароль'
    inputProjectPassw.required = 'true'
    inputProjectPassw.autocomplete = 'off'

    projectPassw.appendChild(inputProjectPassw)

    const projectDate = element('div', ['projectDate', 'form-floating'])
    const inputDate = document.createElement('input')
    inputDate.type = 'text'
    inputDate.name = 'projectDate'
    inputDate.id = 'projectDate'
    inputDate.classList.add('date-input')
    inputDate.placeholder = 'Дата съемки'
    inputDate.required = 'true'
    inputDate.autocomplete = 'off'

// Создаём контейнер для иконки
    const calendarIcon = element('i', ['fa-regular', 'fa-calendar-days', 'fa-xl']);
    calendarIcon.setAttribute('aria-hidden', 'true');

    projectDate.appendChild(calendarIcon)
    projectDate.appendChild(inputDate)

    popupBody.appendChild(projectName)
    popupBody.appendChild(projectPassw)
    popupBody.appendChild(projectDate)

    const popupFooter = element('div', ['modal-footer']);

    const btnSubmit = document.createElement('button')
    btnSubmit.type = 'submit'
    btnSubmit.classList.add('custom-btn')
    btnSubmit.classList.add('submit-btn')
    btnSubmit.innerText = 'Создать'
    const btnReject = document.createElement('button')
    btnReject.type = 'reset'
    btnReject.classList.add('custom-btn')
    btnReject.classList.add('reject-btn')
    btnReject.innerText = 'Отмена'
    btnReject.setAttribute('_', "on click transition .modal-dialog's opacity to 0 and transform scale to 0 over 150ms then remove .show from #modalNewClient remove event.target.closest('.modal-dialog')")

    popupFooter.appendChild(btnReject)
    popupFooter.appendChild(btnSubmit)


    formNewProject.appendChild(popupBody)
    formNewProject.appendChild(popupFooter)

    popupMainBody.appendChild(popupHeader)
    popupMainBody.appendChild(formNewProject)
    popupWindow.appendChild(popupMainBody)

    popupWindow.classList.add('show')

    _hyperscript.processNode(modalNewClient)
    // htmx.process(modalNewClient)
    return popupWindow
}

export async function changePasswordBuilder(projectName) {
    const popupWindow = document.querySelector('#modalChangePassw')

    const popupMainBody = element('div', ['modal-dialog']);

    const popupHeader = element('div', ['modal-header']);
    popupHeader.innerHTML = `<span>Изменение пароля для ${projectName}</span>
                             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                             _="on click transition .modal-dialog's opacity to 0 over 150ms then remove .show from #modalChangePassw remove event.target.closest('.modal-dialog')">
                             <i class="fa-solid fa-xmark fa-xl" aria-hidden="true"></i></button>`


    const formChangePassw = element('form', ['modal-content'])
    formChangePassw.id = 'formNewProject'
    formChangePassw.method = 'POST'


    const projectPassw = document.createElement('div')
    projectPassw.classList.add('form-floating')

    const inputProjectPassw = document.createElement('input')
    inputProjectPassw.type = 'text'
    inputProjectPassw.classList.add('form-control')
    inputProjectPassw.id = 'ProjectPassword'
    inputProjectPassw.name = 'projectPassword'
    inputProjectPassw.placeholder = 'Новый пароль'
    inputProjectPassw.required = 'true'
    inputProjectPassw.autocomplete = 'off'

    projectPassw.appendChild(inputProjectPassw)

    formChangePassw.appendChild(projectPassw)

    const popupFooter = element('div', ['modal-footer']);

    const btnSubmit = document.createElement('button')
    btnSubmit.type = 'submit'
    btnSubmit.classList.add('custom-btn')
    btnSubmit.classList.add('submit-btn')
    btnSubmit.innerText = 'Применить'
    const btnReject = document.createElement('button')
    btnReject.type = 'reset'
    btnReject.classList.add('custom-btn')
    btnReject.classList.add('reject-btn')
    btnReject.innerText = 'Отмена'
    btnReject.setAttribute('_', "on click transition .modal-dialog's opacity to 0 and transform scale to 0 over 150ms then remove .show from #modalChangePassw remove event.target.closest('.modal-dialog')")

    popupFooter.appendChild(btnReject)
    popupFooter.appendChild(btnSubmit)


    formChangePassw.appendChild(popupFooter)

    popupMainBody.appendChild(popupHeader)
    popupMainBody.appendChild(formChangePassw)
    popupWindow.appendChild(popupMainBody)

    popupWindow.classList.add('show')

    _hyperscript.processNode(modalChangePassw)
    // htmx.process(modalNewClient)
    return formChangePassw
}