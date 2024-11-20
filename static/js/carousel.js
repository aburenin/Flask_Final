
let nextImage = 0
const images = document.querySelectorAll('.slider img')
const slider = document.getElementById('carouselMobile')
let oldImage = 0
let isAnimating = false

const carouselMobile = () => {
    slider.addEventListener('click', (e) => {
        if (isAnimating) return
        let target
        if (e.target.closest('.next')) {
            target = 'next'
            nextImage = (nextImage + 1) % images.length;
        }
        if (e.target.closest('.prev')) {
            target = 'prev'
            nextImage = (nextImage - 1 + images.length) % images.length;
        }
        imagesControl(nextImage, target)
    })
}



const imagesControl = async (nextImage, target) => {
    if (oldImage !== nextImage) {
        isAnimating = true
        await new Promise((resolve) => {
            images[nextImage].classList.add('active')
            images[oldImage].style.opacity = '0'
            setTimeout(() => {
                images[nextImage].style.opacity = '1'
            }, 1)
            setTimeout(() => {
                resolve()
            }, 749)
        })
            .then(() => {
                isAnimating = false
                images[oldImage].classList.remove('active')
            })
    }
    oldImage = nextImage
}


document.addEventListener("DOMContentLoaded", function () {
    carouselMobile()
})