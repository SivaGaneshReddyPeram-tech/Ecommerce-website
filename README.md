# Marketly E-Commerce

A Django e-commerce MVP using SQLite, Django templates, CSS and JavaScript.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install django pillow
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

Django Admin: http://127.0.0.1:8000/admin/

Demo admin account:
- Username: `admin`
- Password: `admin123`

Change the demo password before deployment.

## Features

- Public product catalog with search, category filters and price sorting
- Product detail and server-side session cart
- Registration, login, logout and account pages
- COD checkout with stock and price revalidation
- Atomic order creation and stock reduction
- Customer order history and order details
- Django Admin product, category and order management

## Tests

```powershell
python manage.py test
```
