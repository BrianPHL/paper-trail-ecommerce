import landingPageLogic from "./pages/landing.js";

document.addEventListener('DOMContentLoaded', async () => {
    
    console.log("Initializing main JavaScript entry file!");

    // pages - JavaScript for page-specific logic
    await landingPageLogic();

    console.log("Main JavaScript entry file successfully initialized!");

});
