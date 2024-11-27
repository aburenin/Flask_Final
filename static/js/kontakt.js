import {writeAlert} from "./gui/gui_alert.js"


const contactForm = document.getElementById('contactForm')
const submitButton = document.querySelector('button[name=submitButton]')

const checkBtnActive = () => {
    const textarea = contactForm.querySelector("textarea")
    const email = contactForm.querySelector("#email")
    const checkbox = contactForm.querySelector("#stimmung")
    const sendBtn = contactForm.querySelector('button')

    if (checkbox.checked && email.value !== '' && textarea.value !== '') {
        sendBtn.disabled = false
    } else {
        sendBtn.disabled = true
    }
}

contactForm.addEventListener('change', (e) => {
    checkBtnActive()
})


contactForm.addEventListener('submit', async (e) => {
    e.preventDefault()

    console.log("sent")

    let formData = new FormData(contactForm);

    const res = await fetch('/kontakt/', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                // Если проверка reCAPTCHA успешна, отправляем email
                contactForm.reset()
                writeAlert('success', "Ihre Anfrage wurde versandt. Wir werden uns so schnell wie möglich mit Ihnen in Verbindung setzen.")
            } else {
                alert("Verification failed. Please try again.")
            }
        })
        .catch(error => {
            console.error("Error:", error)
            alert("An error occurred. Please try again.")
        })
})