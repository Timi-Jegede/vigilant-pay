const elemHeight  = document.getElementById('check-height');
const elemWidth = document.getElementById('check-width');

if (elemHeight) {
    console.log('Height: ', elemHeight.offsetHeight, 'px');
}

if(elemWidth) {
    console.log('Width: ', elemWidth.offsetWidth, 'px');
}

// console.log(window.innerHeight + ' px');