export const portfolio_gallery = async () => {
    try {
        const response = await fetch(window.location.pathname + '?action=loadPictures')

        if (!response.ok) {
            throw new Error('Сетевая ошибка при загрузке файла: ' + response.statusText)
        }

        const data = await response.json()

        return data
    } catch (error) {
        console.error('Ошибка:', error)
    }
}



