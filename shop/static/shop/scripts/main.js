
import initializeLandingPage from "./pages/landing.js";
import initializeSignInPage from "./pages/sign-in.js";
import initializeSignUpPage from "./pages/sign-up.js";
import initializeProductDetailPage from "./pages/pdp.js";
import initializeShopPage from "./pages/shop.js";
import initializeCartPage from "./pages/cart.js";
import initializeAboutUsPage from "./pages/about-us.js";
import initializeContactUsPage from "./pages/contact-us.js";
import initializeProfilePage from "./pages/profile.js";
import initializeFeedbackPage from "./pages/feedback.js";
import initializeCheckoutPage from "./pages/checkout.js";
import initializeModalComponent from "./components/modal.js";
import initializeHeaderComponent from "./components/header.js";
import initializeFooterComponent from "./components/footer.js";

// Cart utilities function
const initializeCartUtils = () => {
    // Function to update cart count in navbar
    window.updateCartCount = (count) => {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    };

    // Function to fetch current cart count from server
    window.refreshCartCount = async () => {
        try {
            const response = await fetch('/api/cart-count/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            if (response.ok) {
                const data = await response.json();
                window.updateCartCount(data.count);
            }
        } catch (error) {
            console.log('Could not refresh cart count:', error);
        }
    };

    // Listen for cart update events
    document.addEventListener('cartUpdated', (event) => {
        if (event.detail && typeof event.detail.count !== 'undefined') {
            window.updateCartCount(event.detail.count);
        } else {
            window.refreshCartCount();
        }
    });
};

document.addEventListener('DOMContentLoaded', () => {

    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

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
    initializeFeedbackPage();
    initializeProfilePage();
    initializeCheckoutPage();

    // Components JavaScript Logic
    initializeModalComponent();
    initializeHeaderComponent();
    initializeFooterComponent();

    // Cart utilities
    initializeCartUtils();

    console.log("Main JavaScript entry file successfully initialized!");

});
