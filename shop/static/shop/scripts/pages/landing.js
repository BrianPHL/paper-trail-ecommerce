import * as themeUtilities from "../utils/theme.js";
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

    const initializeHeroHandling = () => {

        window.addEventListener('resize', () => {

            const header = document.querySelector('.header');
            const hero = document.querySelector('.hero');
            
            responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero);

        });

        window.addEventListener('load', () => {

            const header = document.querySelector('.header');
            const hero = document.querySelector('.hero');

            responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero);

        });

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

    console.log("Initialized landing page logic!");

    initializePageTheme();
    initializeHeroHandling();

};

export default initializeLandingPage;
