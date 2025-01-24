const lazyImageObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach(function (entry) {
        const lazyImage = entry.target;

        // Если элемент в зоне видимости
        if (entry.isIntersecting) {
            // Добавляем таймер для проверки, что элемент находится в зоне видимости достаточно долго
            lazyImage._visibleTimer = setTimeout(() => {
                if (lazyImage.dataset.src) {
                    lazyImage.src = lazyImage.dataset.src;
                }
                if (lazyImage.dataset.srcset) {
                    lazyImage.srcset = lazyImage.dataset.srcset;
                }

                // Убираем наблюдение за элементом
                lazyImageObserver.unobserve(lazyImage);
            }, 250); // Задержка 250 мс
        } else {
            // Если элемент покидает зону видимости до истечения времени, сбрасываем таймер
            clearTimeout(lazyImage._visibleTimer);
        }
    });
}, {
    threshold: [0, 0.25, 0.5, 0.75, 1.0] // Пороговые значения
    // threshold: 0.25 // Пороговые значения
});

// const lazyImageObserver = new IntersectionObserver(function (entries, observer) {
//     entries.forEach(function (entry) {
//         const lazyImage = entry.target;
//
//         // Если элемент в зоне видимости
//         if (entry.isIntersecting) {
//             if (lazyImage.dataset.src) {
//                 lazyImage.src = lazyImage.dataset.src;
//             }
//             if (lazyImage.dataset.srcset) {
//                 lazyImage.srcset = lazyImage.dataset.srcset;
//             }
//
//             // Убираем наблюдение за элементом
//             lazyImageObserver.unobserve(lazyImage);
//         }
//     });
// }, {
//     threshold: [0, 0.25, 0.5, 0.75, 1.0] // Пороговые значения
// });

// Инициализация IntersectionObserver
document.addEventListener("DOMContentLoaded", async function () {

    const lazyImages = document.querySelectorAll("img")
    lazyImages.forEach(function (lazyImage) {
        lazyImageObserver.observe(lazyImage)
    })

})
