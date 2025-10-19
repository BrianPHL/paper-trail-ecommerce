const initializeFooterComponent = () => {

    const navigationMain = document.querySelector('.footer-middle-navigation_main');
    const navigationOther = document.querySelector('.footer-middle-navigation_other');
    const navigationMainAnchors = navigationMain.querySelectorAll('.anchor-button');
    const navigationOtherAnchors = navigationOther.querySelectorAll('.anchor-button');
    const navigationAnchors = [ ...navigationMainAnchors, ...navigationOtherAnchors ];
    const currentPage = window.location.pathname.replaceAll('/', '');

    navigationAnchors.forEach((navigationAnchor) => {
        
        const anchorPage = navigationAnchor.href.split('/').at(-1);

        navigationAnchor.classList.remove('active');
        
        if (anchorPage === currentPage)
            navigationAnchor.classList.add('active');

    });

};

export default initializeFooterComponent;
