const lazyImageObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            const lazyImage = entry.target
            if (lazyImage.dataset.src) {
                lazyImage.src = lazyImage.dataset.src
            }
            if (lazyImage.dataset.srcset) {
                lazyImage.srcset = lazyImage.dataset.srcset
            }
            lazyImageObserver.unobserve(lazyImage)
        }
    })
}, {
    threshold: 0.2
});



// Инициализация IntersectionObserver
document.addEventListener("DOMContentLoaded", async function () {

    const lazyImages = document.querySelectorAll("img")
    lazyImages.forEach(function (lazyImage) {
        lazyImageObserver.observe(lazyImage)
    })

})

//
// document.addEventListener('click', e=> {
//     console.log(e.target)
// })