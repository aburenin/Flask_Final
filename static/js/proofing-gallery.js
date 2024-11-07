import {getAusgewaelteFotos, addFotoToDB, delFotoFromDB, downloadGallery} from '/static/js/apis/proofing_apis.js'
import {iso} from '/static/js/portfolio.js'


document.addEventListener('DOMContentLoaded', async () => {
    
    FilterObserver()
    const clientFotosList = await getAusgewaelteFotos()
    
    
    document.querySelectorAll('.grid-item').forEach(item=>{
        const heart = item.querySelector('.heart--selection')
        const fileName = item.getAttribute('data-filename')
        
        if (clientFotosList.includes(fileName)) {
            heart.classList.add('selected')
            item.classList.add('selected')
        }
        else { item.classList.add('rejected') }
        
        heart.addEventListener('click', ()=>{
            // selected image to gallery and write filename to DB
            if (heart.classList.contains('selected')) { 
                item.classList.add('selected')
                item.classList.remove('rejected')
                addFotoToDB({fileName: fileName})
            }
            // rejected image from gallery and remove filename from DB
            else {
                item.classList.add('rejected')
                item.classList.remove('selected')
                delFotoFromDB({fileName: fileName})
            }
        })
    })
    
    document.querySelector('.menu-filter').addEventListener('click', (e)=>{
        // console.log(e.target.closest('.filter--item').getAttribute('data-filter'))
        const type = e.target.closest('.filter--item').getAttribute('data-filter')
        console.log(type)
        iso.arrange({ filter: type })
    })
    
    document.querySelector('.download').addEventListener('click', (e)=> {
        e.preventDefault()
        downloadGallery()
    })
})


function FilterObserver() {
    const filterObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            const filter = document.querySelector('.menu-filter')
            if (entry.isIntersecting) {
                filter.classList.remove('hidden')
            } else filter.classList.add('hidden')
        })
    })
    filterObserver.observe(document.querySelector('.grid'))
}



