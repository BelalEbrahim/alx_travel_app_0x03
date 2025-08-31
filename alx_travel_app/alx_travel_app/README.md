Here’s your updated **all-in-one tab code** with improvements: added authentication mention, extended API endpoints (reviews, auth), and clearer setup steps.

````markdown
# 🧳 ALX Travel App (alx_travel_app_0x00)

A backend application for a travel booking platform built with **Django** and **Django REST Framework (DRF)**.  
This project provides a RESTful API to manage travel listings, user bookings, and reviews.  
It serves as a practical example of building a scalable, API-driven web service.

---

## ✨ Key Features

- **Listings Management**: CRUD (Create, Read, Update, Delete) operations for travel listings.
- **Booking System**: Endpoints for users to create and manage their bookings.
- **User Reviews**: Functionality for users to leave reviews and ratings on listings.
- **Authentication & Authorization**: User registration, login, and JWT-based authentication.
- **Database Seeding**: A custom management command to populate the database with sample data for easy testing.
- **Environment-Based Configuration**: Securely manages settings like secret keys and database credentials using a `.env` file.

---

## 🚀 Tech Stack

- **Backend**: Python, Django
- **API**: Django REST Framework (DRF)
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Database**: SQLite (default for development, can be swapped with PostgreSQL/MySQL)
- **Environment Variables**: `django-environ`
- **Data Seeding**: `Faker` library for generating sample data

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/BelalEbrahim/alx_travel_app_0x03.git
cd alx_travel_app_0x03
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run Database Migrations

Apply schema changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed the Database (Optional)

Populate the database with sample listings, bookings, and reviews:

```bash
python manage.py seed_data
```

### 7. Start Development Server

```bash
python manage.py runserver
```

---

## 📡 API Endpoints

### Listings

| Method   | Endpoint              | Description                      |
| :------- | :-------------------- | :------------------------------- |
| `GET`    | `/api/listings/`      | Retrieve a list of all listings. |
| `POST`   | `/api/listings/`      | Create a new listing.            |
| `GET`    | `/api/listings/<id>/` | Retrieve a single listing.       |
| `PUT`    | `/api/listings/<id>/` | Update an existing listing.      |
| `DELETE` | `/api/listings/<id>/` | Delete a listing.                |

### Bookings

| Method   | Endpoint              | Description             |
| :------- | :-------------------- | :---------------------- |
| `POST`   | `/api/bookings/`      | Create a new booking.   |
| `GET`    | `/api/bookings/`      | Retrieve user bookings. |
| `DELETE` | `/api/bookings/<id>/` | Cancel a booking.       |

### Reviews

| Method   | Endpoint             | Description               |
| :------- | :------------------- | :------------------------ |
| `POST`   | `/api/reviews/`      | Create a new review.      |
| `GET`    | `/api/reviews/`      | Retrieve all reviews.     |
| `GET`    | `/api/reviews/<id>/` | Retrieve a single review. |
| `PUT`    | `/api/reviews/<id>/` | Update a review.          |
| `DELETE` | `/api/reviews/<id>/` | Delete a review.          |

### Authentication

| Method | Endpoint              | Description          |
| :----- | :-------------------- | :------------------- |
| `POST` | `/api/auth/register/` | Register a new user. |
| `POST` | `/api/auth/login/`    | Obtain JWT token.    |
| `POST` | `/api/auth/refresh/`  | Refresh JWT token.   |

---

## 📌 Notes

* Default database is **SQLite**. For production, configure PostgreSQL or MySQL via `.env`.
* All write operations (`POST`, `PUT`, `DELETE`) require authentication.
* Extendable to include payment gateways, notifications, or advanced search.

