import initializeLandingPage from "./pages/landing.js";
import initializeModalComponent from "./components/modal.js";

document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Initializing main JavaScript entry file!");

    initializeLandingPage();
    initializeModalComponent();

    console.log("Main JavaScript entry file successfully initialized!");

});
