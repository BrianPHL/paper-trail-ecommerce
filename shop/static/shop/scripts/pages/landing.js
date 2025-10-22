import * as themeUtilities from "../utils/theme.js";
import * as paginationUtilities from "../utils/pagination.js";
import * as responsiveUtilities from "../utils/responsive.js";

const initializeLandingPage = () => {

    if (window.location.pathname !== '/') return;

    const themeSwitchBtns = document.querySelectorAll('.theme-switcher-btn');
    const logos = document.querySelectorAll('.logo');
    const hero = document.querySelector('#hero');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        const mediaQuery = window.matchMedia('(max-width: 1500px');

        themeUtilities.getTheme((theme) => {

            themeUtilities.setTheme(theme);

            logos.forEach(logo => logo.src = `/static/shop/images/logo-${ theme }.png`)

            if (mediaQuery.matches)
                hero.style.backgroundImage = `url(/static/shop/images/hero-${ theme }.jpg)`;

            mediaQuery.addEventListener('change', (event) => {
                if (event.matches) {
                    hero.style.backgroundImage = `url(/static/shop/images/hero-${ theme }.jpg)`;
                } else {
                    hero.style.backgroundImage = ``;
                }
            }) 

            htmlElement.setAttribute('data-theme', theme);

        });

    };

    const initializePageLayoutHandling = () => {

        const header = document.querySelector('.header');
        const hero = document.querySelector('.landing-container');

        window.addEventListener('resize', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, true));
        window.addEventListener('load', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, true));

    };

    const initializeSectionsPaginationHandling = () => {

        const featured = document.querySelector('.featured_products-container');
        const bestsellers = document.querySelector('.bestsellers-container');
        const newArrivals = document.querySelector('.new_arrivals-container');

        if (featured)
            paginationUtilities.handleHorizontalPagination(featured);

        if (bestsellers)
            paginationUtilities.handleHorizontalPagination(bestsellers);

        if (newArrivals)
            paginationUtilities.handleHorizontalPagination(newArrivals);

    };

    themeSwitchBtns.forEach(themeSwitchBtn => themeSwitchBtn.addEventListener('click', () => {
        
        themeUtilities.getTheme((callback) => {

            const alternateTheme =
            (callback === 'light')
            ? 'dark'
            : 'light'

            themeSwitchBtn.innerHTML=
            `
                <i class="fa-solid ${ alternateTheme === 'light' ? 'fa-moon' : 'fa-sun' }"></i>
            `

            themeUtilities.setTheme(alternateTheme);
            initializePageTheme();

        });

    }))

    initializePageTheme();
    initializePageLayoutHandling();
    initializeSectionsPaginationHandling();

    console.log("Initialized landing page logic!");

};

export default initializeLandingPage;
