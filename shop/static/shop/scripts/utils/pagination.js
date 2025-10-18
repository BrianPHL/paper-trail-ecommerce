export const handleHorizontalPagination = (container) => {

    const parsedContainer = container.className.replace('-container', '');
    const list = container.querySelector(`.${ parsedContainer }-list`);
    const pagination = container.querySelector(`.${ parsedContainer }-pagination`);
    const paginationPrev = pagination.querySelector(`.${ pagination.className }-prev`);
    const paginationNext = pagination.querySelector(`.${ pagination.className }-next`);

    const scrollAmount = () => {

        const card = list.querySelector('.product_card');

        if (!card) return 0;
        
        const cardWidth = card.offsetWidth;
        const gap = parseInt(getComputedStyle(list).gap) || 16;

        return cardWidth + gap;

    };

    const handlePaginationActionBtnStates = () => {
        
        const { scrollLeft, scrollWidth, clientWidth } = list;

        paginationPrev.disabled = scrollLeft <= 0;
        paginationNext.disabled = scrollLeft + clientWidth >= scrollWidth - 1;

    };

    const initializePaginationActions = () => {
        paginationPrev.addEventListener('click', () => {
            list.scrollBy({
                left: -scrollAmount(),
                behavior: 'smooth'
            });
        });

        paginationNext.addEventListener('click', () => {
            list.scrollBy({
                left: scrollAmount(),
                behavior: 'smooth'
            });
        });
    };

    initializePaginationActions();
    
    list.addEventListener('scroll', handlePaginationActionBtnStates);
    handlePaginationActionBtnStates();

};
