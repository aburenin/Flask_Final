export const questions = async () => {
    try {
        const response = await fetch(window.location.pathname + '?action=getQuestions')

        if (!response.ok) {
            throw new Error('Сетевая ошибка при загрузке файла: ' + response.statusText)
        }

        const data = await response.json()

        const questionsArray = Object.keys(data).map(question => ({
            question: question,
            answer: data[question]
        }));

        return questionsArray
    } catch (error) {
        console.error('Ошибка:', error)
    }
}



