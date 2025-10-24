import initializeLandingPage from "./pages/landing.js";
import initializeSignInPage from "./pages/sign-in.js";
import initializeSignUpPage from "./pages/sign-up.js";
import initializeProductDetailPage from "./pages/pdp.js";
import initializeShopPage from "./pages/shop.js";
import initializeCartPage from "./pages/cart.js";
import initializeAboutUsPage from "./pages/about-us.js";
import initializeContactUsPage from "./pages/contact-us.js";
import initializeModalComponent from "./components/modal.js";
import initializeHeaderComponent from "./components/header.js";
import initializeFooterComponent from "./components/footer.js";

document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Initializing main JavaScript entry file!");

    // Pages JavaScript Logic
    initializeLandingPage();
    initializeSignInPage();
    initializeSignUpPage();
    initializeProductDetailPage();
    initializeShopPage();
    initializeCartPage();
    initializeAboutUsPage();
    initializeContactUsPage();

    // Components JavaScript Logic
    initializeModalComponent();
    initializeHeaderComponent();
    initializeFooterComponent();

    console.log("Main JavaScript entry file successfully initialized!");

});
