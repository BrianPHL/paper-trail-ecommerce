export const equalizeChildrenHeightInContainer = async (container) => {

    const containerChildren = container.querySelectorAll(':scope > *');
    const containerChildrenArray = Array.from(containerChildren);
    const isImageHidden = containerChildrenArray.filter(containerChild => window.getComputedStyle(containerChild).display === 'none').length === 1;

    if (containerChildren.length <= 0 || isImageHidden) return;

    containerChildren.forEach(containerChild => containerChild.style.height = 'auto');
    
    await new Promise(resolve => setTimeout(resolve, 5));

    const referenceHeight = containerChildren[0].offsetHeight;
    
    containerChildren.forEach(containerChild => {
    	if (containerChild.matches('.sign_in-form')) return;
    	containerChild.style.height = `${ referenceHeight }px`
    });
    
};

export const equalizeHeaderAndHeroSpacing = (header, hero, isLandingPage = false) => {

    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;
    const headerHeight = header.offsetHeight;

    header.style.height = `${ headerHeight }px`;
    hero.style.marginTop = `${ headerHeight }px`;
    
    if (viewportWidth <= 800 || viewportHeight <= 900 || !isLandingPage) {
        header.style.height = 'auto';
        hero.style.height = 'auto';
        return;
    };

    hero.style.height = `${ (viewportHeight - headerHeight) - (viewportHeight - headerHeight) * 0.20 }px`

};
