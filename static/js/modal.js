const impressumModal = document.getElementById('impressum')


document.querySelector('.impressum-footer').addEventListener('click', (e) => {
    if (e.target.closest('.modal')) {
        e.preventDefault()
        impressumModal.classList.add('show')
        document.body.classList.add('overhide')
        addCloseModalEvent()
    }
})

function addCloseModalEvent() {
    impressumModal.addEventListener('click', handleCloseModal)
}

function removeCloseModalEvent() {
    impressumModal.removeEventListener('click', handleCloseModal)
}

function handleCloseModal(e) {
    if (e.target.closest('.btn-close') || !e.target.closest('.modal-content')) {
        impressumModal.classList.remove('show')
        document.body.classList.remove('overhide')
        impressumModal.remove()
        removeCloseModalEvent()
    }
}
