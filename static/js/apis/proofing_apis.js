export const getAusgewaelteFotos = async () => {
    try {
        const response = await fetch(window.location.pathname + `?action=checkApprovedImages`, {
            method: 'GET'
        })

        if (!response.ok) {
            throw new Error('Network response was not ok')
        }

        const data = await response.json()
        return data
    } catch (error) {
        console.error('Ошибка:', error)
    }
}


export async function addFotoToDB(Data) {
    return await fetch(window.location.pathname + `?action=addToDB`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Data)
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


export async function delFotoFromDB(Data) {
    return await fetch(window.location.pathname + `?action=delFromDB`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Data)
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


export async function downloadGallery() {
    try {
        console.log('Start')
        const response = await fetch(window.location.pathname + '?action=download', {
            method: 'GET'
        })

        if (!response.ok) {
            throw new Error('Сетевая ошибка: ' + response.statusText)
        }
    
        console.log('Mitte')
        
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url

        a.download = 'gallery.zip'
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
        
        console.log('END')
    } catch (err) {
        console.error('Сетевая ошибка:', err)
        alert('Не удалось скачать файл: ' + err.message)
    }
}