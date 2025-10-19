import initializeLandingPage from "./pages/landing.js";
import initializeSignInPage from "./pages/sign-in.js";
import initializeSignUpPage from "./pages/sign-up.js";
import initializeProductDetailPage from "./pages/pdp.js";
import initializeShopPage from "./pages/shop.js";
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

    // Components JavaScript Logic
    initializeModalComponent();
    initializeHeaderComponent();
    initializeFooterComponent();

    console.log("Main JavaScript entry file successfully initialized!");

});
