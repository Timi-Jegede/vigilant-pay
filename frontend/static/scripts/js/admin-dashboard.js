var selector = document.getElementById('admin-selector');
var selectorMenu = document.getElementById('admin-selector-menu');
function toggleSelectorMenu() {
    var isClosed = selectorMenu.classList.contains('opacity-0');
    if (isClosed) {
        selectorMenu.classList.remove('hidden');
        requestAnimationFrame(function () {
            selectorMenu.classList.remove('opacity-0', 'scale-95', '-translate-y-2');
            selectorMenu.classList.add('opacity-100', 'scale-100', 'translate-y-0');
        });
    }
    else {
        selectorMenu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
        selectorMenu.classList.add('opacity-0', 'scale-95', '-translate-y-2');
        setTimeout(function () {
            if (selectorMenu.classList.contains('opacity-0')) {
                selectorMenu.classList.add('hidden');
            }
        }, 200);
    }
}
selector.addEventListener('click', toggleSelectorMenu);
document.addEventListener('click', function (e) {
    var clickedElement = e.target;
    var insideMenu = selectorMenu.contains(clickedElement);
    var insideButton = selector.contains(clickedElement);
    if (!insideMenu && !insideButton) {
        if (!selectorMenu.classList.contains('hidden')) {
            selectorMenu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
            selectorMenu.classList.add('opacity-0', 'scale-95', '-translate-y-2');
            setTimeout(function () {
                if (selectorMenu.classList.contains('opacity-0')) {
                    selectorMenu.classList.add('hidden');
                }
            }, 200);
        }
    }
});
