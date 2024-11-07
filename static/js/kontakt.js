import {writeAlert} from "./gui/gui_alert.js"


const contactForm = document.getElementById('contactForm')
const submitButton = document.querySelector('button[name=submitButton]')

const checkBtnActive = ()=> {
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

contactForm.addEventListener('change', (e)=>{
    checkBtnActive()
})

contactForm.addEventListener('submit', (e)=>{
    e.preventDefault()
    console.log('clicked_send_msg')
    let formData = new FormData(contactForm)
    const bodyMessage = `Vorname: ${formData.get('firstName')} <br>
                                        Nachname: ${formData.get('lastName')} <br>
                                        Phone: ${formData.get('phone')} <br>
                                        E-mail: ${formData.get('email')} <br>
                                        Fotoshooting Art: ${formData.get('inputGroupSelect01')} <br>
                                        Message: ${formData.get('message')}`
    console.log(bodyMessage)
    sendEmail(bodyMessage, contactForm)
})


function sendEmail(bodyMessage, form) {

    Email.send({
        SecureToken: "679b76ed-f23c-42da-9d67-1812a563b6ad",
        To: 'burenin.alexey@gmail.com',
        From: "info@fotosbaby.de",
        Subject: "Baby und Babybauch Fotografie | Burenina Veronika",
        Body: bodyMessage +
            "<hr>" +
            "<br>".repeat(100) +
            "<style> a {opacity: 0 !important; display: none !important; color: transparent !important} </style>" +
            "<style> div {display: none !important; height: 0!important} </style>" +
            "&#9759;".repeat(9) + 'Не трогать!' + "&#9759;".repeat(9)
    }).then(response => {
        if (response === 'OK') {
            form.reset()
            writeAlert('success', "Ihre Anfrage wurde versandt. Wir werden uns so schnell wie möglich mit Ihnen in Verbindung setzen.")
        }
        else {
            writeAlert('error', response)
        }
    })
}
