import * as themeUtilities from "../utils/theme.js";
import * as inputUtilities from "../utils/input.js";


const initializeSignInPage = () => {

    if (window.location.pathname !== '/sign-in/') return;

    const initializeTheme = () => {

        const htmlElement = document.querySelector('html');
        const main = document.querySelector('.main');
        const logos = document.querySelectorAll('.logo');
        const mediaQuery = window.matchMedia('(max-width: 1500px');

        themeUtilities.getTheme((theme) => {

            themeUtilities.setTheme(theme);

            logos.forEach(logo => logo.src = `/static/shop/images/logo-${ theme }.png`)

            if (mediaQuery.matches)
                main.style.backgroundImage = `url(/static/shop/images/auth-${ theme }.png)`;

            mediaQuery.addEventListener('change', (event) => {
                if (event.matches) {
                    main.style.backgroundImage = `url(/static/shop/images/auth-${ theme }.png)`;
                } else {
                    main.style.backgroundImage = ``;
                }
            }) 

            htmlElement.setAttribute('data-theme', theme);

        });

    };

    const initializeThemeHandling = () => {
        
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
                initializeTheme();

            });

        }));

    };

    const initializeFormHandling = () => {

        const form = document.querySelector('form');

        const formInputsCheckingHandler = (formInputs, formSubmitBtn) => {

            inputUtilities.handleFormInputsChecking(formInputs, (callback) => {

                (!callback)
                    ? formSubmitBtn.setAttribute('disabled', 'disabled')
                    : formSubmitBtn.removeAttribute('disabled')

            });

        }

        const passwordToggle = form.querySelector('[data-toggle="password"]');
        
        passwordToggle.addEventListener('click', () => {

            const input = passwordToggle.previousElementSibling;

            inputUtilities.handlePasswordToggle(input, (callback) => {

                input.type = callback || 'password';
                passwordToggle.className = `fa-solid ${ callback === 'password' ? 'fa-eye-slash' : 'fa-eye' }`
            
            });

        });

        const formInputs = form.querySelectorAll('input');
        const formSubmitBtn = form.querySelector('button[type="submit"]');

        formInputs.forEach(formInput => formInput.addEventListener('input', () => {
            formInputsCheckingHandler(formInputs, formSubmitBtn)
        }));

        formInputsCheckingHandler(formInputs, formSubmitBtn);

    };

    initializeThemeHandling();
    initializeFormHandling();
    initializeTheme();

    console.log("Initialized sign in page logic!");

};

export default initializeSignInPage;
