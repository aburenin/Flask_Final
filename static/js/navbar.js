//===========================================
//👉👉👉        Mobile X             👈👈👈
//==================🔽🔽🔽🔽🔽🔽===========
const hamburger = document.getElementById('hamburger')
const navbar = document.querySelector('.navbar')
const dropdown = document.querySelector('.nav-item.dropdown')

hamburger.addEventListener('click', (e) => {
    if (hamburger.classList.contains('open')) {
        navbar.classList.remove('show')
        hamburger.classList.remove('open')
    } else {
        navbar.classList.add('show')
        hamburger.classList.add('open')
    }

})

dropdown.addEventListener('click', (e) => {
    const dropdownMenu = document.querySelector('.dropdown-menu')
    dropdownMenu.classList.toggle('show')
})
