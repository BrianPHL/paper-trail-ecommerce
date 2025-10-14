export const equalizeChildrenHeightInContainer = (container) => {

    const containerChildren = container.querySelectorAll(':scope > *');
    const containerChildrenArray = Array.from(containerChildren);
    const isImageHidden = containerChildrenArray.filter(containerChild => window.getComputedStyle(containerChild).display === 'none').length === 1;

    if (containerChildren.length <= 0 || isImageHidden) return;

    containerChildren.forEach(containerChild => containerChild.style.height = 'auto');

    const referenceHeight = containerChildren[0].offsetHeight;

    containerChildren.forEach(containerChild => containerChild.style.height = `${ referenceHeight }px`)

};

export const equalizeHeaderAndHeroSpacing = (header, hero) => {

    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;
    const headerHeight = header.offsetHeight;
    const heroHeight = hero.offsetHeight;

    console.log("Viewport height (in px): ", viewportHeight);
    console.log("Header height (in px): ", headerHeight);
    console.log("Hero height (in px): ", heroHeight);

    console.log(viewportHeight - headerHeight);

    header.style.height = `${ headerHeight }px`;
    hero.style.marginTop = `${ headerHeight }px`;
    
    if (viewportWidth <= 600) {
        header.style.height = 'auto';
        hero.style.height = 'auto';
        return;
    };

    hero.style.height = `${ (viewportHeight - headerHeight) - (viewportHeight - headerHeight) * 0.10  }px`

};
