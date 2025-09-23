import * as utilities from "../utils/theme.js";

const landingPageLogic = async () => {

    const themeSwitchBtn = document.querySelector('#theme-switcher-btn');

    const initializePageTheme = () => {

        utilities.getTheme((callback) => {
            utilities.setTheme(callback);
        })

    }

    themeSwitchBtn.addEventListener('click', () => {
        
        utilities.getTheme((callback) => {

            const alternateTheme =
            (callback === 'light')
            ? 'dark'
            : 'light'

            utilities.setTheme(alternateTheme);
        });

    })

    console.log("Initialized landing page logic!");

    initializePageTheme();

};

export default landingPageLogic;
