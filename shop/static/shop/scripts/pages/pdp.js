import * as themeUtilities from "../utils/theme.js";
import * as paginationUtilities from "../utils/pagination.js";
import * as responsiveUtilities from "../utils/responsive.js";

const initializeProductDetailPage = () => {

    if (!window.location.pathname.startsWith('/product/')) return;

    const initializePageTheme = () => {

        const htmlElement = document.querySelector('html');
        const logos = document.querySelectorAll('.logo');

        themeUtilities.getTheme((theme) => {

            themeUtilities.setTheme(theme);

            logos.forEach(logo => logo.src = `/static/shop/images/logo-${ theme }.png`)

            htmlElement.setAttribute('data-theme', theme);

        });

    };

    const initializePageThemeHandling = () => {
        
        const themeSwitchBtns = document.querySelectorAll('.theme-switcher-btn');

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

        }));

    };

    const initializePageLayoutHandling = () => {

        const header = document.querySelector('.header');
        const hero = document.querySelector('.pdp-container');

        window.addEventListener('resize', () =>  responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));
        window.addEventListener('load', () =>  responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));

    };

    const initializeRelatedProductsPaginationHandling = () => {

        const relatedProducts = document.querySelector('.related_products-container');

        paginationUtilities.handleHorizontalPagination(relatedProducts);

    };

    initializePageLayoutHandling();
    initializePageTheme();
    initializePageThemeHandling();
    initializeRelatedProductsPaginationHandling();

    console.log("Initialized product detail page page logic!");

};

export default initializeProductDetailPage;
