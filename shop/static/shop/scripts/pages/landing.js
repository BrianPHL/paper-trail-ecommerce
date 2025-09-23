import * as utilities from "../utils/theme.js";

const landingPageLogic = async () => {

    const themeSwitchBtn = document.querySelector('#theme-switcher-btn');
    const headerLogo = document.querySelector('#header-logo');
    const hero = document.querySelector('#hero');
    const heroImg = document.querySelector('#hero-img');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        const mediaQuery = window.matchMedia('(max-width: 1500px');

        utilities.getTheme((theme) => {

            utilities.setTheme(theme);

            headerLogo.src = `/static/shop/images/logo-${ theme }.png`

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

    themeSwitchBtn.addEventListener('click', () => {

        utilities.getTheme((callback) => {

            const alternateTheme =
            (callback === 'light')
            ? 'dark'
            : 'light'

            themeSwitchBtn.innerHTML=
            `
                <i class="fa-solid ${ alternateTheme === 'light' ? 'fa-moon' : 'fa-sun' }"></i>
            `

            utilities.setTheme(alternateTheme);
            initializePageTheme();

        });

    });

    console.log("Initialized landing page logic!");

    initializePageTheme();

};

export default landingPageLogic;
