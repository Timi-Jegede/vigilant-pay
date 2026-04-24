const siteHamburgerButton = document.querySelector('#site-hamburger-button');
let state;

if (siteHamburgerButton) {
    siteHamburgerButton.addEventListener('click', () => {
        state = (state === null) ? 'collapsed' : (state === 'collapsed') ? 'expanded' : 'collapsed';

        const sideBar = document.querySelector('#sidebar');
        const main = document.querySelector('#main');
        const accountOverviewLink = document.querySelector('#account-overview');
        const securityLogLink = document.querySelector('#security-log');
        const textElem = document.createElement('span');
        const accountOverviewText = textElem.textContent = 'Account Overview';
        const securityLogText = textElem.textContent = 'Security Log';
        const accountOverviewIcon = `<svg id="account-overview-icon" class="w-10 h-10 text-site-background-color hover:text-site-primary-color" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                                    </svg>`;
        const securityLogIcon = `<svg class="w-10 h-10 text-site-background-color hover:text-site-primary-color" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                                </svg>`;

        const sideBarElems = {
            expanded: {
                icons: {
                    accountOverview: accountOverviewText,
                    securityLog: securityLogText
                },
                classes: {
                    widthClassSideBar: 'col-span-2',
                    widthClassMain: 'col-span-10',
                    backgroundClass: 'bg-site-primary-color' 
                }

            },
            collapsed: {
                icons: {
                    accountOverview: accountOverviewIcon,
                    securityLog: securityLogIcon
                },
                classes: {
                    widthClassSideBar: 'col-span-1',
                    widthClassMain: 'col-span-11',
                    backgroundClass: 'bg-white'
                }
            }
        }

        Object.entries(sideBarElems).forEach(([objState, value]) => {
            Object.keys(value).forEach((uiElem) => {
                const { accountOverview, securityLog, widthClassSideBar, 
                    widthClassMain, backgroundClass } = value[uiElem];
                const isActive = (objState === state);
                sideBar.classList.toggle(widthClassSideBar, isActive);
                sideBar.classList.toggle(backgroundClass, isActive);
                main.classList.toggle(widthClassMain, isActive);
            });
        });

        const { accountOverview, securityLog } = sideBarElems[state]['icons'];
        accountOverviewLink.innerHTML = accountOverview;
        securityLogLink.innerHTML = securityLog;
    });
}


const profileIcon = document.querySelector('#profile-icon');
const profileMenu = document.querySelector('#profile-menu');

if (profileIcon) {
    profileIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        profileMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!profileIcon.contains(e.target) && !profileMenu.contains(e.target)) {
            profileMenu.classList.add('hidden');
        }
    });
}





