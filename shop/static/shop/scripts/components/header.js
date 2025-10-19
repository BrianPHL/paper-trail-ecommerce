const initializeHeaderComponent = () => {

    const navigationMain = document.querySelector('.header-bottom-navigation');
    const navigationOther = document.querySelector('.header-top-ctas');

    if (!navigationMain || !navigationOther) return;

    const navigationMainAnchors = navigationMain.querySelectorAll('.anchor-button');
    const navigationOtherAnchors = navigationOther.querySelectorAll('.button-secondary');
    const navigationAnchors = [ ...navigationMainAnchors, ...navigationOtherAnchors ];
    const currentPage = window.location.pathname.replaceAll('/', '');

    navigationAnchors.forEach((navigationAnchor) => {
        
        const anchorPage = navigationAnchor.href.split('/').at(-1);

        navigationAnchor.classList.remove('active');
        
        if (anchorPage === currentPage)
            navigationAnchor.classList.add('active');

    });

};

export default initializeHeaderComponent;
