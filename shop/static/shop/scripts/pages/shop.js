import * as themeUtilities from "../utils/theme.js";
import * as responsiveUtilities from "../utils/responsive.js";

const initializeShopPage = () => {

    if (window.location.pathname !== '/shop/') return;

    const logos = document.querySelectorAll('.logo');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

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
        const hero = document.querySelector('.shop-wrapper');

        window.addEventListener('resize', () =>  responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));
        window.addEventListener('load', () =>  responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));

    };

    const initializeAutomaticFiltering = () => {
        const sidebarForm = document.querySelector('.shop-sidebar form');
        const modalForm = document.querySelector('.modal form');

        const setupAutoSubmit = (form) => {
            if (!form) return;

            const sortByRadios = form.querySelectorAll('input[name="sort_by"]');
            const categoryCheckboxes = form.querySelectorAll('input[name="categories"]');

            sortByRadios.forEach(radio => {
                radio.addEventListener('change', () => {
                    form.submit();
                });
            });

            categoryCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    form.submit();
                });
            });
        };

        setupAutoSubmit(sidebarForm);
        setupAutoSubmit(modalForm);
    };

    initializePageLayoutHandling();
    initializePageTheme();
    initializePageThemeHandling();
    initializeAutomaticFiltering();

    console.log("Initialized shop page logic!");

};

export default initializeShopPage;
