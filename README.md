# Little Lemon Restaurant API

A restaurant management and ordering REST API built with **Django** and **Django REST Framework**. The API supports menu and category management, customer registration, token-based authentication, shopping carts, order placement, and delivery crew management.

This project demonstrates REST API development, relational database modeling, authentication, role-based permissions, filtering, searching, sorting, and pagination.

## Features

* **User authentication:** Customer registration, login, and token-based authentication.
* **Role-based access:** Separate permissions for managers, delivery crew, and customers.
* **Category management:** Create and browse menu categories.
* **Menu management:** Create, retrieve, update, and delete menu items.
* **Menu discovery:** Filter by category and price, search by menu item or category title, and order results by title or price.
* **Shopping cart:** Add menu items to a personal cart, view cart items, and clear the cart.
* **Order management:** Place orders from cart items and view order details.
* **Delivery management:** Assign orders to delivery crew and update delivery status.
* **Pagination:** Paginated API responses, configured with a page size of three.
* **API throttling:** Configured limits for anonymous and authenticated requests.

## Technology Stack

* Python
* Django 6.1
* Django REST Framework
* Djoser
* Django Filter
* SQLite
* Token Authentication
* Pipenv (for dependency management, if included in the repository)

## Project Structure

```text
LittleLemon/
├── LittleLemon/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── LittleLemonAPI/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── throttles.py
│   └── urls.py
├── manage.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── LICENSE
└── .gitignore
```

The structure above illustrates the main files; your actual repository may contain additional files.

## Data Models

### Category

Stores menu categories.

* `id`: Primary key
* `slug`: URL-friendly category identifier
* `title`: Category name

### MenuItem

Stores restaurant menu items.

* `id`: Primary key
* `title`: Menu item name
* `price`: Price with two decimal places
* `featured`: Indicates whether the item is featured
* `category`: Foreign key referencing Category

### Cart

Stores items added to a customer's cart.

* `user`: Customer who owns the cart item
* `menuitem`: Selected menu item
* `quantity`: Number of units
* `unit_price`: Price per unit when added
* `price`: Total price for the cart item

A user cannot have duplicate cart records for the same menu item according to the model's uniqueness constraint.

### Order

Stores customer orders.

* `user`: Customer who placed the order
* `delivery_crew`: Assigned delivery crew member; optional
* `status`: Boolean delivery status, initially `False`
* `total`: Total order amount
* `date`: Automatically recorded order date

### OrderItem

Stores the menu items associated with an order, including quantity, unit price, and total item price. Each order can contain multiple order items.

## Installation and Setup

### Prerequisites

* Python compatible with the project's Django version
* Pipenv
* Git

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd LittleLemon
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's HTTPS or SSH URL.

### 2. Install dependencies

If `Pipfile` and `Pipfile.lock` are included:

```bash
python -m pipenv sync
```

Activate the environment:

```bash
python -m pipenv shell
```

If you are using a `requirements.txt` instead, install the dependencies using `pip install -r requirements.txt`.

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Create an administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to create your own administrator account.

### 5. Start the development server

```bash
python manage.py runserver
```

The local API root is:

`http://127.0.0.1:8000/api/`

The Django administration interface is available at:

`http://127.0.0.1:8000/admin/`

**Note:** This project is configured for local development. Before deploying it publicly, configure production settings, secrets, allowed hosts, HTTPS, and an appropriate production database.

## Authentication

The API uses Django REST Framework's token authentication.

### Register a customer

**POST** `/api/users/`

Example request:

```json
{
  "username": "customer01",
  "password": "Use-A-Strong-Password"
}
```

### Log in and obtain an authentication token

**POST** `/api/token/login/`

```json
{
  "username": "customer01",
  "password": "Use-A-Strong-Password"
}
```

A successful login returns an authentication token.

### Authenticate subsequent requests

Include the token in the HTTP request header:

```http
Authorization: Token YOUR_AUTH_TOKEN
```

Do not publish real passwords, authentication tokens, secret keys, or database credentials in this repository.

## API Endpoints

All endpoints below are relative to `http://127.0.0.1:8000`.

### General and Authentication

| Method | Endpoint             | Purpose                                                                       |
| ------ | -------------------- | ----------------------------------------------------------------------------- |
| GET    | `/api/`              | API root and endpoint links                                                   |
| POST   | `/api/users/`        | Register a customer                                                           |
| GET    | `/api/users/me/`     | Retrieve the authenticated user's profile                                     |
| POST   | `/api/token/login/`  | Obtain an authentication token                                                |
| POST   | `/api/token/logout/` | Log out and invalidate the token, if supported by the configured Djoser setup |

### Categories

| Method | Endpoint           | Purpose                                        |
| ------ | ------------------ | ---------------------------------------------- |
| GET    | `/api/categories/` | Browse categories                              |
| POST   | `/api/categories/` | Create a category; manager permission required |

Example request:

```json
{
  "slug": "appetizers",
  "title": "Appetizers"
}
```

### Menu Items

| Method    | Endpoint                | Purpose                                         |
| --------- | ----------------------- | ----------------------------------------------- |
| GET       | `/api/menu-items/`      | List menu items                                 |
| POST      | `/api/menu-items/`      | Create a menu item; manager permission required |
| GET       | `/api/menu-items/{id}/` | Retrieve a menu item                            |
| PUT/PATCH | `/api/menu-items/{id}/` | Update a menu item; manager permission required |
| DELETE    | `/api/menu-items/{id}/` | Delete a menu item; manager permission required |

Example request to create a menu item:

```json
{
  "title": "Eggplant Parmigiana",
  "price": "16.00",
  "featured": true,
  "category_id": 2
}
```

The `category_id` must reference an existing category.

#### Filtering, searching, and ordering

Filter by category:

`GET /api/menu-items/?category=2`

Filter by price:

`GET /api/menu-items/?price=16.00`

Search menu item and category titles:

`GET /api/menu-items/?search=salad`

Sort by price in ascending order:

`GET /api/menu-items/?ordering=price`

Sort by price in descending order:

`GET /api/menu-items/?ordering=-price`

Sort by title:

`GET /api/menu-items/?ordering=title`

Menu items are paginated, with a configured page size of three.

### Manager Group Management

Manager endpoints require manager permissions.

| Method | Endpoint                              | Purpose                                   |
| ------ | ------------------------------------- | ----------------------------------------- |
| GET    | `/api/groups/manager/users/`          | List manager group members                |
| POST   | `/api/groups/manager/users/`          | Add an existing user to the Manager group |
| DELETE | `/api/groups/manager/users/{userId}/` | Remove a user from the Manager group      |

Example request to add an existing user:

```json
{
  "username": "customer01"
}
```

The user must already exist.

### Delivery Crew Management

| Method | Endpoint                                    | Purpose                                         |
| ------ | ------------------------------------------- | ----------------------------------------------- |
| GET    | `/api/groups/delivery-crew/users/`          | List delivery crew members                      |
| POST   | `/api/groups/delivery-crew/users/`          | Add an existing user to the Delivery crew group |
| DELETE | `/api/groups/delivery-crew/users/{userId}/` | Remove a user from the Delivery crew group      |

These endpoints require manager permissions.

### Shopping Cart

Cart endpoints are intended for authenticated customers.

| Method | Endpoint                | Purpose                            |
| ------ | ----------------------- | ---------------------------------- |
| GET    | `/api/cart/menu-items/` | View the current user's cart items |
| POST   | `/api/cart/menu-items/` | Add a menu item to the cart        |
| DELETE | `/api/cart/clear/`      | Clear the current user's cart      |

Example request to add an item:

```json
{
  "menuitem": 5,
  "quantity": 2
}
```

The API calculates the unit price from the menu item and the total price from the quantity.

### Orders

| Method | Endpoint                 | Purpose                                                                             |
| ------ | ------------------------ | ----------------------------------------------------------------------------------- |
| GET    | `/api/orders/`           | List orders according to the user's role                                            |
| POST   | `/api/orders/`           | Create an order from the current user's cart                                        |
| GET    | `/api/orders/{orderId}/` | Retrieve an order                                                                   |
| PATCH  | `/api/orders/{orderId}/` | Update order assignment or delivery status, subject to role checks                  |
| PUT    | `/api/orders/{orderId}/` | Update through the same custom update handler; verify permitted fields before using |
| DELETE | `/api/orders/{orderId}/` | Delete an order; manager permission required                                        |

To place an order, add menu items to the cart first and then send an empty JSON object:

```json
{}
```

to `POST /api/orders/`.

The API calculates the order total, creates order items from the cart, and clears the customer's cart after order creation.

Example order response:

```json
{
  "id": 1,
  "user": 6,
  "delivery_crew": null,
  "status": false,
  "total": "42.00",
  "date": "2026-10-02",
  "items": []
}
```

The `items` array contains the order's menu items, quantities, unit prices, and item totals. The empty array above is illustrative; a real response includes the created order items.

#### Order access by role

* **Customers:** View their own orders and place new orders.
* **Managers:** View all orders and assign orders to delivery crew members.
* **Delivery crew:** View orders assigned to them and update delivery status.

The intended delivery workflow is to assign an order to a user in the Delivery crew group, then allow that crew member to mark the order as delivered by setting `status` to `true`.

## Role and Permission Overview

| Operation                          | Customer      | Manager                                 | Delivery crew                           |
| ---------------------------------- | ------------- | --------------------------------------- | --------------------------------------- |
| Browse categories                  | Authenticated | Yes                                     | Authenticated                           |
| Browse menu items                  | Authenticated | Yes                                     | Authenticated                           |
| Create or modify menu items        | No            | Yes                                     | No                                      |
| Manage manager and delivery groups | No            | Yes                                     | No                                      |
| Manage own cart                    | Yes           | No, unless also permitted as a customer | No, unless also permitted as a customer |
| Place orders                       | Yes           | Depends on `IsCustomer` implementation  | Depends on `IsCustomer` implementation  |
| View orders                        | Own orders    | All orders                              | Assigned orders                         |
| Assign delivery crew               | No            | Yes                                     | No                                      |
| Update delivery status             | No            | Yes                                     | Yes, subject to the view's update logic |

**Permission note:** The precise behavior of `IsCustomer`, `IsManager`, and the order update handler depends on the implementations in `permissions.py` and `views.py`. Review those files before treating this table as a complete security guarantee.

## API Configuration

The project settings configure:

* Token authentication using Django REST Framework.
* Django Filter, SearchFilter, and OrderingFilter.
* Pagination with a default page size of three.
* Anonymous request throttling at 10 requests per minute.
* Authenticated-user throttling at 20 requests per minute.
* SQLite as the development database.

These limits are configuration values and may be adjusted for testing or production requirements.

## Testing the API

You can test the endpoints using Insomnia, Postman, or `curl`.

Recommended testing sequence:

1. Create an administrator using `createsuperuser`.
2. Log in to Django Admin and create the `Manager` and `Delivery crew` groups if they do not already exist.
3. Register a customer through `/api/users/`.
4. Obtain a token through `/api/token/login/`.
5. Add users to the appropriate groups using Django Admin or manager endpoints.
6. Create categories and menu items as a manager.
7. Browse and filter menu items as an authenticated user.
8. Add items to a customer's cart.
9. Place an order and verify that the cart is cleared.
10. Assign the order to a delivery crew member.
11. Log in as that delivery crew member and test delivery status updates.
12. Verify that customers cannot access other customers' orders.

Use test accounts and dummy data. Never include working credentials or tokens in screenshots, commits, or public documentation.

## Security and Deployment Notes

This repository is intended as a learning and portfolio project.

Before production deployment:

* Move `SECRET_KEY` to an environment variable and replace any exposed secret.
* Set `DEBUG = False`.
* Configure `ALLOWED_HOSTS`.
* Review all custom permissions and object-level access controls.
* Validate order updates so delivery crew members can change only permitted fields.
* Handle invalid menu item IDs and quantities with appropriate validation.
* Review the database, HTTPS, logging, backups, and deployment settings.
* Remove local database files and private test data from version control.

## License

This project is distributed under the license specified in the repository's `LICENSE` file. Refer to that file for the applicable terms.
