import * as themeUtilities from "../utils/theme.js";
import * as paginationUtilities from "../utils/pagination.js";
import * as responsiveUtilities from "../utils/responsive.js";

const initializeCartPage = () => {

    if (window.location.pathname !== '/cart/') return;

    const themeSwitchBtns = document.querySelectorAll('.theme-switcher-btn');
    const logos = document.querySelectorAll('.logo');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        themeUtilities.getTheme((theme) => {

            themeUtilities.setTheme(theme);

            logos.forEach(logo => logo.src = `/static/shop/images/logo-${ theme }.png`)

            htmlElement.setAttribute('data-theme', theme);

        });

    };

    const initializeHeroHandling = () => {

        const header = document.querySelector('.header');
        const hero = document.querySelector('.cart');

        window.addEventListener('resize', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, true));
        window.addEventListener('load', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, true));

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
    initializeHeroHandling();

    console.log("Initialized cart page logic!");

};

export default initializeCartPage;
