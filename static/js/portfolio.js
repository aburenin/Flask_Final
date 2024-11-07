import PhotoSwipeLightbox from '../libs/PhotoSwipe/photoswipe-lightbox.esm.min.js'
// import Isotope from '../libs/Isotope/isotope.pkgd.min.js'
import '../libs/Isotope/isotope.pkgd.min.js'

// export async function isoStart() {
let grid = document.querySelector('.grid');
export let iso = new Isotope(grid, {
    itemSelector: '.grid-item',
    percentPosition: true,
    layoutMode: 'masonry',
    transitionDuration: '1s',
})
// }

const lightbox = new PhotoSwipeLightbox({
    gallery: '.grid',
    children: '[data-pswp]',
    pswpModule: () => import('../libs/PhotoSwipe/photoswipe.esm.min.js'),
    loop: false,
    preloaderDelay: 0,
    preload: [1, 4],
    padding: {top: 20, bottom: 40},
})

if (window.location.pathname.includes('client')) {
    lightbox.on('uiRegister', function () {
        lightbox.pswp.ui.registerElement({
            name: 'custom-caption',
            order: 9,
            isButton: false,
            appendTo: 'root',
            html: 'Caption text',
            onInit: (el, pswp) => {
                lightbox.pswp.on('change', () => {
                    const currSlideElement = lightbox.pswp.currSlide.data.element;
                    let captionHTML = '';
                    if (currSlideElement) {
                        captionHTML = currSlideElement.querySelector('img').getAttribute('alt').split('.')[0];
                    }
                    el.innerHTML = captionHTML || '';
                });
            }
        });
    });
}

lightbox.on('close', () => {
    // Получаем индекс текущего слайда
    const index = lightbox.pswp.currIndex;

    // Получаем все элементы галереи
    const galleryItems = document.querySelectorAll('.grid a');

    if (galleryItems[index]) {
        // Получаем элемент галереи
        const element = galleryItems[index];

        // Прокручиваем страницу до позиции элемента с учетом отступа
        window.scrollTo({
            top: element.getBoundingClientRect().top + window.scrollY - 7,
            behavior: 'smooth'
        });
    }

    // if (galleryItems[index]) {
    //     // Прокручиваем страницу до соответствующего элемента
    //     galleryItems[index].scrollIntoView({ behavior: 'smooth', block: 'center' });
    // }
});

//-------------- change to HTMX
document.querySelectorAll('.grid-item').forEach(item => item.classList.add('show'))
// isoStart()
lightbox.init()