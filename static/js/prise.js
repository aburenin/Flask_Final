import {addPriceTable} from "./gui/gui_prise.js"
import {prices} from "./apis/price_api.js"

const priceTable = document.querySelector('.price-table')

prices().then(data => {
    data.forEach((item) => {
        addPriceTable(priceTable, item)
    })
})