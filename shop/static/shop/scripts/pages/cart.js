import * as themeUtilities from "../utils/theme.js";
import * as responsiveUtilities from "../utils/responsive.js";

const initializeCartPage = () => {

    if (window.location.pathname !== '/cart/') return;

    const logos = document.querySelectorAll('.logo');
    const htmlElement = document.querySelector('html');

    const initializePageTheme = () => {

        themeUtilities.getTheme((theme) => {

            themeUtilities.setTheme(theme);

            logos.forEach(logo => logo.src = `/static/shop/images/logo-${ theme }.png`)

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

    const initializePageLayoutHandling = () => {

        const header = document.querySelector('.header');
        const hero = document.querySelector('.cart-wrapper');

        window.addEventListener('resize', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));
        window.addEventListener('load', () => responsiveUtilities.equalizeHeaderAndHeroSpacing(header, hero, false));

    };

    const initializeCartFunctionality = () => {
        // Handle quantity increment/decrement buttons
        const incrementButtons = document.querySelectorAll('.counter-btn[data-action="increment"]');
        const decrementButtons = document.querySelectorAll('.counter-btn[data-action="decrement"]');
        
        // Function to get total cart items count
        const getTotalCartItems = () => {
            let totalItems = 0;
            const cartItems = document.querySelectorAll('.cart-list-item');
            
            cartItems.forEach(item => {
                const quantityInput = item.querySelector('input[name="quantity"]');
                if (quantityInput) {
                    totalItems += parseInt(quantityInput.value) || 0;
                }
            });
            
            return totalItems;
        };
        
        // Function to update cart totals based on SELECTED items only
        const updateCartTotals = () => {
            let subtotal = 0;
            let selectedItemsCount = 0;
            const cartItems = document.querySelectorAll('.cart-list-item');
            
            cartItems.forEach(item => {
                const checkbox = item.querySelector('input[name="cart-select"]');
                const quantityInput = item.querySelector('input[name="quantity"]');
                const priceElement = item.querySelector('.cart-list-item-price-value');
                
                // Only count if checkbox is checked
                if (checkbox && checkbox.checked && quantityInput && priceElement) {
                    const quantity = parseInt(quantityInput.value) || 0;
                    const price = parseFloat(priceElement.textContent.replace('PHP ', '').replace(',', '')) || 0;
                    subtotal += quantity * price;
                    selectedItemsCount++;
                }
            });
            
            // Update summary
            const subtotalElement = document.querySelector('.cart-summary-list-item:first-child h3');
            const totalElement = document.querySelector('.cart-summary-list-item:last-child h3');
            const shippingElement = document.querySelector('.cart-summary-list-item:nth-child(2) h3');
            const checkoutButton = document.querySelector('.cart-summary-proceed_to_checkout');
            
            if (subtotalElement) {
                subtotalElement.textContent = `PHP ${subtotal.toFixed(2)}`;
            }
            
            if (totalElement && shippingElement) {
                const shipping = parseFloat(shippingElement.textContent.replace('PHP ', '')) || 0;
                totalElement.textContent = `PHP ${(subtotal + shipping).toFixed(2)}`;
            }
            
            // Enable/disable checkout button based on selection
            if (checkoutButton) {
                checkoutButton.disabled = selectedItemsCount === 0;
                checkoutButton.style.opacity = selectedItemsCount === 0 ? '0.5' : '1';
            }
        };
        
        // Handle increment buttons
        incrementButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const form = button.closest('form');
                const input = form.querySelector('input[name="quantity"]');
                if (input && !button.disabled) {
                    // Disable button temporarily
                    button.disabled = true;
                    button.style.opacity = '0.6';
                    
                    let currentValue = parseInt(input.value) || 0;
                    input.value = currentValue + 1;
                    updateCartTotals();
                    
                    // Dispatch cart updated event
                    const newCount = getTotalCartItems();
                    document.dispatchEvent(new CustomEvent('cartUpdated', { detail: { count: newCount } }));
                    
                    // Submit form to update server
                    setTimeout(() => {
                        form.submit();
                    }, 200);
                }
            });
        });
        
        // Handle decrement buttons
        decrementButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const form = button.closest('form');
                const input = form.querySelector('input[name="quantity"]');
                if (input && !button.disabled) {
                    let currentValue = parseInt(input.value) || 0;
                    if (currentValue > 0) {
                        // Disable button temporarily
                        button.disabled = true;
                        button.style.opacity = '0.6';
                        
                        input.value = currentValue - 1;
                        updateCartTotals();
                        
                        // Dispatch cart updated event
                        const newCount = getTotalCartItems();
                        document.dispatchEvent(new CustomEvent('cartUpdated', { detail: { count: newCount } }));
                        
                        // Submit form to update server
                        setTimeout(() => {
                            form.submit();
                        }, 200);
                    }
                }
            });
        });
        
        // Handle direct input changes
        const quantityInputs = document.querySelectorAll('input[name="quantity"]');
        quantityInputs.forEach(input => {
            input.addEventListener('change', () => {
                updateCartTotals();
                const form = input.closest('form');
                if (form) {
                    setTimeout(() => {
                        form.submit();
                    }, 100);
                }
            });
        });

        // Handle individual item checkboxes
        const itemCheckboxes = document.querySelectorAll('input[name="cart-select"]');
        itemCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                updateCartTotals();
                updateSelectAllCheckbox();
            });
        });

        // Handle "Select All" checkbox
        const selectAllCheckbox = document.getElementById('cart-select_all');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', () => {
                const isChecked = selectAllCheckbox.checked;
                itemCheckboxes.forEach(checkbox => {
                    checkbox.checked = isChecked;
                });
                updateCartTotals();
            });
        }

        // Function to update "Select All" checkbox state
        const updateSelectAllCheckbox = () => {
            if (selectAllCheckbox) {
                const totalCheckboxes = itemCheckboxes.length;
                const checkedCheckboxes = document.querySelectorAll('input[name="cart-select"]:checked').length;
                
                if (checkedCheckboxes === 0) {
                    selectAllCheckbox.indeterminate = false;
                    selectAllCheckbox.checked = false;
                } else if (checkedCheckboxes === totalCheckboxes) {
                    selectAllCheckbox.indeterminate = false;
                    selectAllCheckbox.checked = true;
                } else {
                    selectAllCheckbox.indeterminate = true;
                    selectAllCheckbox.checked = false;
                }
            }
        };

        // Initialize with no items selected (totals should be 0)
        updateCartTotals();
        updateSelectAllCheckbox();
    };

    initializePageLayoutHandling();
    initializePageTheme();
    initializePageThemeHandling();
    initializeCartFunctionality();

    console.log("Initialized cart page logic!");

};

export default initializeCartPage;
