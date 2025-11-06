import * as themeUtilities from "../utils/theme.js";
import * as inputUtilities from "../utils/input.js";
import * as responsiveUtilities from "../utils/responsive.js";
import { createUser } from "../api/auth.js";

const initializeSignUpPage = () => {

    if (window.location.pathname !== '/sign-up/') return;

    const initializePageTheme = () => {

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

    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validatePhoneNumber = (phone) => {
        const phoneRegex = /^(09|\+639)\d{9}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    };

    const showInputError = (inputElement, message) => {
        const inputContainer = inputElement.closest('.sign_up-form-group-input');
        const errorSpan = inputContainer.querySelector('.form-input-error');

        if (inputElement.classList.contains('input-nested')) {
            inputElement.closest('.input-with-btn').classList.add('error');
        } else {
            inputElement.classList.add('error');
        }

        errorSpan.textContent = message;
        errorSpan.style.display = 'block';
    };

    const clearInputError = (inputElement) => {
        const inputContainer = inputElement.closest('.sign_up-form-group-input');
        const errorSpan = inputContainer.querySelector('.form-input-error');

        if (inputElement.classList.contains('input-nested')) {
            inputElement.closest('.input-with-btn').classList.remove('error');
        } else {
            inputElement.classList.remove('error');
        }

        errorSpan.textContent = '';
        errorSpan.style.display = 'none';
    };

    const validateInput = (inputElement, allInputs = null) => {
        const inputName = inputElement.name;
        const inputValue = inputElement.value.trim();

        clearInputError(inputElement);

        if (inputElement.required && !inputValue) {
            showInputError(inputElement, 'This field is required');
            return false;
        }

        if (!inputElement.required && !inputValue) {
            return true;
        }

        if (inputName === 'first_name' && inputValue) {
            if (inputValue.length < 2) {
                showInputError(inputElement, 'First name must be at least 2 characters');
                return false;
            }
            if (!/^[a-zA-Z\s]+$/.test(inputValue)) {
                showInputError(inputElement, 'First name should only contain letters');
                return false;
            }
        }

        if (inputName === 'last_name' && inputValue) {
            if (inputValue.length < 2) {
                showInputError(inputElement, 'Last name must be at least 2 characters');
                return false;
            }
            if (!/^[a-zA-Z\s]+$/.test(inputValue)) {
                showInputError(inputElement, 'Last name should only contain letters');
                return false;
            }
        }

        if (inputName === 'contact_number' && inputValue) {
            if (!validatePhoneNumber(inputValue)) {
                showInputError(inputElement, 'Please enter a valid Philippine phone number (e.g., 09123456789)');
                return false;
            }
        }

        if (inputName === 'email_address' && inputValue) {
            if (!validateEmail(inputValue)) {
                showInputError(inputElement, 'Please enter a valid email address');
                return false;
            }
        }

        if (inputName === 'password' && inputValue) {
            if (inputValue.length < 8) {
                showInputError(inputElement, 'Password must be at least 8 characters long');
                return false;
            }
            if (!/(?=.*[a-z])/.test(inputValue)) {
                showInputError(inputElement, 'Password must contain at least one lowercase letter');
                return false;
            }
            if (!/(?=.*[A-Z])/.test(inputValue)) {
                showInputError(inputElement, 'Password must contain at least one uppercase letter');
                return false;
            }
            if (!/(?=.*\d)/.test(inputValue)) {
                showInputError(inputElement, 'Password must contain at least one number');
                return false;
            }
        }

        if (inputName === 'confirm_password' && inputValue && allInputs) {
            const passwordInput = Array.from(allInputs).find(input => input.name === 'password');
            if (passwordInput && inputValue !== passwordInput.value) {
                showInputError(inputElement, 'Passwords do not match');
                return false;
            }
        }

        return true;
    };

    const validateStepInputs = (stepInputs, allInputs) => {
        let isValid = true;
        stepInputs.forEach(input => {
            if (!validateInput(input, allInputs)) {
                isValid = false;
            }
        });
        return isValid;
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
        const formReturnBtn = document.querySelector('.sign_up-form-group-ctas-btn[type="button"');
        const formError = document.querySelector('.sign_up-form-error');
        const formErrorText = formError.querySelector('.sign_up-form-error-text');

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

            if (!validateStepInputs(segregatedFormInputs, formInputsArray)) {
                return;
            }

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

        const handleAccountCreation = async () => {

            if (!validateStepInputs(segregatedFormInputs, formInputsArray)) {
                return;
            }

            const formData = new FormData(form);

            formError.style.display = 'none';

            try {

                if (formData.get('password') !== formData.get('confirm_password'))
                    throw new Error('Passwords do not match!');
            
                const result = await createUser({
                    first_name: formData.get('first_name'),
                    last_name: formData.get('last_name'),
                    house_address: formData.get('house_address'),
                    contact_number: formData.get('contact_number'),
                    email_address: formData.get('email_address'),
                    password: formData.get('password')
                });

                if (!result.success)
                    throw new Error(result.err || 'Failed to create user!');

                window.location.href = '/sign-in';

            } catch (err) {

                formError.style.display = 'flex';
                formErrorText.innerHTML = err.message;

            }

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

            segregatedFormInputs.forEach(formInput => {
                formInput.value = '';
                clearInputError(formInput);
            });

            formInputsCheckingHandler(segregatedFormInputs, segregatedFormSubmitBtn);

        }));

        formReturnBtn.addEventListener('click', showFirstStep);

    };

    const initializePageLayoutHandling = () => {

        const formSignUp = document.querySelector('.sign_up');

        window.addEventListener("resize", () => responsiveUtilities.equalizeChildrenHeightInContainer(formSignUp));
        window.addEventListener("load", () => responsiveUtilities.equalizeChildrenHeightInContainer(formSignUp));

    };

    initializePageLayoutHandling();
    initializePageTheme();
    initializePageThemeHandling();
    initializeFormHandling();

    console.log("Initialized sign in page logic!");

};

export default initializeSignUpPage;
