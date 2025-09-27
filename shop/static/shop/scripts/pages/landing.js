import * as utilities from "../utils/theme.js";

const initializeLandingPage = () => {

    const themeSwitchBtns = document.querySelectorAll('.theme-switcher-btn');
    const logos = document.querySelectorAll('.logo');
    const hero = document.querySelector('#hero');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        const mediaQuery = window.matchMedia('(max-width: 1500px');

        utilities.getTheme((theme) => {

            utilities.setTheme(theme);

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

    themeSwitchBtns.forEach(themeSwitchBtn => themeSwitchBtn.addEventListener('click', () => {
        
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

    }))

    console.log("Initialized landing page logic!");

    initializePageTheme();

};

export default initializeLandingPage;
