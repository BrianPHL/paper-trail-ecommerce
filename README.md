# Paper Trail Ecommerce

A simple Django project for ecommerce.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/<your-username>/paper-trail-ecommerce.git
   cd paper-trail-ecommerce
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows (PowerShell):
     ```
     .\venv\Scripts\Activate.ps1
     ```
   - On Windows (cmd):
     ```
     .\venv\Scripts\activate.bat
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```
   python manage.py migrate
   ```

6. **Start the development server:**
   ```
   python manage.py runserver
   ```

7. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

---

**Note:**
- Make sure your database settings in `settings.py` are correct for your environment.
- For MySQL, ensure you have a running MySQL server and update credentials as needed.
