export async function addPriceTable(section, paket) {
    console.log(paket)

    const priceCard = document.createElement('div')
    priceCard.classList.add('price-card')

    const cardHead = document.createElement('div')
    cardHead.classList.add('card-head')
    cardHead.innerHTML = `<h2>${paket.name}</h2>`

    priceCard.appendChild(cardHead)

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

    const priceDIV = document.createElement('div')
    priceDIV.classList.add('price-img')
    priceDIV.style.backgroundImage = `url("${window.location.origin}/static/media/preis/preis_pure.svg")`

    const priceSpan = document.createElement('span')
    priceSpan.classList.add('price--item')
    priceSpan.innerText = paket.price

    priceDIV.appendChild(priceSpan)
    
    cardFooter.appendChild(bookBtn)
    cardFooter.appendChild(priceDIV)
    priceCard.appendChild(cardFooter)

    section.appendChild(priceCard)
}
