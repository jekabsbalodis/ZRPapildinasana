const spinnerWrapperEl = document.querySelector('.spinner-wrapper');
const wholePageEl = document.querySelector('.whole-page');
function loading() {
    spinnerWrapperEl.style.opacity = '1';
    spinnerWrapperEl.style.display = 'unset';
    wholePageEl.style.transition = 'opacity 1s ease-in-out'
    wholePageEl.style.opacity = '0.5'
    wholePageEl.style.pointerEvents = 'none'
}
