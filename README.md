# Ruth Miskin Portal

## Overview

This app is fairly straightforward, focusing on two clear domains: accounts for user management (registration, login, and member data) and schools for storing and importing school records. By separating these into distinct apps, we keep each area’s logic organized and self-contained. The accounts app handles user creation, password management, and email activation, while the schools app manages a large CSV import process and an efficient search mechanism for selecting schools.

One of the challenges was dealing with large CSV files (potentially tens of thousands of rows). To handle this, we used Pandas for fast reading and bulk creation in Django, carefully avoiding slow lookups by using dictionaries or sets. We also integrated a searchable dropdown (Select2 widget with an AJAX endpoint) so users can find their school without loading every record at once, or in this case, making the register page usable as it'd crash due to the huge payload.

I've also made the decision to separate User (Django’s built-in authentication model) and Member (which contains additional user-related data) was intentional. Keeping authentication-related fields within Django’s User model ensures compatibility with built-in authentication and permission handling. Meanwhile, Member extends this functionality by storing school and birth date information, keeping domain-specific user data separate. 

A major focus was ensuring users can register with a valid school without loading thousands of records into a dropdown. The autocomplete search field makes this possible, querying the backend dynamically for relevant schools based on user input.

## Installation & Setup

### 1. Set up a Virtual Environment
```sh
cd src
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and update the necessary values:
```sh
cp .env.example .env
```
OPTIONAL - You'll be able to get the link from the terminal log as well (for demo purposes ofc)
Modify `.env` with database and email settings :
```env
# Database Configuration
DB_NAME=ruth_portal
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=***
EMAIL_PORT=2525
EMAIL_HOST_USER=****
EMAIL_HOST_PASSWORD=***
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@example.com
```

### 4. Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server
```sh
python manage.py runserver
```

### 6. Load School Data
To import school data from a CSV file:
```sh
python manage.py import_schools schools.csv
```

## Email Configuration
This app uses email verification for account activation. If email setup isn’t available, activation links will be printed in the terminal for manual activation.

## Features
- User registration and authentication
- Email verification with activation links
- Dynamic school selection with search functionality
- Bulk import of schools via CSV
- Authenticated users are redirected to the welcome page

## API & Route Map

### Accounts

- `GET /signup/` - User registration page

- `POST /signup/` - Handles user signup and email verification

- `GET /login/` - Login page

- `POST /login/` - Handles user authentication

- `POST /logout/` - Logs out the user

- `GET /activate/<str:token>/` - Activates a user account via email link

- `GET /password_reset/` - Password reset request page

- `POST /password_reset/` - Handles password reset submission

- `GET /reset/<uidb64>/<token>/` - Password reset confirmation link

- `POST /reset/<uidb64>/<token>/` - Handles password reset confirmation

- `GET /welcome/` - Redirects authenticated users to their dashboard

## Requirements
- Python 3.10+
- Django 5+
- PostgreSQL (or SQLite for development)
<!-- - Redis (if using async tasks) -->

## Notes
- Authenticated users cannot access the login or register pages.
- Schools are imported efficiently using a management command to avoid performance issues.
- The app maintains clear separation between accounts and schools for better maintainability.

