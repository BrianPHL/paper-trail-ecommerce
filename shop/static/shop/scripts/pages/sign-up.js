import * as themeUtilities from "../utils/theme.js";
import * as inputUtilities from "../utils/input.js";


const initializeSignUpPage = () => {

    if (window.location.pathname !== '/sign-up/') return;

    const initializeTheme = () => {

        const htmlElement = document.querySelector('html');
        const main = document.querySelector('.sign_up');
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
        const formStepsProgressBar = document.querySelector('.sign_up-form-progress_bar-level');
        const formCtasContainers = form.querySelectorAll('.sign_up-form-group-ctas-container');
        const formCtasContainersArray = Array.from(formCtasContainers);
        const formGroupContainers = form.querySelectorAll('.sign_up-form-group-container');
        const formGroupContainersArray = Array.from(formGroupContainers);
        const formInputs = form.querySelectorAll('input');
        const formInputsArray = Array.from(formInputs);
        const formSubmitBtns = form.querySelectorAll('.sign_up-form-group-ctas-btn[type="submit"]');
        const formSubmitBtnsArray = Array.from(formSubmitBtns);
        const formResetBtns = form.querySelectorAll('.sign_up-form-group-ctas-btn[type="reset"]');
        const formResetBtnsArray = Array.from(formResetBtns);
        const formReturnBtn = form.querySelector('.sign_up-form-group-ctas-btn[type="button"');

        let currentFormStep = "1";
        let segregatedFormInputs = formInputsArray.filter(formInput => formInput.closest('.sign_up-form-group-container[data-step="1"]'));
        let segregatedFormSubmitBtn = formSubmitBtnsArray.find(formSubmitBtn => formSubmitBtn.parentElement.getAttribute('data-step') === "1");

        const formInputsCheckingHandler = (formInputs, formSubmitBtn) => {

            inputUtilities.handleFormInputsChecking(formInputs, (callback) => {

                if (!formSubmitBtn) return;

                (!callback)
                    ? formSubmitBtn.setAttribute('disabled', 'disabled')
                    : formSubmitBtn.removeAttribute('disabled')


            });

        };

        const showFirstStep = () => {

            const currentFormGroupContainer = formGroupContainersArray.find(formGroupContainer => formGroupContainer.getAttribute('data-step') === '1');
            const previousFormGroupContainer = formGroupContainersArray.find(formGroupContainer => formGroupContainer.getAttribute('data-step') === '2');
            const currentFormCtasContainer = formCtasContainersArray.find(formCtasContainer => formCtasContainer.getAttribute('data-step') === '1');
            const previousFormCtasContainer = formCtasContainersArray.find(formCtasContainer => formCtasContainer.getAttribute('data-step') === '2');

            previousFormCtasContainer.style.display = 'none';
            currentFormCtasContainer.style.display = 'flex';

            previousFormGroupContainer.style.display = 'none';
            currentFormGroupContainer.style.display = 'flex';

            formStepsProgressBar.style.width = "50%";

            currentFormStep = "1";
            segregatedFormInputs = formInputsArray.filter(formInput => formInput.closest('.sign_up-form-group-container[data-step="1"]'));
            segregatedFormSubmitBtn = formSubmitBtnsArray.find(formSubmitBtn => formSubmitBtn.parentElement.getAttribute('data-step') === "1");

            formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        };

        const showSecondStep = () => {
            
            const currentFormGroupContainer = formGroupContainersArray.find(formGroupContainer => formGroupContainer.getAttribute('data-step') === '2');
            const previousFormGroupContainer = formGroupContainersArray.find(formGroupContainer => formGroupContainer.getAttribute('data-step') === '1');
            const currentFormCtasContainer = formCtasContainersArray.find(formCtasContainer => formCtasContainer.getAttribute('data-step') === '2');
            const previousFormCtasContainer = formCtasContainersArray.find(formCtasContainer => formCtasContainer.getAttribute('data-step') === '1');

            previousFormCtasContainer.style.display = 'none';
            currentFormCtasContainer.style.display = 'flex';

            previousFormGroupContainer.style.display = 'none';
            currentFormGroupContainer.style.display = 'flex';

            formStepsProgressBar.style.width = "100%";

            currentFormStep = "2";
            segregatedFormInputs = formInputsArray.filter(formInput => formInput.closest('.sign_up-form-group-container[data-step="2"]'));
            segregatedFormSubmitBtn = formSubmitBtnsArray.find(formSubmitBtn => formSubmitBtn.parentElement.getAttribute('data-step') === "2");

            formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        };

        const handleAccountCreation = () => {

            const formData = new FormData(form);

            // first_name
            // last_name
            // house_address (optional)
            // contact_number
            // email_address
            // password
            // confirm_password

            // TODO: setup POST request here to backend.

        };

        const passwordToggles = form.querySelectorAll('[data-toggle="password"]');
        
        passwordToggles.forEach(passwordToggle => passwordToggle.addEventListener('click', () => {
            
            const input = passwordToggle.previousElementSibling;

            inputUtilities.handlePasswordToggle(input, (callback) => {

                input.type = callback || 'password';
                passwordToggle.className = `fa-solid ${ callback === 'password' ? 'fa-eye-slash' : 'fa-eye' }`
            
            });

        }));

        formInputs.forEach(formInput => formInput.addEventListener('input', () => {

            formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        }));

        formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        formSubmitBtnsArray.forEach(formSubmitBtn => formSubmitBtn.addEventListener('click', (event) => {
            
            event.preventDefault();

            currentFormStep === '1'
            ? showSecondStep()
            : handleAccountCreation()

        }));

        formResetBtnsArray.forEach(formResetBtn => formResetBtn.addEventListener('click', (event) => {

            event.preventDefault();

            segregatedFormInputs.forEach(formInput => formInput.value = '');

            formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        }));

        formReturnBtn.addEventListener('click', showFirstStep);

    };

    initializeThemeHandling();
    initializeFormHandling();
    initializeTheme();

    console.log("Initialized sign in page logic!");

};

export default initializeSignUpPage;
