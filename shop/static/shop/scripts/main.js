import initializeLandingPage from "./pages/landing.js";
import initializeSignInPage from "./pages/sign-in.js";
import initializeSignUpPage from "./pages/sign-up.js";
import initializeProductDetailPage from "./pages/pdp.js";
import initializeModalComponent from "./components/modal.js";

document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Initializing main JavaScript entry file!");

    // Pages JavaScript Logic
    initializeLandingPage();
    initializeSignInPage();
    initializeSignUpPage();
    initializeProductDetailPage();

    // Components JavaScript Logic
    initializeModalComponent();

    console.log("Main JavaScript entry file successfully initialized!");

});
