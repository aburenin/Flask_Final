import {clear_client_gallery, delete_image_from_gallery} from "/static/js/apis/adminka_apis.js"
import {writeAlert} from "/static/js/gui/gui_alert.js"
import {iso} from "/static/js/portfolio.js"

document.addEventListener('DOMContentLoaded', () => {

    const projectName = document.getElementById('uploadWindow').getAttribute('data-projectname')
    document.querySelector('.btn.clear-all').addEventListener('click', () => {
        clear_client_gallery(projectName)
            .then(response => {
                if (response.status === 'success') {
                    console.log(response)
                    writeAlert('success', "Все фотографии удалены из проекта!")
                    reload_page_without_cache(1000)
                }
            })
            .catch(err => {
                writeAlert('error', `${err}`)
            })
    })

    document.getElementById('gallery').addEventListener('click', async (event)=>{
        if (event.target.classList.contains('del-img')) {
            const fileName = event.target.closest('.grid-item').getAttribute('data-filename')
            const response = await delete_image_from_gallery(projectName, fileName)
            console.log(response)
            if (response === 'success') {event.target.closest('.grid-item').remove()}
            iso.arrange({filter: '*'})
        }
    })

    document.querySelectorAll('.proofing--footer').forEach(item=>{
        item.style.display = 'none'
    })
})

export function reload_page_without_cache (ms) {
    setTimeout(function () {
        location.reload(true);
    }, ms);
}