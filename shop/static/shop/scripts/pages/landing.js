import * as utilities from "../utils/theme.js";

const landingPageLogic = async () => {

    const themeSwitchBtn = document.querySelector('#theme-switcher-btn');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        utilities.getTheme((theme) => {

            utilities.setTheme(theme);

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

    })

    console.log("Initialized landing page logic!");

    initializePageTheme();

};

export default landingPageLogic;
