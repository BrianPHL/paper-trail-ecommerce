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

        
        const dropdownWrappers = document.querySelectorAll('.user-dropdown');

        if (!dropdownWrappers || dropdownWrappers.length === 0) return;

        dropdownWrappers.forEach((wrapper) => {
            const trigger = wrapper.querySelector('.dropdown-trigger');
            const menu = wrapper.querySelector('.dropdown-menu');

            if (!trigger || !menu) return;

            
            if (!menu.hasAttribute('data-open')) menu.setAttribute('data-open', 'false');

            trigger.addEventListener('click', (e) => {
                e.stopPropagation();

                const isOpen = menu.getAttribute('data-open') === 'true';
                menu.setAttribute('data-open', isOpen ? 'false' : 'true');

                
                if (menu.style.display) menu.style.display = '';
            });

            
            document.addEventListener('click', (e) => {
                if (!menu.contains(e.target) && !trigger.contains(e.target)) {
                    menu.setAttribute('data-open', 'false');
                }
            });

            
            document.addEventListener('keyup', (e) => {
                if (e.key === 'Escape') {
                    menu.setAttribute('data-open', 'false');
                }
            });
        });

    };

    initializeNavigationModule();
    initializeDropdownModule();

};

export default initializeHeaderComponent;
