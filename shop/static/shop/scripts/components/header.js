const initializeHeaderComponent = () => {

    const initializeNavigationModule = () => {
        
        const navigationMain = document.querySelector('.header-bottom-navigation');
        const navigationOther = document.querySelector('.header-top-ctas');

        if (!navigationMain || !navigationOther) return;

        const navigationMainAnchors = navigationMain.querySelectorAll('.anchor-button');
        const navigationOtherAnchors = navigationOther.querySelectorAll('.button-secondary');
        const navigationAnchors = [ ...navigationMainAnchors, ...navigationOtherAnchors ];
        const currentPage = window.location.pathname.replaceAll('/', '');

        navigationAnchors.forEach((navigationAnchor) => {

            if (navigationAnchor.matches('button'))
                return;

            const anchorPage = navigationAnchor.href.split('/').at(-1);

            navigationAnchor.classList.remove('active');

            if (anchorPage === currentPage)
                navigationAnchor.classList.add('active');

        });

    };

    const initializeDropdownModule = () => {

        const dropdownTrigger = document.querySelector('.dropdown-trigger');
        const dropdownMenu = document.querySelector('.dropdown-menu');
        
        if (dropdownTrigger && dropdownMenu) {
            dropdownTrigger.addEventListener('click', (e) => {
                e.stopPropagation();

                (dropdownMenu.getAttribute('data-open') === 'false')
                    ? dropdownMenu.setAttribute('data-open', 'true')
                    : dropdownMenu.setAttribute('data-open', 'false')
            });

            document.addEventListener('click', (e) => {
                if (!dropdownMenu.contains(e.target) && !dropdownTrigger.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                }
            });
        };
    };

    initializeNavigationModule();
    initializeDropdownModule();

};

export default initializeHeaderComponent;
