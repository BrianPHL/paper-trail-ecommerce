# Paper Trail Ecommerce

A Django-based e-commerce platform for stationery products featuring product management, search, filtering, and a modern responsive UI.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/BrianPHL/paper-trail-ecommerce.git
cd paper-trail-ecommerce
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
- On Windows (PowerShell):
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- On Windows (cmd):
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the root directory of the project (same level as `manage.py`):

```env
# Database Configuration
DB_NAME=paper-trail
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

**Important Note:**
- Never commit the `.env` file to version control (it's already in `.gitignore`)

### 6. Set up the database

Create your MySQL database:
```sql
CREATE DATABASE paper-trail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 9. Import products to the database

Run the product import script to populate your database with 30+ products:

```bash
python add_products.py
```

**What this script does:**
- Creates 30+ stationery products across different categories
- Links products to their respective images in the `media/products/` folder
- Includes product details like name, description, price, weight, dimensions, and stock quantity
- Skips products that already exist in the database (safe to run multiple times)

**Expected output:**
```
Looking for images in: C:\path\to\project\media\products
✅ Created 'Classic Spiral Notebook (A5)' with image
✅ Created 'Composition Notebook' with image
...
🎉 Done! Created 33 new products, skipped 0 existing products.
```

**Troubleshooting:**
- If you see `⚠️ Created 'Product Name' but image not found`, make sure the image file exists in `media/products/`
- The script will still create the product entry, but the image won't be displayed until you add the file

### 10. Start the development server
```bash
python manage.py runserver
```

### 11. Access the application

- **Homepage:** `http://127.0.0.1:8000/`
- **Shop Page:** `http://127.0.0.1:8000/shop/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
  - Use the superuser credentials you created in step 8

---

## Project Structure

```
paper-trail-ecommerce/
├── manage.py
├── add_products.py          # Bulk product import script
├── requirements.txt
├── .env                     # Environment variables (create this)
├── media/                   # User-uploaded files
│   └── products/           # Product images
├── paper_trail_ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── shop/
    ├── models.py           # Product, UserProfile models
    ├── views.py            # Landing, shop, product detail views
    ├── admin.py            # Admin configuration
    ├── urls.py
    ├── static/
    │   └── shop/
    │       ├── styles/    # CSS files
    │       ├── scripts/   # JavaScript files
    │       └── images/    # Static images (logo, hero, etc.)
    └── templates/
        └── shop/
            ├── landing.html
            ├── shop.html
            ├── pdp.html
            └── components/
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Need Help?**

- Check the Django documentation: https://docs.djangoproject.com/
- Review the code comments in `models.py` and `views.py`
- Open an issue on GitHub for bug reports or feature requests
