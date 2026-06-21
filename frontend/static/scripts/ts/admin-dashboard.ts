const selector = document.getElementById('admin-selector') as HTMLElement;
const selectorMenu = document.getElementById('admin-selector-menu') as HTMLElement;

function toggleSelectorMenu(): void {
    const isClosed = selectorMenu.classList.contains('opacity-0');
    
    if (isClosed) {
        selectorMenu.classList.remove('hidden');

        requestAnimationFrame(() => {
            selectorMenu.classList.remove('opacity-0', 'scale-95', '-translate-y-2');
            selectorMenu.classList.add('opacity-100', 'scale-100', 'translate-y-0');
        });
    } else {
        selectorMenu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
        selectorMenu.classList.add('opacity-0', 'scale-95', '-translate-y-2');

        setTimeout(() => {
            if (selectorMenu.classList.contains('opacity-0')) {
                selectorMenu.classList.add('hidden');
            }
        }, 200);
    }
}

selector.addEventListener('click', toggleSelectorMenu);

document.addEventListener('click', (e: MouseEvent) => {
    const clickedElement = e.target as Node;

    const insideMenu = selectorMenu.contains(clickedElement);
    const insideButton = selector.contains(clickedElement);

    if (!insideMenu && !insideButton) {
        if (!selectorMenu.classList.contains('hidden')) {
            selectorMenu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
            selectorMenu.classList.add('opacity-0', 'scale-95', '-translate-y-2');

            setTimeout(() => {
                if (selectorMenu.classList.contains('opacity-0')) {
                    selectorMenu.classList.add('hidden');
                }
            }, 200);
        }
    }
});