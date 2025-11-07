# Paper Trail | Premium Stationery E-commerce

A full-stack Django-based e-commerce platform for premium stationery products, featuring comprehensive inventory management, shopping cart functionality, user profiles, and an enhanced admin dashboard with analytics.

## 🌟 Features

### Customer-Facing Features
- **Product Catalog**: Browse and filter stationery products with advanced search and category filtering
- **Shopping Cart**: Add products without page reload using AJAX, manage quantities, and proceed to checkout
- **Order Management**: Place orders with Cash on Delivery, track order history and status
- **User Authentication**: Sign up, sign in with secure password validation and session management
- **User Profiles**: Manage account information, multiple shipping addresses, and preferences
- **Multi-Currency Support**: Choose preferred currency (PHP, USD, EUR) for pricing display
- **Product Details**: View comprehensive product information including weight, dimensions, and stock availability
- **Customer Feedback**: Submit feedback and suggestions through dedicated feedback form
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes with persistent preference storage

### Admin Panel Features
- **Analytics Dashboard**: Sales analytics with Chart.js visualizations showing monthly revenue and order trends
- **Inventory Management**: Comprehensive stock tracking with transaction history and low-stock alerts
- **Product Management**: CRUD operations with image upload and bulk editing capabilities
- **Order Management**: Process orders, update status (Pending → Out for Delivery → Delivered → Returned/Refunded)
- **Stock History**: Complete audit trail of all inventory transactions (sales, restocks, adjustments, returns)
- **Feedback Management**: View and respond to customer feedback with categorization
- **User Management**: Admin user accounts with profile management
- **Real-time Stock Deduction**: Automatic inventory updates when orders are placed

## 🛠️ Tech Stack

### Backend
- **Django 5.2.6** - Web framework with ORM, authentication, and admin interface
- **MySQL 8.4** - Relational database with connection pooling
- **Pillow 11.3.0** - Image processing for product/profile pictures

### Frontend
- **JavaScript ES6 + Fetch API** - AJAX cart operations without page reloads
- **CSS Custom Properties** - Light/dark theme system with design tokens

### Development Tools
- **python-dotenv** - Environment variable management for secure configuration
- **django-watchfiles & django-browser-reload** - Auto-reload tools for faster development

## 📁 Project Structure

```bash
paper-trail-ecommerce/
├── manage.py                                    # Django management script
├── add_products.py                              # Bulk product import utility
├── requirements.txt                             # Python dependencies
├── .env                                         # Environment variables (create this)
├── media/                                       # User-uploaded files
│   ├── products/                               # Product images
│   └── profiles/                               # User profile pictures
├── paper_trail_ecommerce_project/              # Django project configuration
│   ├── settings.py                             # Global settings
│   ├── urls.py                                 # Root URL configuration
│   └── wsgi.py                                 # WSGI deployment
└── shop/                                       # Main application
    ├── models.py                               # Data models (Product, Cart, Order, etc.)
    ├── views.py                                # View functions (25+ routes)
    ├── admin.py                                # Enhanced admin with dashboards
    ├── urls.py                                 # URL routing
    ├── context_processors.py                   # Global template context
    ├── migrations/                             # Database migrations
    ├── static/
    │   └── shop/
    │       ├── styles/                         # CSS with theme system
    │       │   ├── main.css
    │       │   ├── abstracts/                  # Theme variables
    │       │   ├── components/                 # UI components
    │       │   └── layout/                     # Page layouts
    │       ├── scripts/                        # JavaScript modules
    │       │   ├── main.js
    │       │   ├── api/                        # API utilities
    │       │   ├── components/                 # Reusable components
    │       │   ├── pages/                      # Page-specific scripts
    │       │   └── utils/                      # Helper functions
    │       └── images/                         # Static assets
    └── templates/
        └── shop/
            ├── landing.html                    # Homepage
            ├── shop.html                       # Product listing
            ├── pdp.html                        # Product detail page
            ├── cart.html                       # Shopping cart
            ├── checkout.html                   # Checkout form
            ├── checkout_success.html           # Order confirmation
            ├── profile.html                    # User profile management
            ├── orders.html                     # Order history
            ├── order_detail.html               # Individual order view
            ├── feedback.html                   # Feedback form
            ├── about-us.html                   # About page
            ├── contact-us.html                 # Contact page
            ├── sign-in.html                    # Login
            ├── sign-up.html                    # Registration
            └── components/                     # Reusable templates
                ├── header.html
                ├── footer.html
                ├── product_card.html
                └── cart_ajax_script.html
```
## 🚀 Getting Started
### Prerequisites
- Python 3.13 or higher
- MySQL 8.4 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation
1. **Clone the repository**
```bash
git clone https://github.com/BrianPHL/paper-trail-ecommerce.git
cd paper-trail-ecommerce
```
2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\venv\Scripts\activate.bat

# Activate (macOS/Linux)
source venv/bin/activate
```
3. **Install project dependencies**
```bash
pip install -r requirements.txt
```
4. **Configure environment variables**
Create a ``.env`` file in the root directory:
```bash
# Database Configuration
DB_NAME=paper_trail
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```
5. **Set up the database**
Create a ``.env``file in the root directory:
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE paper_trail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Run migrations
python manage.py makemigrations
python manage.py migrate
```
6. **Create superuser account**
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.
7. **Import sample products to the database**
```bash
python add_products.py
```
This script imports 30+ stationery products with images and product details.
8. **Run the development server**
```bash
python manage.py runserver
```
9. **Access the application**
- Homepage: http://127.0.0.1:8000/
- Shop: http://127.0.0.1:8000/shop/
- Admin Panel: http://127.0.0.1:8000/admin/
- Cart: http://127.0.0.1:8000/cart/
- Profile: http://127.0.0.1:8000/profile/
## 🔑 Key Features Explained
### AJAX Shopping Cart
- Add products to cart without page reload using Fetch API
- Real-time cart count updates in header
- Styled notifications matching design system theme
- MutationObserver for dynamically loaded product cards
- Update quantities and remove items asynchronously
### Inventory Management System
- **Automatic Stock Deduction:** Stock decreases when orders are placed
- **Transaction Tracking:** Complete audit trail of all stock changes
- **Transaction Types:** Sale, Restock, Manual Adjustment, Return, Damaged/Lost
- **Low Stock Alerts:** Visual indicators in admin for products needing restock
- **Stock Status:** Real-time status (In Stock, Low Stock, Out of Stock, Discontinued)
- **Inventory Dashboard:** Admin view showing low stock products, recent transactions, and stock movement analytics
### Enhanced Admin Panel
- **Sales Analytics:** Monthly revenue charts, top/bottom products, order statistics
- **Transaction Tracking:** Complete audit trail of all stock changes
- **Order History:** Complete order tracking with status breakdown and top customers
- **Product Inventory History:** Per-product transaction history with stock changes
- **Bulk Editing:** Update prices, stock, and product flags directly from list view
- **Image Preview:** Visual product image thumbnails in admin list
- **Custom Dashboards:** Dedicated views for inventory and order management
### User Profile Management
- Multiple shipping addresses with default selection
- Profile picture upload with image optimization
- Currency preference (PHP, USD, EUR)
- Payment method preference
- Address management (add, edit, delete)
- Password change functionality
- Account deletion with confirmation
### Theme System
- CSS custom properties for consistent styling
- Light and dark mode with smooth transitions
- User preference stored in localStorage
- Theme toggle in header with instant switching
## 📊 Database Schema
### Core Tables
- **accounts** - User authentication and profiles (User, UserProfile)
- **products** - Product catalog with categories, images, and stock (Product)
- **carts** - Shopping cart management (Cart, CartItem)
- **orders** - Order lifecycle with items and status tracking (Order, OrderItem)
- **addresses** - User shipping and billing addresses (Address)
- **inventory** - Stock tracking with transaction history (InventoryTransaction)
- **feedback** - Customer feedback and support (Feedback)
### Key Models Overview
- **Product:** Name, slug, description, image, price, category, stock quantity, dimensions, weight, featured/bestseller flags
- **Cart/CartItem:** Session-based or user-linked carts with line items
- **Order/OrderItem:** Complete order information with status workflow
- **InventoryTransaction:** Audit trail for all stock changes with before/after quantities
- **Address:** Multiple addresses per user with default selection
- **UserProfile:** Extended user data with currency/payment preferences and profile picture
## 🔒 Security Features
- Django's built-in password hashing (PBKDF2)
- CSRF protection on all forms
- Session-based authentication
- SQL injection prevention with ORM parameterized queries
- XSS protection with template auto-escaping
- Environment variable protection for sensitive data
- Login required decorators for protected routes
- Secure password validation rules
## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## 👥 Authors
- Brian ([BrianPHL](https://github.com/BrianPHL)) - Lead Developer
- Pel ([qkpl](https://github.com/qkpl)) - Developer
- jassywinter ([jassywinter](https://github.com/jassywinter)) - Developer
- CASAVERDE123 ([CASAVERDE123](https://github.com/CASAVERDE123)) - Developer
## 🎓 Acknowledgments
This project demonstrates:
- Modern Django development practices with MVT architecture
- Real-world e-commerce functionality with inventory management
- AJAX integration for enhanced user experience
- Comprehensive admin customization with analytics dashboards
- Responsive design with CSS custom properties and theme system
## 📝 Notes
This is a demonstration project for academic purposes. For production deployment, ensure all security best practices are followed, including:
- Strong ``SECRET_KEY`` in production
- ``DEBUG = False in`` production
- Proper SSL/TLS configuration
- Database connection security
- Regular security audits
- ``ALLOWED_HOSTS`` configuration
- Static file serving via CDN or web server