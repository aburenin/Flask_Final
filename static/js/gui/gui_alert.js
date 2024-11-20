export function writeAlert(action, text) {
        const alertWrap = document.createElement('div')
        alertWrap.classList.add('alert-wrapper')
        alertWrap.id = 'alert'
        alertWrap.setAttribute('_', "on click if event.target.closest('.alert') is null then transition opacity to 0 over 150ms then remove me")


        const alert = document.createElement('div')
        alert.classList.add('alert', `${action}`)

        const p = document.createElement('p')
        p.classList.add('text-alert')
        p.innerText = `${text}`

        const okButton = document.createElement('button')
        okButton.classList.add('ok')
        okButton.setAttribute('_', "on click transition #alert's opacity to 0 over 150ms then remove #alert");
        okButton.innerText = 'OK'

        alert.appendChild(p)
        alert.appendChild(okButton)

        alertWrap.appendChild(alert)

        document.body.appendChild(alertWrap)

        _hyperscript.processNode(alertWrap)
    }