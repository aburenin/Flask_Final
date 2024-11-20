import {changePasswordBuilder, createNewProjectLine, modalNewClientBuilder} from '/static/js/gui/adminka_gui.js'
import {addNewProject, changePassw, loadClients} from '/static/js/apis/adminka_apis.js'
import {writeAlert} from '/static/js/gui/gui_alert.js'
import {Calendar} from '/static/js/extern/datepicker.js'

let ClientIndex = 1


async function updateClientTable(clients) {
    clients.forEach((client, index) => {
        const project = createNewProjectLine(client)
        ClientIndex += 1
        project.addEventListener('click', (e) => {
            if (e.target.closest('.fa-gear')) {
                changePasswordBuilder(project.querySelector('.client-name').innerText)
                    .then(form => {
                        form.addEventListener('submit', (e) => {
                            e.preventDefault()
                            const formChangePassw = new FormData(form)
                            formChangePassw.append('projectName', project.querySelector('.client-name').innerText)
                            changePassw(formChangePassw)
                                .then(data => {
                                    const modalChangePassw = document.getElementById('modalChangePassw')
                                    modalChangePassw.classList.remove('show')
                                    modalChangePassw.querySelector('.modal-dialog').remove()
                                    writeAlert(data.status, data.text)
                                })
                        })
                    })
            }
            if (e.target.closest('.kunden-info')) {
                const clientName = e.target.closest('.kunden-info').querySelector('.client-name').textContent;
                window.location.href = window.location.pathname + `?project=${clientName}`
            }
        })
    })
}


//
document.addEventListener("DOMContentLoaded", async function () {

    await loadClients(ClientIndex)
        .then(async (data) => {
            await updateClientTable(data)
        })

    document.querySelector('.add-project').addEventListener('click', async () => {
        const modalNewProject = document.getElementById('modalNewClient')

        await modalNewClientBuilder()

        const datepicker = new Calendar('.date-input')
        observAddNewClient()
    })

    if (document.querySelector('#LoadMoreProjects')) {
        document.querySelector('#LoadMoreProjects').addEventListener('click', async () => {
            await loadClients(ClientIndex)
                .then(async (data) => {
                    await updateClientTable(data)
                })
        })
    }
})

const observAddNewClient = () => {
    document.getElementById('formNewProject').addEventListener('submit', (event) => {
        event.preventDefault()
        const form = document.getElementById('formNewProject')
        const formNewProject = new FormData(form)
        addNewProject(formNewProject)
            .then(data => {
                const modalNewClient = document.getElementById('modalNewClient')
                modalNewClient.classList.remove('show')
                modalNewClient.querySelector('.modal-dialog').remove()
                writeAlert(data.status, data.text)
                reload_page_without_cache(1000)
            })
    })
}

export function reload_page_without_cache (ms) {
    setTimeout(function () {
        location.reload(true);
    }, ms);
}