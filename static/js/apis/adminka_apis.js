// export const hostname = window.location.hostname + ':5000'

export async function loadClients(ClientIndex) {
    // return await fetch(window.location.origin + `/api/clients?lastindex=${encodeURIComponent(ClientIndex)}`)
    return await fetch(window.location.pathname + `?action=getClients&lastindex=${encodeURIComponent(ClientIndex)}`, {
        method: 'POST'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.length < 10) document.querySelector('#LoadMoreProjects').remove()
            return data
        })
        .catch(error => {
            console.error('Ошибка:', error)
        })
}


export async function addNewProject(formData) {
    return await fetch(window.location.pathname + `?action=addNew`, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка: ' + response.statusText);
            }
            return response.json()
        })
        .catch(err => {
            throw new Error('Сетевая ошибка: ' + err);
        })
}


export async function changePassw(formData) {
    return await fetch(window.location.pathname + `?action=chngPassw`, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка: ' + response.statusText);
            }
            return response.json()
        })
        .catch(err => {
            throw new Error('Сетевая ошибка: ' + err);
        })
}


export async function clear_client_gallery(projectName) {
    return await fetch(window.location.pathname + `?projectName=${projectName}&action=clearGallery`, {
        method: 'POST'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка: ' + response.statusText);
            }
            return response.json()
        })
        .catch(err => {
            throw new Error('Сетевая ошибка: ' + err)
        })
}


export async function delete_image_from_gallery(projectName, fileName) {
    // return await fetch(window.location.pathname + `?projectName=${projectName}&fileName=${fileName}`, {
    return await fetch(window.location.pathname, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({action: 'delFoto',  projectName: projectName, fileName: fileName})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка: ' + response.statusText);
            }
            // return response.json()
            return 'success'
        })
        .catch(err => {
            throw new Error('Сетевая ошибка: ' + err)
        })
}