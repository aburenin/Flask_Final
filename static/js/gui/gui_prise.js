export async function addPriceTable(section, paket) {
    const priceCard = document.createElement('div')
    priceCard.classList.add('price-card')

    const cardHead = document.createElement('div')
    cardHead.classList.add('card-head')
    cardHead.innerHTML = `<h2>${paket.name}</h2>`

    priceCard.appendChild(cardHead)

    const cardPrice = document.createElement('div')
    cardPrice.classList.add('card__price')
    const spanPrise = document.createElement('span')
    spanPrise.innerText = 'eur'
    const pPrice = document.createElement('p')
    pPrice.innerText = paket.price
    cardPrice.appendChild(spanPrise)
    cardPrice.appendChild(pPrice)
    priceCard.appendChild(cardPrice)

    const cardBody = document.createElement('div')
    cardBody.classList.add('card-body')

    const ulServices = document.createElement('ul')
    ulServices.classList.add('services')

    paket.description.forEach((service) => {
        const liService = document.createElement('li')
        liService.classList.add('service')
        liService.innerHTML = `${service} <hr>`
        ulServices.appendChild(liService)
    })

    cardBody.appendChild(ulServices)
    priceCard.appendChild(cardBody)

    const cardFooter = document.createElement('div')
    cardFooter.classList.add('card-footer')

    const bookBtn = document.createElement('button')
    bookBtn.classList.add('book-btn')
    bookBtn.innerText = 'Jetzt buchen'
    bookBtn.addEventListener('click', () => {
        window.location.href = '/kontakt/'
    })


    cardFooter.appendChild(bookBtn)
    priceCard.appendChild(cardFooter)

    section.appendChild(priceCard)
}
